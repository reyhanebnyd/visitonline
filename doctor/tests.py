from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Doctor, Comment
from user.models import Appuser
import json

class DoctorViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin_user = User.objects.create_user(username='adminuser', password='12345')
        self.appuser = Appuser.objects.create(user=self.user, is_admin=False)
        self.admin_appuser = Appuser.objects.create(user=self.admin_user, is_admin=True)
        
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

    def test_add_doctor_view_get(self):
        self.client.login(username='adminuser', password='12345')
        response = self.client.get(reverse('adddoctor'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adddoctor.html')  

    def test_add_doctor_view_post(self):
        # Test POST request for add doctor view
        self.client.login(username='adminuser', password='12345')
        response = self.client.post(reverse('adddoctor'), {
            'name': 'New Doctor',
            'career': 'Pediatrician',
            'price': 150,
            'avg_visit_time': 20,
            'accessdate': '{"monday": ["09:00", "17:00"], "tuesday": ["09:00", "17:00"]}'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Doctor.objects.filter(name='New Doctor').exists())

    def test_delete_doctor_view_get(self):
        self.client.login(username='adminuser', password='12345')
        response = self.client.get(reverse('doctor-delete', kwargs={'pk': self.doctor.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/doctor_confirm_delete.html')  
    def test_delete_doctor_view_post(self):
        self.client.login(username='adminuser', password='12345')
        response = self.client.post(reverse('doctor-delete', kwargs={'pk': self.doctor.pk}))
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(Doctor.objects.filter(pk=self.doctor.pk).exists())

    def test_edit_doctor_view_get(self):
        # Test GET request for edit doctor view
        self.client.login(username='adminuser', password='12345')
        response = self.client.get(reverse('doctor-edited', kwargs={'pk': self.doctor.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'updated.html')  

    def test_edit_doctor_view_post(self):
        # Test POST request for edit doctor view
        self.client.login(username='adminuser', password='12345')
        response = self.client.post(reverse('doctor-edited', kwargs={'pk': self.doctor.pk}), {
            'name': 'Updated Doctor',
            'career': 'Dermatologist',
            'price': 120,
            'avg_visit_time': 25,
            'accessdate': '{"monday": ["09:00", "17:00"], "tuesday": ["09:00", "17:00"]}'
        })
        self.assertEqual(response.status_code, 302)  
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.name, 'Updated Doctor')

    def test_doctor_list_view_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('doctor-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor_list.html')  

    def test_doctor_detail_view_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('doctor-detail', kwargs={'pk': self.doctor.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor_detail.html')  

    def test_doctor_detail_view_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('doctor-detail', kwargs={'pk': self.doctor.pk}), {
            'content': 'Great doctor!'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Comment.objects.filter(doctor=self.doctor, content='Great doctor!').exists())
