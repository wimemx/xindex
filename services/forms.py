
from django import forms
from xindex.models import Service


class AddService(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddService, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages = {
            'required': 'Ingrese un nombre de servicio',
            'invalid': 'Ingrese un nombre valido de servicio'
        }
        self.fields['description'].error_messages = {
            'required': 'Ingrese una descripcion del servicio',
            'invalid': 'Ingrese una descripcion valida'
        }
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['moments'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Service
        fields = ('name', 'description', 'moments')



