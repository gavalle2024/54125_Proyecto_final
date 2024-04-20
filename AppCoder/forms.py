from django import forms
from .models import Avatar, Entregable
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User


class UserEditForm(UserChangeForm):
    email = forms.EmailField(label="Modificar")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repita Contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'password1', 'password2']
        help_text = {k: "" for k in fields}


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['imagen']  # Lista de campos que deseas incluir en el formulario

    def __init__(self, *args, **kwargs):
        super(AvatarForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].widget.attrs.update()  #({'class': 'form-control-file'})  # Añadir una clase CSS si es necesario


class Curso_formulario(forms.Form):
    nombre = forms.CharField(max_length=200)
    camada = forms.IntegerField()


class Alumno_formulario(forms.Form):
    apellido = forms.CharField(max_length=30)
    nombre = forms.CharField(max_length=40)
    fecha_nac = forms.DateField()
    dni = forms.IntegerField()
    mail = forms.EmailField()


class Profesor_formulario(forms.Form):
    apellido = forms.CharField(max_length=30)
    nombre = forms.CharField(max_length=40)
    mail = forms.EmailField()
    profesion = forms.CharField(max_length=100)


class Entregable_formulario(forms.Form):
    nombre = forms.CharField(max_length=200)
    fecha_entrega = forms.DateField()
    entregado = forms.BooleanField(required=False)

    class Meta:
        model = Entregable
        fields = ['nombre', 'fecha_entrega', 'entregado']
        # Asegura que 'entregado' no sea requerido
        field_classes = {'entregado': forms.BooleanField(required=False)}