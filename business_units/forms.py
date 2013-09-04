from django import forms
from xindex.models import BusinessUnit

class AddBusinessUnit(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddBusinessUnit, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages = {
            'required': 'Ingrese un nombre para la unidad de negocio',
            'invalid': 'Ingrese un nombre valido'
        }
        self.fields['description'].error_messages = {
            'required': 'Ingrese una descripcion para la unidad de negocio',
            'invalid': 'Ingrese una descripcion valida'
        }

    class Meta:
        model = BusinessUnit
        fields = ('name', 'description', 'service', 'active')
