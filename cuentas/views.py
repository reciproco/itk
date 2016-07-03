# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from cuentas.forms import RegistrationForm
from cuentas.models import Profile
from django.utils import timezone
from cuentas.utils import generate_link, send_email
from datetime import datetime
from datetime import timedelta


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

# Untested
def new_activation_link(request, user_id):

    p = Profile.objects.get(user_id=user_id)
    if p.user is not None and not p.user.is_active:
        activation_key = generate_link(p.user.username)
        # profil = Profil.objects.get(user=user)
        p.activation_key = activation_key
        p.key_expires = datetime.strftime(
                              datetime.now() + timedelta(days=2),
                              "%Y-%m-%d %H:%M:%S")
        p.save()
        send_email(request, activation_key, p.user.email,
                   'NUEVO enlace de activación de su cuenta en ' +
                   request.get_host())

    return redirect('home')
