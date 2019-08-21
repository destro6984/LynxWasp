from django import forms
from django.contrib import messages

from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, CreateView
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
        order_in_cart=Order.objects.all()
        huj=OrderItem.objects.all()
        return render(request, 'product_manager_ices/order_form.html', context={"add_order_form": add_order_form,
                                                                                "order_in_cart":order_in_cart,
                                                                                "huj":huj})
    def post(self,request):
        add_order_form = AddOrderItem(request.POST)
        valid = add_order_form.is_valid()
        if valid:
            ice=add_order_form.cleaned_data.get('ice')
            quantity=add_order_form.cleaned_data.get('quantity')
            ice_in_order=OrderItem.objects.create(ice=ice,quantity=quantity)
            ice_in_order.flavour.set(request.POST.getlist('flavour'))
            ord=Order.objects.create()
            ord.ices_ordered.add(ice_in_order)
            messages.success(request, "Order Added")
            return redirect("create-order")
        else:
            add_order_form=AddOrderItem()
            messages.success(request, "Wrong Data")
        return render(request, 'product_manager_ices/order_form.html', context={"add_order_form": add_order_form})


