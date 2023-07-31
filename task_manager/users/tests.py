from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import User
from django.contrib.messages import get_messages


class UserCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='DarkSideLord', password='SithLord123')

    def test_register(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'DogeToTheMoon',
            'password1': 'SuchPassword123',
            'password2': 'SuchPassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='DogeToTheMoon').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Пользователь успешно зарегистрирован")

    def test_update_user(self):
        self.client.login(username='DarkSideLord', password='SithLord123')
        response = self.client.post(reverse('users:update_user', args=[self.test_user.id]), {
            'username': 'DarthVader',
            'first_name': 'Anakin',
            'last_name': 'Skywalker',
            'password1': 'NewSithLord123',
            'password2': 'NewSithLord123'
        })
        self.assertEqual(response.status_code, 302)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, 'DarthVader')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Пользователь успешно изменен")

    def test_update_other_user(self):
        other_user = User.objects.create_user(username='OtherUser', password='OtherUser123')
        self.client.login(username='DarkSideLord', password='SithLord123')
        response = self.client.post(reverse('users:update_user', args=[other_user.id]), {
            'username': 'CrazyHarley',
            'first_name': 'Харли',
            'last_name': 'Квинн',
            'password1': 'Puddin123',
            'password2': 'Puddin123'
        })
        self.assertEqual(response.status_code, 302)
        other_user.refresh_from_db()
        self.assertNotEqual(other_user.username, 'NewUsername')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "У вас нет прав для изменения другого пользователя.")

    def test_delete_other_user(self):
        other_user = User.objects.create_user(username='OtherUser', password='OtherUser123')
        self.client.login(username='DarkSideLord', password='SithLord123')
        response = self.client.post(reverse('users:delete_user', args=[other_user.id]), {
            'username': 'CrazyHarley',
            'first_name': 'Харли',
            'last_name': 'Квинн',
            'password1': 'Puddin123',
            'password2': 'Puddin123'
        })
        self.assertEqual(response.status_code, 302)
        other_user.refresh_from_db()
        self.assertNotEqual(other_user.username, 'NewUsername')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "У вас нет прав для изменения другого пользователя.")

    def test_delete_user(self):
        self.client.login(username='DarkSideLord', password='SithLord123')
        response = self.client.post(reverse('users:delete_user', args=[self.test_user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(
            username='DarkSideLord').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Пользователь успешно удален")

    def test_login(self):
        username = "CrazyHarley"
        password = "Puddin123"
        User.objects.create_user(username=username, password=password)
        response = self.client.post(reverse('login'), {
            'username': username,
            'password': password,
        })
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Вы залогинены")

    def test_logout(self):
        self.client.login(username=self.test_user.username, password='SithLord123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Вы разлогинены")
