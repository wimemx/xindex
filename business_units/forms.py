from django import forms
from xindex.models import BusinessUnit

class AddBusinessUnit(forms.ModelForm):
    class Meta:
        model = BusinessUnit
        fields = ('name', 'description', 'service')
