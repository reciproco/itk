# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from cuentas.forms import RegistrationForm
from cuentas.models import Profile
from django.utils import timezone
from cuentas.utils import generate_link, send_email


def register(request):
    if request.user.is_authenticated():
        return redirect('home')
    registration_form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            activation_key = generate_link(form.cleaned_data['username'])
            form.save(form.cleaned_data['username'],
                      form.cleaned_data['email'],
                      form.cleaned_data['password1'],
                      activation_key)

            send_email(request, activation_key, form.cleaned_data['email'],
                       'Enlace de activación de su cuenta en ' +
                       request.get_host())
            return redirect('home')
        else:
            registration_form = form  # Display form with error messages
    return render(request, 'cuentas/registro.html', locals())


# View called from activation email. Activate user if link didn'
# expire (48h default), or offer to
# send a second link if the first expired.
def activation(request, key):
    activation_expired = False
    already_active = False
    profil = get_object_or_404(Profile, activation_key=key)
    if profil.user.is_active is False:
        if timezone.now() > profil.key_expires:
            activation_expired is True
            id_user = profil.user.id
        else:  # Activation successful
            profil.user.is_active = True
            profil.user.save()

    # If user is already active, simply display error message
    else:
        already_active = True  # Display : error message
    return render(request, 'cuentas/activacion.html', locals())

# NO USO ESTA function
def new_activation_link(request, user_id):
    form = RegistrationForm()
    datas = {}
    user = User.objects.get(id=user_id)
    if user is not None and not user.is_active:
        datas['username'] = user.username
        datas['email'] = user.email
        datas['email_path'] = "/ResendEmail.txt"
        datas['email_subject'] = "Nouveau lien d'activation yourdomain"

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = datas['username']
        if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
        datas['activation_key'] = hashlib.sha1(salt+usernamesalt).hexdigest()

        profil = Profil.objects.get(user=user)
        profil.activation_key = datas['activation_key']
        profil.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profil.save()

        form.sendEmail(datas)
        request.session['new_link'] = True  # Display : new link send

    return redirect('/')
