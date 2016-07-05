from django.core.validators import validate_email, validate_slug
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from cuentas.models import Profile, MyUser
from datetime import datetime
from datetime import timedelta


class RegistrationForm(forms.Form):
    nombre = forms.CharField(label="", widget=forms.TextInput(
               attrs={'placeholder': 'Nombre',
                      'class': 'form-control input-perso'}),
               max_length=30, min_length=1)
    apellidos = forms.CharField(label="", widget=forms.TextInput(
               attrs={'placeholder': 'Apellidos',
                      'class': 'form-control input-perso'}),
               max_length=30, min_length=1,)
    provincia = forms.CharField(label="", widget=forms.TextInput(
               attrs={'placeholder': 'Provincia',
                      'class': 'form-control input-perso'}),
               max_length=30, min_length=1)
    localidad = forms.CharField(label="", widget=forms.TextInput(
               attrs={'placeholder': 'Localidad',
                      'class': 'form-control input-perso'}),
               max_length=30, min_length=1)
    centro_de_trabajo = forms.CharField(label="", widget=forms.TextInput(
               attrs={'placeholder': 'Centro de trabajo',
                      'class': 'form-control input-perso'}),
               max_length=30, min_length=3)

    email = forms.EmailField(label="", widget=forms.EmailInput(
               attrs={'placeholder': 'Correo electronico',
                      'class': 'form-control input-perso'}),
               max_length=100, validators=[validate_email])
    password1 = forms.CharField(label="", max_length=50, min_length=6,
                                widget=forms.PasswordInput(
                                  attrs={'placeholder': 'contraseña',
                                         'class': 'form-control input-perso'}))
    password2 = forms.CharField(label="", max_length=50, min_length=6,
                                widget=forms.PasswordInput(
                                  attrs={'placeholder': 'confirme contraseña',
                                         'class': 'form-control input-perso'}))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self.add_error('password2', "La contraseña no coincide")

        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=email).exists():
            self.add_error('email', 'Dirección de correo en uso.')

        return self.cleaned_data

    # Override of save method for saving both User and Profil objects
    def save(self, nombre, apellidos, localidad, provincia, centro_de_trabajo,
             email, password, activation_key):
        u = MyUser.objects.create_user(email, nombre, apellidos, provincia,
                                       localidad, centro_de_trabajo, password)
        u.is_active = False
        u.save()
        profile = Profile()
        profile.user = u
        profile.activation_key = activation_key
        profile.key_expires = datetime.strftime(datetime.now() +
                                                timedelta(days=2),
                                                "%Y-%m-%d %H:%M:%S")
        profile.save()
        return u


class ItkAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        # pdb.set_trace()
        if not user.is_active:
            raise forms.ValidationError(
                "Por favor active su cuenta usando \
                 el link que ha recibido en la dirección de correo \
                 que nos proporcionó.",
                code='inactive',
            )
