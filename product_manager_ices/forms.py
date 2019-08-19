from django import forms
from django.forms import ModelForm

from product_manager_ices.models import Ices, Flavour, Order


class AddIceForm(ModelForm):
    flavoures = [(flav.id, flav.flavour) for flav in Flavour.objects.all()]
    type_ice = [(type_ice.id, type_ice.type) for type_ice in Ices.objects.all()]
    type = forms.MultipleChoiceField(choices=type_ice, widget=forms.CheckboxSelectMultiple)
    flavour_type = forms.MultipleChoiceField(choices=flavoures, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Ices
        fields = ['type']
        # widgets ={'type': forms.SelectMultiple()}

class AddFlavourForm(ModelForm):
    flavoures=[(flav.id, flav.flavour) for flav in Flavour.objects.all()]
    flavour = forms.MultipleChoiceField(choices=flavoures, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model=Flavour
        fields = '__all__'

class AddOrder(ModelForm):
    class Meta:
        model=Order
        fields = '__all__'