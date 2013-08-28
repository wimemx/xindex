from django import forms
from xindex.models import Subsidiary_Type

class AddSubsidiaryType(forms.ModelForm):
    class Meta:
        model = Subsidiary_Type
        fields = ('name', 'description')
