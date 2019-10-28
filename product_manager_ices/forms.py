from django import forms
from django.forms import ModelForm

from product_manager_ices.models import Ices, Flavour, Order, OrderItem

class AddIceForm(ModelForm):
    class Meta:
        model = Ices
        fields = "__all__"
    widgets = {
        'type': forms.TextInput(attrs={'style': 'text-transform:lowercase'})
    }



class AddFlavourForm(ModelForm):
    class Meta:
        model=Flavour
        fields = '__all__'
        widgets = {
            'flavour': forms.TextInput(attrs={'style': 'text-transform:lowercase'})
        }

class AddOrderItem(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddOrderItem, self).__init__(*args, **kwargs)
        # this is to do not restart server to show the added flavour automatically
        self.fields['flavour'].choices = [(flav.id, flav.flavour) for flav in Flavour.objects.all()]
        # this is to do not restart server to show the added product automatically
        self.fields['ice'].choices = [(typeice.id, typeice.type) for typeice in Ices.objects.all()]

    # type_ice = [(type_ice.id, Ices.objects.filter(id=type_ice.id)) for type_ice in Ices.objects.all()]
    ice = forms.ChoiceField(widget=forms.RadioSelect)
    flavour = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    quantity= forms.IntegerField(min_value=1,initial=1)


