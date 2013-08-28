
from django import forms
from xindex.models import Service




class AddService(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'description', 'picture', 'moments')



