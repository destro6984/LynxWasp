from django.forms import forms, ModelForm

from product_manager_ices.models import Ices, Flavour


class AddIceForm(ModelForm):
    class Meta:
        model = Ices
        fields = '__all__'

class AddFlavourForm(ModelForm):
    class Meta:
        model=Flavour
        fields = '__all__'

