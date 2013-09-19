from django.forms import ModelForm, Form
from django.forms.widgets import CheckboxSelectMultiple, Textarea
from django import forms
from xindex.models import Company, Company_Type, Zone, Country, State, City, \
    Moment, Attributes, Owner, Survey, Xindex_User, Question
import datetime


class MomentForm(ModelForm):

    name = forms.CharField(label="Name:")
    """
    attributes = forms.ModelMultipleChoiceField(queryset=Attributes.objects.all(),
        label="Attribute:",
        widget=forms.CheckboxSelectMultiple,
        required=False)
    """
    def __init__(self, *args, **kwargs):
        super(MomentForm, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages = {
            'required': 'Ingrese un nombre',
            'invalid': 'Ingrese un nombre valido'
        }
        self.fields['description'].error_messages = {
            'required': 'Ingrese una descripcion',
            'invalid': 'Ingrese una descripcion valida'
        }
        self.fields['owners'].error_messages = {
            'required': 'Seleccione un propietario',
            'invalid': 'Seleccione un propietario valido'
        }

        self.fields['name'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['attributes'].widget.attrs.update({'class': 'form-control'})
        self.fields['owners'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Moment
        fields = ('name', 'description', 'attributes', 'owners')
        exclude = ('date','meta',)


class OwnerForm(ModelForm):

    name = forms.CharField(label="Name:")

    class Meta:
        model = Owner
        fields = ('name', 'type', 'subsidiary')
        exclude = ('date','meta')


class AttributesForm(ModelForm):
    name = forms.CharField(label="Name:")
    moments = forms.ModelMultipleChoiceField(
        queryset=Moment.objects.all().filter(active=True),
        label="Momentos",
        widget=forms.SelectMultiple,
        required=True)

    def __init__(self, *args, **kwargs):
        super(AttributesForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['threshold'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['moments'].widget.attrs.update({'class': 'form-control', 'required': 'required'})

    class Meta:
        model = Attributes
        fields = ('name', 'description', 'threshold')
        exclude = ('active', 'date', 'meta')


class CompanyForm(ModelForm):

    name = forms.CharField(label="Name:")
    types = forms.ModelMultipleChoiceField(
        queryset=Company_Type.objects.all().filter(active=True),
        label="Types:",
        widget=forms.CheckboxSelectMultiple,
        required=False)
    zone = forms.ModelMultipleChoiceField(
        queryset=Zone.objects.all().filter(active=True),
        label="Zone",
        widget=forms.CheckboxSelectMultiple,
        required=False)

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages = {
            'required': 'Ingrese un nombre',
            'invalid': 'Ingrese un nombre valido'
        }
        self.fields['address'].error_messages = {
            'required': 'Ingrese la direccion de la compania',
            'invalid': 'Ingrese una direccion valida'
        }
        self.fields['rfc'].error_messages = {
            'required': 'Ingrese el RFC de la compania',
            'invalid': 'Ingrese un RFC valido'
        }
        self.fields['phone'].error_messages = {
            'required': 'Ingrese el numero de telefono',
            'invalid': 'Ingrese un numero de telefono valido'
        }

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['types'].widget.attrs.update({'class': 'form-control'})
        self.fields['parent_company'].widget.attrs.update({'class': 'form-control'})
        self.fields['about'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['rfc'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['staff'].widget.attrs.update({'class': 'form-control'})
        self.fields['zone'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Company
        fields = ('name', 'types', 'parent_company', 'about', 'address', 'rfc',
                  'phone', 'staff', 'zone')
        exclude = ('date', 'meta', 'active')


class ZoneForm(ModelForm):

    countries = forms.ModelMultipleChoiceField(
        queryset=Country.objects.all().filter(active=True),
        label="Country",
        widget=forms.CheckboxSelectMultiple,
        required=False)
    states = forms.ModelMultipleChoiceField(
        queryset=State.objects.all().filter(active=True),
        label="State",
        widget=forms.CheckboxSelectMultiple,
        required=False)
    cities = forms.ModelMultipleChoiceField(
        queryset=City.objects.all().filter(active=True),
        label="City",
        widget=forms.CheckboxSelectMultiple,
        required=False)
    description = forms.CharField(label="Description", widget=Textarea)

    class Meta:
        model = Zone
        fields = ('name', 'countries', 'states', 'cities', 'description',
                  'parent_zone')
        exclude = ('date', 'meta', 'active')


class CompanyTypeForm(ModelForm):

    name = forms.CharField(label="Name:")
    description = forms.CharField(label="Description:", widget=Textarea,
                                  required=False)

    class Meta:
        model = Company_Type
        fields = ('name', 'description')
        exclude = ('date', 'meta', 'active')


class SurveyForm(ModelForm):

    user_id = forms.ModelChoiceField(
        queryset=Xindex_User.objects.all(),
        label="User",
        widget=forms.Select,
        empty_label="Select")
    name = forms.CharField(label="Name:")
    description = forms.CharField(
        label="Description:", widget=Textarea,
        required=False)
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().filter(active=True),
        label="Questions",
        widget=forms.Select)

    class Meta:
        model = Survey
