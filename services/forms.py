
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
        self.fields['picture'].error_messages = {
            'required': 'Seleccione una imagen del servicio',
            'invalid': 'Seleccione un archivo de imagen valido'
        }

    class Meta:
        model = Service
        fields = ('name', 'description', 'picture', 'moments', 'active')



