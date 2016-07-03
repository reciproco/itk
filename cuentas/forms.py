from django.core.validators import validate_email, validate_slug
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from cuentas.models import Profile
from datetime import datetime
from datetime import timedelta


class RegistrationForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(
               attrs={'placeholder': 'Nombre de usuario',
                      'class': 'form-control input-perso'}),
               max_length=30, min_length=3, validators=[validate_slug])
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

        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Nombre de usuario no disponible.')

        return self.cleaned_data

    # Override of save method for saving both User and Profil objects
    def save(self, username, email, password, activation_key):
        u = User.objects.create_user(username,
                                     email,
                                     password)
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
