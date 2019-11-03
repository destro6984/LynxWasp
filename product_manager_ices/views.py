from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.views.generic.base import View

from product_manager_ices.forms import AddIceForm, AddFlavourForm, AddOrderItem
from product_manager_ices.models import Ices, Order, OrderItem
from users_app.models import MyUser


class Homepage(View):
    """
    Welcome Page
    """
    def get(self, request):
        return render(request, 'Homepage.html')


class AddIce(LoginRequiredMixin,View):
    """
    Class to add products by type and flavoures,
    Two separate forms given
    """

    def get(self, request):
        form_type = AddIceForm()
        form_flavour = AddFlavourForm()
        return render(request, 'product_manager_ices/add_ices.html', context={"form_type": form_type,
                                                                              "form_flavour": form_flavour, })

    def post(self, request):

        form_type = AddIceForm(request.POST)
        form_flavour = AddFlavourForm(request.POST)

        if form_type.is_valid():
            form_type.save()
            messages.success(request, "Type Added")
            return redirect("add-ice")
        if form_flavour.is_valid():
            form_flavour.save()
            messages.success(request, "Flavour Added")
            return redirect("add-ice")
        else:
            form_type = AddIceForm()
            form_flavour = AddFlavourForm()
            messages.success(request, "Wrong Data")
        return render(request, 'product_manager_ices/add_ices.html', context={"form_type": form_type,
                                                                              "form_flavour": form_flavour, })


# TODO/inprogress
# def price_of_ice(request):
#     order=Order.objects.get(worker_owner=request.user, status=1)
#     if len(request.POST.getlist('flavour')) == 1:
#         order.ices_ordered
#     elif len(request.POST.getlist('flavour')) == 2:
#         order.ices_ordered.ice.price=15
#     elif len(request.POST.getlist('flavour')) ==3:
#         order.ices_ordered.ice.price=16




class CreateOrder(LoginRequiredMixin, View):
    """
    Main Page to service the Ice sale:
    Choosing type,quantity,flavoures
    SideBar Shop Cart
    Only one order can be open and being active / orders can be postpone or deleted
    """
    def get(self, request):
        add_order_form = AddOrderItem()
        try:
            order_in_cart = Order.objects.get(worker_owner=request.user, status=1)
            sumarize = order_in_cart.get_total()
        except ObjectDoesNotExist:
            order_in_cart = None
            sumarize = None
        return render(request, 'product_manager_ices/order_form.html', context={"add_order_form": add_order_form,
                                                                                "order_in_cart": order_in_cart,
                                                                                "sumarize": sumarize,
                                                                                })

    def post(self, request):

        add_order_form = AddOrderItem(request.POST)
        valid = add_order_form.is_valid()
        if valid:
            ice = add_order_form.cleaned_data.get('ice')
            quantity = add_order_form.cleaned_data.get('quantity')
            # create order_items-ices
            ice_in_order = OrderItem.objects.create(ice_id=ice, quantity=quantity)
            ice_in_order.flavour.set(request.POST.getlist('flavour')) # 1 of thai  Flavouers:czekolada
            # Order exists - add order_items-ices to cart not-exists- create order and add order_items-ices
            if Order.objects.filter(worker_owner=request.user, status=1).exists():
                orde = Order.objects.get(worker_owner=request.user, status=1)
                ice_in_order.order.add(orde.id)
                ice_in_order.save()
            else:
                orde = Order.objects.create(worker_owner=request.user, status=1)
                # orde.ices_ordered.add(ice_in_order)
                # price_of_ice(request) todo
                ice_in_order.order.add(orde.id)
                ice_in_order.save()
                # orde.save()
            messages.success(request, "OrderItem Added to cart")
            return redirect("create-order")
        else:
            add_order_form = AddOrderItem()
            messages.info(request, "Wrong Data")
        return render(request, 'product_manager_ices/order_form.html', context={"add_order_form": add_order_form})

@login_required
def delete_orderitem(request,id=None):
    """
    Deleting orderitems in current order CART
    """
    if request.method == "POST":
        order_to_delete = OrderItem.objects.get(id=id)
        order_to_delete.delete()
    return redirect('create-order')

@login_required
def change_status_order_for_finish(request, id=None):
    """
    Change status of order to finished
    Boostrap Modal > buttons PAY>Finish
    """
    if request.method == "POST":
        order_to_change_status = Order.objects.get(id=id, worker_owner=request.user, status=1)
        order_to_change_status.status = 3
        order_to_change_status.save()
    return redirect('create-order')

@login_required
def postpone_order(request, id):
    """
    Postpone current order in CART
    button> POSTPONE
    """
    if request.method == "POST":
        order_to_change_status = Order.objects.get(id=id, worker_owner=request.user, status="1")
        order_to_change_status.status = 2
        order_to_change_status.save()
    return redirect('create-order')

@login_required
def return_order(request, id=None):
    """
    Change status of order form postpone to started
    List-of-orders button> return order to active
    Only the same user can return the order to active
    ONLY ONE ORDER CAN BE ACTIVE IN CART
    """
    if Order.objects.filter(worker_owner=request.user, status=1).exists():
        messages.info(request, "You have active order opened, Please postpone or delete it")
        return redirect('create-order')
    else:
        order_to_change_status = Order.objects.get(worker_owner=request.user, id=id)
        order_to_change_status.status = 1
        order_to_change_status.save()
        return redirect('create-order')


class OrderDelete(LoginRequiredMixin,DeleteView):
    """
    Deleting whole current order in CART
    """
    model = Order
    success_url = reverse_lazy("create-order")


class ListOfOrders(LoginRequiredMixin, ListView):

    """
    List of finished orders
    Search of orders,
    Only the same user can return the order to active
    """
    model = Order
    context_object_name = "orderlist"
    paginate_by = 7
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            queryset = Order.objects.filter(Q(worker_owner__username__icontains=query) |
                                            Q(time_sell__icontains=query)|
                                            Q(ices_ordered__flavour__flavour__icontains=query) |
                                            Q(ices_ordered__ice__type__contains=query)).order_by("-time_sell").distinct()
        else:
            queryset = Order.objects.filter(worker_owner=self.request.user).order_by("-time_sell")
        return queryset


class OrderDetail(UserPassesTestMixin,LoginRequiredMixin,DetailView):
    """
    Detail of every order
    Only owner of order can see the details.
    """
    model = Order
    def test_func(self):
        user = Order.objects.get(id=self.kwargs.get("pk"))
        return self.request.user.id == user.worker_owner.id
