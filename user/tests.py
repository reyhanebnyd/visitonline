from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Appuser
import pyotp

class UserAuthViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.appuser = Appuser.objects.create(user=self.user, otp_secret=pyotp.random_base32())

    def test_signup_view_get(self):
        response = self.client.get(reverse('signup'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')  
    def test_signup_view_post_valid(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newuserpassword',
            'password2': 'newuserpassword',
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_view_post_invalid(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newuserpassword',
            'password2': 'differentpassword',
        })
        self.assertEqual(response.status_code, 200)  
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_get_username_view_get(self):
        response = self.client.get(reverse('get_username'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'get_username.html')  

    def test_get_username_view_post_valid(self):
        response = self.client.post(reverse('get_username'), {
            'username': 'testuser',
        })
        self.assertEqual(response.status_code, 302,msg="No redirect to OTP") 
        self.assertEqual(self.client.session['otp_username'], 'testuser')
        self.assertIn('otp_code', self.client.session,msg="Otp Not stored in session")

    def test_get_username_view_post_invalid(self):
        response = self.client.post(reverse('get_username'), {
            'username': 'invaliduser',
        })
        self.assertEqual(response.status_code, 200,msg="user vojod nadarad vali dakhel shode ast") 
        self.assertContains(response, 'Username does not exist')

    def test_otp_verify_view_get(self):
        response = self.client.get(reverse('otp_verify', kwargs={'username': 'testuser'}))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'otp_verify.html')  

    def test_otp_verify_view_post_valid(self):
        otp_code = self.appuser.generate_otp()
        self.client.session['otp_code'] = otp_code
        self.client.session['otp_username'] = 'testuser'
        self.client.save_session()

        response = self.client.post(reverse('otp_verify', kwargs={'username': 'testuser'}), {
            'otp_code': otp_code,
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_otp_verify_view_post_invalid(self):
        self.client.session['otp_code'] = '123456'
        self.client.session['otp_username'] = 'testuser'
        self.client.save_session()

        response = self.client.post(reverse('otp_verify', kwargs={'username': 'testuser'}), {
            'otp_code': 'invalid_otp',
        })
        self.assertEqual(response.status_code, 200,msg="in Error yani OK")
        self.assertContains(response, 'Invalid OTP')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

