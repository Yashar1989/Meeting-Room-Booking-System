from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from user.models import CustomUser
from .forms import OTPLoginForm
from .views import register, login_user, profile, edit, send_otp, verify_otp


class TestUrl(SimpleTestCase):
    def test_register_url(self):
        url = reverse('account:register')
        self.assertEqual(resolve(url).func, register)

    def test_login_url(self):
        url = reverse('account:login')
        self.assertEqual(resolve(url).func, login_user)

    def test_profile_url(self):
        url = reverse('account:profile')
        self.assertEqual(resolve(url).func, profile)

    def test_edit_profile_url(self):
        url = reverse('account:edit')
        self.assertEqual(resolve(url).func, edit)

    def test_send_otp_url(self):
        url = reverse('account:send_otp')
        self.assertEqual(resolve(url).func, send_otp)

    def test_verify_otp_url(self):
        url = reverse('account:verify_otp')
        self.assertEqual(resolve(url).func, verify_otp)


class UserFormTest(TestCase):

    def test_otp_form_with_not_valid_data(self):
        form = OTPLoginForm(data={})
        self.assertFalse(form.is_valid())

    def test_otp_form_with_valid_data(self):
        form = OTPLoginForm(data={
            'otp': 1111
        })
        self.assertTrue(form.is_valid())

    def test_create_user(self):
        user = CustomUser.objects.create(
            username='admin',
            email='admin@admin.com',
            password='!@#qazWSX'
        )
        user2 = CustomUser.objects.create(
            username='hesam',
            email='hesam@admin.com',
            password='123456'
        )
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user2.email, 'hesam@admin.com')


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')

    def test_login_view(self):
        response = self.client.post(reverse('account:login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:profile'))

    def test_invalid_login(self):
        response = self.client.post(reverse('account:login'),
                                    {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)


class TestCustomUserModel(TestCase):

    def test_create_user_with_profile(self):
        user = CustomUser.objects.create_user(username='erfan', password='!@#WSXqaz')
        self.assertEqual(user.username, 'erfan')
        self.assertEqual(user.profile.user_id, user.id)

