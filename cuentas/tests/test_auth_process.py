from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from cuentas.forms import RegistrationForm
from cuentas.models import Profile
import pdb


class AuthTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.form_data = {'nombre': 'prueba',
                          'apellidos': 'prueba',
                          'localidad': 'madir',
                          'provincia': 'provincia',
                          'centro_de_trabajo': 'prueba',
                          'email': 'reciprocidad@gmail.com',
                          'password1': 'peloto', 'password2': 'peloto'}

    def test_registro_endpoint(self):
        response = self.client.get(reverse('cuentas:registro'))
        self.assertEqual(response.status_code, 200)

    def test_registro_valid_form(self):
        # form_data = {'username': 'prueba', 'email': 'reciprocidad@gmail.com',
        #             'password1': 'peloto', 'password2': 'peloto'}

        form = RegistrationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_registro_invalid_email(self):
        form_data = {'nombre': 'prueba',
                     'apellidos': 'prueba',
                     'localidad': 'madir',
                     'provincia': 'provincia',
                     'centro_de_trabajo': 'prueba',
                     'email': 'reciprocidad_gmail.com',
                     'password1': 'peloto', 'password2': 'peloto'}
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_registro(self):
        response = self.client.post(reverse('cuentas:registro'),
                                    self.form_data)
        self.assertRedirects(response, reverse('home'))

    def test_resgitro_unavailable_username(self):
        self.test_registro()
        response = self.client.post(reverse('cuentas:registro'),
                                    self.form_data)
        # pdb.set_trace()
        self.assertContains(response, 'de correo en uso.')

    def test_login_without_activation(self):
        self.test_registro()

        form_data = {'username': 'reciprocidad@gmail.com',
                     'password': 'peloto'}
        response = self.client.post(reverse('cuentas:login'), form_data)
        # self.assertEqual(response.status_code, 200)

        # pdb.set_trace()
        self.assertContains(response, 'active su cuenta usando')
        # self.assertIn('_auth_user_id', self.client.session)

    def test_login_with_activation(self):
        self.test_registro()
        p = Profile.objects.get(user_id=1)
        response = self.client.get(
                   reverse('cuentas:activar',
                           kwargs={'key': p.activation_key}))
        form_data = {'username': 'reciprocidad@gmail.com',
                     'password': 'peloto'}
        response = self.client.post(reverse('cuentas:login'), form_data)
        # self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)
