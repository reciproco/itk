from django.core.validators import validate_email, validate_slug
from django import forms
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from cuentas.models import Profile
from datetime import datetime
from datetime import timedelta


class RegistrationForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario', 'class':'form-control input-perso'}), max_length=30,min_length=3, validators=[validate_slug])
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'placeholder': 'Correo electronico','class':'form-control input-perso'}),max_length=100, validators=[validate_email])
    password1 = forms.CharField(label="",max_length=50,min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'contraseña','class':'form-control input-perso'}))
    password2 = forms.CharField(label="",max_length=50,min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'confirme contraseña','class':'form-control input-perso'}))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self.add_error('password2', "La contraseña no coincide")

        return self.cleaned_data

    # Override of save method for saving both User and Profil objects
    def save(self, datas):
        u = User.objects.create_user(datas['username'],
                                     datas['email'],
                                     datas['password1'])
        u.is_active = False
        u.save()
        profile = Profile()
        profile.user = u
        profile.activation_key = datas['activation_key']
        profile.key_expires = datetime.strftime(datetime.now() + timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()
        return u

    # Handling of activation email sending
    def sendEmail(self, datas):
        link = "http://localhost:9000/cuentas/activar/"+datas['activation_key']
#        c=Context({'activation_link':link,'username':datas['username']})
#        f = open(MEDIA_ROOT+datas['email_path'], 'r')
#        t = Template(f.read())
#        f.close()
#        message=t.render(c)
        message = 'prueba : ' + link
        # send_mail(datas['email_subject'], message, 'yourdomain <no-reply@yourdomain.com>', [datas['email']], fail_silently=False)
        email = EmailMessage(datas['email_subject'], link, to=[datas['email']])
        email.send()
