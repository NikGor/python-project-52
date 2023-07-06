from django.test import TestCase, Client
from django.urls import reverse
from .models import User


class UserCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.test_user.save()

    def test_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
        })
        self.assertEqual(response.status_code, 302)  # Проверяем, что произошел редирект
        self.assertTrue(User.objects.filter(username='newuser').exists())  # Проверяем, что пользователь создан

    def test_update_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('update_user', args=[self.test_user.id]), {
            'username': 'updateduser',
            'password1': 'updatedpassword',
            'password2': 'updatedpassword',
        })
        self.assertEqual(response.status_code, 302)  # Проверяем, что произошел редирект
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, 'updateduser')  # Проверяем, что имя пользователя обновлено

    def test_delete_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_user', args=[self.test_user.id]))
        self.assertEqual(response.status_code, 302)  # Проверяем, что произошел редирект
        self.assertFalse(User.objects.filter(username='testuser').exists())  # Проверяем, что пользователь удален
