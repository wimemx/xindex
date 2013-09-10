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
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['service'].widget.attrs.update({'class': 'form-control'})




    class Meta:
        model = BusinessUnit
        fields = ('name', 'description', 'service')
