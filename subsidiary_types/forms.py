from django import forms
from xindex.models import Subsidiary_Type


class AddSubsidiaryType(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddSubsidiaryType, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages = {
            'required': 'Ingrese un nombre',
            'invalid': 'Ingrese un nombre valido'
        }
        self.fields['description'].error_messages = {
            'required': 'Ingrese una descripcion para el tipo de sucursal',
            'invalid': 'Ingrese una descripcion valida'
        }

        self.fields['name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class' : 'form-control'})

    class Meta:
        model = Subsidiary_Type
        fields = ('name', 'description')
