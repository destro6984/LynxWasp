from django import forms
from django.contrib import messages

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
            return redirect("homepage")
        if form_flavour.is_valid():
            form_flavour.save()
            messages.success(request, "Flavour Added")
            return redirect("homepage")
        else:
            form_type = AddIceForm()
            form_flavour = AddFlavourForm()
            messages.success(request, "Wrong Data")
        return render(request, 'product_manager_ices/add_ices.html', context={"form_type": form_type,
                                                                              "form_flavour": form_flavour, })


class IcesView(ListView):
    model = Ices

class CreateOrder(View):
    def get(self,request):
        # AddIceForm.base_fields['price'] = forms.ModelChoiceField(queryset=Price.objects.all())
        # AddIceForm.base_fields['type'] = forms.ModelChoiceField(queryset=Ices.objects.all())
        add_order_form=AddOrderItem()
        order_in_cart=Order.objects.get(worker_owner=request.user,finished=False)
        return render(request, 'product_manager_ices/order_form.html', context={"add_order_form": add_order_form,
                                                                                "order_in_cart":order_in_cart,
                                                                                })
    def post(self,request):
        add_order_form = AddOrderItem(request.POST)
        valid = add_order_form.is_valid()
        if valid:
            ice=add_order_form.cleaned_data.get('ice')
            quantity=add_order_form.cleaned_data.get('quantity')
            ice_in_order=OrderItem.objects.create(ice=ice,quantity=quantity)
            ice_in_order.flavour.set(request.POST.getlist('flavour')) #1 of thai  Flavouers:czekolada
            if Order.objects.filter(worker_owner=request.user,finished=False).exists():
                orde=Order.objects.get(worker_owner=request.user, finished=False)
                orde.ices_ordered.add(ice_in_order)
                orde.save()
            else:
                orde=Order.objects.create(worker_owner=request.user,finished=False,ices_ordered=ice_in_order)
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