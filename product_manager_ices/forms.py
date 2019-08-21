from django import forms
from django.forms import ModelForm

from product_manager_ices.models import Ices, Flavour, Order, OrderItem


class AddIceForm(ModelForm):


    class Meta:
        model = Ices
        fields = "__all__"


class AddFlavourForm(ModelForm):

    class Meta:
        model=Flavour
        fields = '__all__'

class AddOrderItem(forms.Form):
    flavoures = [(flav.id, flav.flavour) for flav in Flavour.objects.all()]
    type_ice = [(type_ice.id, Ices.objects.filter(id=type_ice.id)) for type_ice in Ices.objects.all()]
    ice = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=Ices.objects.all())
    flavour = forms.MultipleChoiceField(choices=flavoures, widget=forms.CheckboxSelectMultiple)
    quantity= forms.IntegerField(min_value=1)