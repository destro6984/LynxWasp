from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.views.generic.base import View

from product_manager_ices.forms import AddIceForm, AddFlavourForm, AddOrderItem
from product_manager_ices.models import Ices, Order, OrderItem


class Homepage(View):
    def get(self, request):
        return render(request, 'Homepage.html')


class AddIce(View):
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


class IcesView(ListView):
    model = Ices

class CreateOrder(LoginRequiredMixin,View):
    def get(self,request):
        # AddIceForm.base_fields['price'] = forms.ModelChoiceField(queryset=Price.objects.all())
        # AddIceForm.base_fields['type'] = forms.ModelChoiceField(queryset=Ices.objects.all())
        add_order_form=AddOrderItem()
        try:
            order_in_cart=Order.objects.get(worker_owner=request.user,finished=False)
            sumarize = order_in_cart.get_total()
        except ObjectDoesNotExist:
            order_in_cart = None
            sumarize=None
        return render(request, 'product_manager_ices/order_form.html', context={"add_order_form": add_order_form,
                                                                                "order_in_cart":order_in_cart,
                                                                                "sumarize":sumarize,
                                                                                })
    def post(self,request):
        add_order_form = AddOrderItem(request.POST)
        valid = add_order_form.is_valid()
        if valid:
            ice=add_order_form.cleaned_data.get('ice')
            quantity=add_order_form.cleaned_data.get('quantity')
            ice_in_order=OrderItem.objects.create(ice_id=ice,quantity=quantity)
            ice_in_order.flavour.set(request.POST.getlist('flavour')) #1 of thai  Flavouers:czekolada
            if Order.objects.filter(worker_owner=request.user,finished=False).exists():
                orde=Order.objects.get(worker_owner=request.user, finished=False)
                orde.ices_ordered.add(ice_in_order)
                orde.save()
            else:
                orde=Order.objects.create(worker_owner=request.user,finished=False)
                orde.ices_ordered.add(ice_in_order)
                orde.save()
            messages.success(request, "OrderItem Added to cart")
            return redirect("create-order")
        else:
            add_order_form=AddOrderItem()
            messages.success(request, "Wrong Data")
        return render(request, 'product_manager_ices/order_form.html', context={"add_order_form": add_order_form})


def delete_orderitem(request,id=None):
    order_to_delete=OrderItem.objects.get(id=id)
    order_to_delete.delete()
    return redirect('create-order')

def change_status_order_for_finish(request,id=None):
    order_to_change_status=Order.objects.get(worker_owner=request.user,finished=False)
    order_to_change_status.finished=True
    order_to_change_status.save()
    return redirect('create-order')