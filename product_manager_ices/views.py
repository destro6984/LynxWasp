from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.base import View

from product_manager_ices.forms import AddFlavourForm, AddIceForm, AddOrderItem
from product_manager_ices.models import Order, OrderItem


class HomepageView(View):
    def get(self, request):
        return render(request, "homepage.html")


class IceView(LoginRequiredMixin, View):
    """
    Class to add products by type and flavoures,
    Two separate forms given
    """

    def get(self, request):
        form_type = AddIceForm()
        form_flavour = AddFlavourForm()
        return render(
            request,
            "product_manager_ices/add_ices.html",
            context={
                "form_type": form_type,
                "form_flavour": form_flavour,
            },
        )

    def post(self, request):
        form_type = AddIceForm(request.POST)
        form_flavour = AddFlavourForm(request.POST)

        if "addtype" in request.POST and not form_type.is_valid():
            for error in form_type.errors:
                messages.error(request, f"{form_type.errors[error].as_text()}")
        elif form_type.is_valid():
            form_type.save()
            messages.success(request, "Type Added")
            return redirect("add-ice")

        if "addflavour" in request.POST and not form_flavour.is_valid():
            for error in form_type.errors:
                messages.error(request, f"{form_type.errors[error].as_text()}")
        elif form_flavour.is_valid():
            form_flavour.save()
            messages.success(request, "Flavour Added")
            return redirect("add-ice")

        return redirect("add-ice")


class CreateOrderItemView(LoginRequiredMixin, View):
    """
    Main Page to service the Ice sale:
    Choosing type,quantity,flavours
    Only one order can be open and being active / orders can be postponed or deleted
    """

    def get(self, request):
        add_order_form = AddOrderItem()
        try:
            opened_order = Order.objects.filter(
                worker_owner=request.user, status=Order.Status.STARTED
            ).first()
            summarize = opened_order.get_total() if opened_order else None
        except ObjectDoesNotExist:
            opened_order, summarize = None, None
        return render(
            request,
            "product_manager_ices/order_form.html",
            context={
                "add_order_form": add_order_form,
                "opened_order": opened_order,
                "summarize": summarize,
            },
        )

    def post(self, request):
        add_order_form = AddOrderItem(request.POST)

        if add_order_form.is_valid():
            ice = add_order_form.cleaned_data.get("ice")
            quantity = add_order_form.cleaned_data.get("quantity")

            # Order add order-items-ices to cart
            order = Order.objects.get(
                worker_owner=request.user, status=Order.Status.STARTED
            )

            # Create order-items-ices
            ice_in_order = OrderItem.objects.create(
                ice_id=ice.id, quantity=quantity, order=order
            )

            # Adding flavour to order-item(ice)
            ice_in_order.flavour.set(request.POST.getlist("flavour"))

            ice_in_order.save()
            messages.success(request, "Added to cart")
            return redirect("create-order-item")
        else:
            for error in add_order_form.errors:
                messages.error(request, f"{add_order_form.errors[error].as_text()}")
            return redirect("create-order-item")


@login_required
def open_order(request: HttpRequest) -> HttpResponseRedirect:
    """
    description: opens new order
    Remark: one user can have only one order opened
    """
    if request.method == "POST":
        order_opened = Order.objects.filter(
            worker_owner=request.user, status=Order.Status.STARTED
        ).exists()
        if not order_opened:
            Order.objects.create(worker_owner=request.user, status=Order.Status.STARTED)
            messages.info(request, "You have opened order")
            return redirect("create-order-item")
        else:
            messages.error(request, "You have already opened order")
            return redirect("create-order-item")


@login_required
def delete_orderitem(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """
    Deleting order-item in current order CART
    """
    if request.method == "POST":
        order_to_delete = OrderItem.objects.get(id=pk)
        order_to_delete.delete()
    return redirect("create-order-item")


@login_required
def change_status_order_for_finish(
    request: HttpRequest, pk: int
) -> HttpResponseRedirect:
    """
    Change status of order to finished
    Boostrap Modal > buttons PAY>Finish
    """
    if request.method == "POST":
        order_to_change_status = Order.objects.get(
            id=pk, worker_owner=request.user, status=Order.Status.STARTED
        )
        order_to_change_status.status = Order.Status.FINISHED
        order_to_change_status.save()
    return redirect("create-order-item")


@login_required
def postpone_order(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """
    Postpone current order in CART
    button> POSTPONE
    """
    if request.method == "POST":
        order_to_change_status = Order.objects.get(
            id=pk, worker_owner=request.user, status=Order.Status.STARTED
        )
        order_to_change_status.status = Order.Status.WAITING
        order_to_change_status.save()
    return redirect("create-order-item")


@login_required
def reactivate_order(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """
    Change status of order form postpone to started
    List-of-orders button> return order to active
    Only the same user can return the order to active
    ONLY ONE ORDER CAN BE ACTIVE IN CART
    """
    if Order.objects.filter(
        worker_owner=request.user, status=Order.Status.STARTED
    ).exists():
        messages.info(
            request, "You have active order opened, Please postpone or delete it"
        )
        return redirect("create-order-item")
    else:
        order_to_change_status = Order.objects.get(worker_owner=request.user, id=pk)
        order_to_change_status.status = Order.Status.STARTED
        order_to_change_status.save()
        return redirect("create-order-item")


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deleting whole current order in CART
    """

    model = Order
    success_url = reverse_lazy("create-order-item")


class OrderListView(LoginRequiredMixin, ListView):
    """
    List of finished orders
    Search of orders by USER/SELL-TIME/FLAVOUR/TYPE-OF-ICE
    Only the same user can return the order to active
    """

    model = Order
    context_object_name = "orderlist"
    paginate_by = 7

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            queryset = (
                Order.objects.select_related('worker_owner').filter(worker_owner=self.request.user)
                .filter(
                    Q(worker_owner__username__icontains=query)
                    | Q(time_sell__icontains=query)
                    | Q(orderitem__flavour__flavour__icontains=query)
                    | Q(orderitem__ice__type__contains=query)
                )
                .order_by("-time_sell")
                .distinct()
            )
        else:
            queryset = Order.objects.select_related('worker_owner').filter(worker_owner=self.request.user).order_by(
                "-time_sell"
            )
        return queryset


class OrderDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    """
    Detail of every order
    Only owner of order can see the details.
    """

    model = Order

    def test_func(self):
        user = Order.objects.get(id=self.kwargs.get("pk"))
        return self.request.user.id == user.worker_owner.id
