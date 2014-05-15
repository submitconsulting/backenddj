# _*_ coding: utf-8 _*_
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from apps.params.models import Person, Locality, LocalityType 

class LocalityAddForm(ModelForm):
    name = forms.CharField(label=(u'Nombre de localidad *'),required=True, widget = forms.TextInput(attrs={'placeholder':'Name','class':'field text input-xlarge input-required mask-alphanum show-error','requiredx':'required'}))
    locality_type = forms.ModelChoiceField(queryset=LocalityType.objects.all(), required=True, label="Tipo")
    location = forms.CharField(widget = forms.TextInput(), label="Lugar", required=True)
    class Meta:
        model = Locality
        fields = ('name','locality_type','location',)
        #widgets={
        #        "name":forms.TextInput(attrs={'placeholder':'Name','class':'field text input-xlarge input-required mask-alphanum show-error','required':'required'}),
        #}
        def clean_name(self):
            namex = self.cleaned_data['name']
            raise forms.ValidationError("That name is already taken, please select another.")
            try:
                Locality.objects.get(name=namex)
            except Locality.DoesNotExist:
                return namex
            raise forms.ValidationError("That name is already taken, please select another.")

class LocalityEditForm(ModelForm):
    class Meta:
        model = Locality
        #Campos que se mostraran
        fields = ('name','locality_type','location',)
        # exclude = ('usuario', 'disponible',) <- Datos que se excluirán. Sirve de la misma manera las dos formas
        




# no usado, eliminar
class RegistrationForm(ModelForm):
    username = forms.CharField(label=(u'User Name'))
    email = forms.EmailField(label=(u'Email Address'))
    password = forms.CharField(label=(u'Password'),
                               widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label=(u'Verify Password'),
                                widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = Person
        exclude = ('user',)

        def clean_username(self):
            username = self.cleaned_data['username']
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return username
            raise forms.ValidationError("That username is already taken, please select another.")

        def clean(self):
            if self.cleaned_data['password'] != self.cleaned_data['password1']:
                raise forms.ValidationError("The passwords did not match.  Please try again.")
            return self.cleaned_data

