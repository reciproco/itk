from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
import hashlib
import uuid


def generate_link(username):
    salt = uuid.uuid4().hex.encode('utf-8')
    return hashlib.sha1(salt + username.encode('utf-8')).hexdigest()


def send_email(request, activation_key, email, subject):
    link = "http://" + request.get_host() + \
           reverse('cuentas:activar', kwargs={'key': activation_key})
    email = EmailMessage(subject, link, to=[email])
    email.send()
