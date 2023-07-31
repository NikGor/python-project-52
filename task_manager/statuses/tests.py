from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from task_manager.statuses.models import Status
from task_manager.users.models import User


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpass123'
        self.test_user = User.objects.create_user(username=self.username, password=self.password)
        self.test_status = Status.objects.create(name='teststatus')
        self.test_status.save()

    def test_create_status(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('statuses:status_create'), {
            'name': 'newstatus',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='newstatus').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно создан")

    def test_update_status(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('statuses:status_update', args=[self.test_status.id]), {
            'name': 'updatedstatus',
        })
        self.assertEqual(response.status_code, 302)
        self.test_status.refresh_from_db()
        self.assertEqual(self.test_status.name, 'updatedstatus')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно изменен")

    def test_delete_status(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('statuses:status_delete', args=[self.test_status.id]))
        self.assertEqual(response.status_code, 302)  # Проверяем, что произошел редирект
        self.assertFalse(Status.objects.filter(name='teststatus').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно удален")
