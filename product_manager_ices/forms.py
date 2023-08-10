from django import forms
from django.forms import ModelForm

from product_manager_ices.fields import NamedModelChoiceField
from product_manager_ices.models import Flavour, Ices


class AddIceForm(ModelForm):
    class Meta:
        model = Ices
        fields = "__all__"

    widgets = {"type": forms.TextInput(attrs={"style": "text-transform:lowercase"})}


class AddFlavourForm(ModelForm):
    class Meta:
        model = Flavour
        fields = "__all__"
        widgets = {
            "flavour": forms.TextInput(attrs={"style": "text-transform:lowercase"})
        }


class AddOrderItem(forms.Form):
    ice = NamedModelChoiceField(queryset=Ices.objects.all(), widget=forms.RadioSelect)
    flavour = forms.ModelMultipleChoiceField(
        queryset=Flavour.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    quantity = forms.IntegerField(min_value=1, initial=1)
