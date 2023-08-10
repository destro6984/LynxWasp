from django.forms import ModelChoiceField


class NamedModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.type.upper()
