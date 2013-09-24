from django import forms
from xindex.models import BusinessUnit
from xindex.models import Subsidiary


class AddBusinessUnit(forms.ModelForm):

    subsidiaries = forms.ModelMultipleChoiceField(
        queryset=Subsidiary.objects.all().filter(active=True),
        label="Subsidiarias",
        widget=forms.SelectMultiple,
        required=True)

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
        self.fields['subsidiaries'].error_messages = {
            'required': 'Seleccione la sucursal a asociar',
            'invalid': 'Seleccione una sucursal valida'
        }
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['service'].widget.attrs.update({'class': 'form-control'})
        self.fields['subsidiaries'].widget.attrs.update(
            {'class': 'form-control'})

    class Meta:
        model = BusinessUnit
        fields = ('name', 'description', 'service')
