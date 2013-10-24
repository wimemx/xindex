__author__ = 'osvaldo'

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

        self.fields['company'].widget.attrs.update({'class' : 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'bg-focus form-control', 'placeholder': 'Nombre'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Telefono'})
        self.fields['rfc'].widget.attrs.update({'class': 'form-control', 'placeholder': 'RFC'})
        self.fields['subsidiary_types'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Direccion'})
        self.fields['country_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['state_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['city_id'].widget.attrs.update({'class': 'form-control'})

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



"""
class NuevaSubsidiaria(forms.Form):

    STATUS = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    )

    company = forms.ModelChoiceField(
        queryset=c.objects.all(),
        widget=Select, empty_label=None, required=True, error_messages={'required':'Seleccione un valor'}
    )

    name = forms.CharField(max_length=100)
    status = forms.Select(choices=STATUS)
    subsidiary_type = forms.ModelChoiceField(
        queryset=Subsidiary_Type.objects.all(),
        widget=Select, empty_label=None, required=True,
        error_messages={
            'required':'Seleccione un tipo de subsidiaria',
            'invalid':'Seleccione un tipo de subsidiaria'
        }
    )

    business_unit = forms.ModelChoiceField(
        queryset=BusinessUnit.objects.all(),
        widget=Select, empty_label=None, required=True,
        error_messages={
            'required': 'Seleccione una unidad de negocio',
            'invalid': 'Seleccione una unidad de negocio'
        }
    )

    zone = forms.ModelChoiceField(
        queryset=Zone.objects.all(),
        widget=Select, empty_label=None, required=True,
        error_messages={
            'required':'Seleccione una zona',
            'invalid':'Seleccione una zona'
        }
    )

    date = forms.DateField()
    meta = forms.TextField(blank=True, null=True)


class new_one(forms.ModelForm):
    class Meta:
        model = Subsidiary

"""