from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from doctor.models import Doctor, Fulltimes
from wallet.models import Wallet
from user.models import Appuser
from datetime import datetime
from django.utils import timezone
import json
class PaymentViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.appuser = Appuser.objects.create(user=self.user)
        self.doctor = Doctor.objects.create(
            name='Test Doctor',
            career='General',
            price=100,
            avg_visit_time=30,
            accessdate=json.dumps({
                'monday': ['09:00', '17:00'],
                'tuesday': ['09:00', '17:00'],
            })
        )
        self.wallet = Wallet.objects.create(uid=self.appuser, balance=200)
    def test_payment_view_get_no_existing_reservation(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('payment'), {
            'slot': '2024-09-17T10:00:00',
            'doctor_id': self.doctor.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment.html')
    def test_payment_view_get_existing_reservation(self):
        Fulltimes.objects.create(id_U=self.appuser, id_D=self.doctor, accessdate=datetime.now())

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('payment'), {
            'slot': '2024-09-17T10:00:00',
            'doctor_id': self.doctor.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'already_reserved.html')
    def test_payment_view_post_successful_payment(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('payment_view'), {
            'slot': '2024-09-17T10:00:00',
            'doctor_id': self.doctor.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')        
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 100)
        self.assertTrue(Fulltimes.objects.filter(id_U=self.appuser, id_D=self.doctor).exists())
    def test_payment_view_post_insufficient_balance(self):
        self.wallet.balance = 50
        self.wallet.save()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('payment_view'), {
            'slot': '2024-09-17T10:00:00',
            'doctor_id': self.doctor.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fail.html')
        self.assertIn('Insufficient balance', response.content.decode())        
        self.assertFalse(Fulltimes.objects.filter(id_U=self.appuser, id_D=self.doctor).exists())
class CancelReservationViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.appuser = Appuser.objects.create(user=self.user)
        self.doctor = Doctor.objects.create(name='Test Doctor', price=100)
        self.wallet = Wallet.objects.create(uid=self.appuser, balance=0)
        self.reservation = Fulltimes.objects.create(id_U=self.appuser, id_D=self.doctor, accessdate=datetime.now())

    def test_cancel_reservation(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('cancel_reservation', kwargs={'reservation_id': self.reservation.id}))
        self.assertEqual(response.status_code, 302)
        
        self.assertFalse(Fulltimes.objects.filter(id=self.reservation.id).exists())
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 100)

class WalletDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.appuser = Appuser.objects.create(user=self.user)
        self.wallet = Wallet.objects.create(uid=self.appuser, balance=200)

    def test_wallet_detail_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('wallet_detail'))  # Replace 'wallet_detail' with the actual URL name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet_detail.html')
        self.assertContains(response, '200')  # Check if balance is displayed

class AddBalanceViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.appuser = Appuser.objects.create(user=self.user)
        self.wallet = Wallet.objects.create(uid=self.appuser, balance=200)

    def test_add_balance_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_balance'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_balance.html')

    def test_add_balance_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_balance'), {
            'amount': 50
        })
        self.assertEqual(response.status_code, 302)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 250)

class ReservationsPageViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.appuser = Appuser.objects.create(user=self.user)
        self.doctor = Doctor.objects.create(name='Test Doctor')
        self.reservation = Fulltimes.objects.create(id_U=self.appuser, id_D=self.doctor, accessdate=datetime.now())

    def test_reservations_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('reservations'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations.html')
        self.assertContains(response, 'Test Doctor')
