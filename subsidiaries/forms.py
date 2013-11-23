from django import forms
from xindex.models import Subsidiary
from xindex.models import Subsidiary_Type


class SubsidiaryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubsidiaryForm, self).__init__(*args, **kwargs)
        self.fields['company'].error_messages = {
            'required': 'Seleccione una compania',
            'invalid': 'Seleccione una compania valida'
        }
        self.fields['name'].error_messages = {
            'required': 'Ingrese un nombre'
        }

        self.fields['company'].widget.attrs.update(
            {
                'class': 'form-control'
            }
        )
        self.fields['name'].widget.attrs.update(
            {
                'class': 'bg-focus form-control',
                'placeholder': 'Nombre'
            }
        )
        self.fields['phone'].widget.attrs.update(
            {'class': 'form-control',
             'placeholder': 'Telefono'}
        )
        self.fields['rfc'].widget.attrs.update(
            {'class': 'form-control',
             'placeholder': 'RFC'}
        )
        self.fields['subsidiary_types'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control',
             'placeholder': 'Direccion'}
        )
        self.fields['country_id'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['state_id'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['city_id'].widget.attrs.update(
            {'class': 'form-control'}
        )

    class Meta:
        model = Subsidiary
        fields = ('company', 'name', 'phone', 'rfc', 'subsidiary_types',
                  'address', 'country_id', 'state_id', 'city_id')


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Subsidiary
        fields = ('company', 'name', 'subsidiary_types', 'zone')


class AddSubsidiaryType(forms.ModelForm):
    class Meta:
        model = Subsidiary_Type
        fields = ('name', 'description')