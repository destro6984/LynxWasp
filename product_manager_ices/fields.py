from django.db import models
from django.forms import ModelChoiceField


class NamedModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.type.upper()


class TypeField(models.CharField):
    # always be using just lowercase
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value if value is None else value.lower()
