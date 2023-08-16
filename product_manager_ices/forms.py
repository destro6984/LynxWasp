from django import forms
from django.core.exceptions import ValidationError
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
    def __init__(self, *args, **kwargs):
        super(AddOrderItem, self).__init__(*args, **kwargs)
        msg = "OrdetItem must be made of type and flavour"

        self.fields["ice"].error_messages.update(
            {
                "required": msg,
            }
        )
        self.fields["flavour"].error_messages.update(
            {
                "required": msg,
            }
        )

    ice = NamedModelChoiceField(queryset=Ices.objects.all(), widget=forms.RadioSelect)
    flavour = forms.ModelMultipleChoiceField(
        queryset=Flavour.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    quantity = forms.IntegerField(min_value=1, initial=1)

    def clean(self):
        cleaned_data = super().clean()
        ice_type = cleaned_data.get("ice")
        flavours = cleaned_data.get("flavour", "")
        if (ice_type and ice_type.type == "thai") and len(flavours) > 2:
            raise ValidationError("Thai Ice cannot be mixed with more than 3 flavours")
