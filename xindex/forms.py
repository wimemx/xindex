from django.forms import ModelForm, Form
from django.forms.widgets import CheckboxSelectMultiple, Textarea
from django import forms
from xindex.models import Company, Company_Type, Zone,Country, State, City, Moment, Attribute, Owner, Indicator
import datetime


class MomentForm(ModelForm):

    name = forms.CharField(label="Name:")
    attributes = forms.ModelMultipleChoiceField(queryset=Attribute.objects.all(),
        label="Attribute:",
        widget=forms.CheckboxSelectMultiple,
        required=False)

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


class AttributeForm(ModelForm):

    name = forms.CharField(label="Name:")

    class Meta:
        model = Attribute
        fields = ('name', 'description')
        exclude = ('date', 'meta')


class IndicatorForm(ModelForm):
    name = forms.CharField(label="Name:")
    attributes = forms.ModelMultipleChoiceField(queryset=Attribute.objects.all(),
        label="Attribute:",
        widget=forms.CheckboxSelectMultiple,
        required=False)


    class Meta:
        model = Indicator
        fields = ('name', 'description', 'type', 'min_value','max_value','threshold','weight', 'attributes','questions','active')
        exclude = ('date', 'meta')


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


'''

class CompanyForm(Form):

    STATUS = (('Active', 'Active'),
              ('Inactive', 'Inactive'))

    name = forms.CharField(label="Name:")

    types = forms.ModelMultipleChoiceField(queryset=Company_Type.objects.all(),
                                   label="Types:",
                                   widget=forms.Select)

    parent_company = forms.ModelChoiceField(queryset=Company.objects.all(),
                                                widget=forms.Select,
                                                empty_label="Select",
                                                label="Parent company")

    about = forms.CharField(label="About", widget=forms.Textarea)
    address = forms.CharField(label="Address:")
    rfc = forms.CharField(label="RFC:")
    phone = forms.CharField(label="Phone:")
    status = forms.ChoiceField(label="Status:", choices=STATUS)
    zone = forms.ModelMultipleChoiceField(queryset=Zone.objects.all(), label="Zone",
                                      widget=forms.Select)

    class Meta:
        model = Company
'''