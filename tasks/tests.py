from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from tasks.models import Task
from users.models import User
from statuses.models import Status
from labels.models import Label
import logging

logger = logging.getLogger(__name__)


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user1 = User.objects.create_user(username='DarkSideLord', password='SithLord123')
        self.test_user2 = User.objects.create_user(username='CrazyHarley', password='Puddin123')
        self.test_status = Status.objects.create(name='teststatus')
        self.test_label = Label.objects.create(name='testlabel')
        self.test_task = Task.objects.create(
            name='testtask',
            description='testdescription',
            status=self.test_status,
            author=self.test_user1,
            assignee=self.test_user2,
        )

    def test_create_task(self):
        self.client.login(username='DarkSideLord', password='SithLord123')
        response = self.client.post(reverse('tasks:task_create'), {
            'name': 'newtask',
            'description': 'newdescription',
            'status': self.test_status.id,
            'labels': [self.test_label.id],
            'author': self.test_user1.id,
            'assignee': self.test_user1.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='newtask').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Задача успешно создана")

    def test_update_task(self):
        self.client.login(username='DarkSideLord', password='SithLord123')
        response = self.client.post(reverse('tasks:task_update', args=[self.test_task.id]), {
            'name': 'updatedtask',
            'description': 'updateddescription',
            'status': self.test_status.id,
            'labels': [self.test_label.id],
        })
        self.assertEqual(response.status_code, 302)
        self.test_task.refresh_from_db()
        self.assertEqual(self.test_task.name, 'updatedtask')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Задача успешно изменена")

    def test_delete_task(self):
        self.client.login(username='DarkSideLord', password='SithLord123')
        response = self.client.post(reverse('tasks:task_delete', args=[self.test_task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name='testtask').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Задача успешно удалена")

    def test_delete_task_by_other_user(self):
        self.client.login(username='CrazyHarley', password='Puddin123')
        response = self.client.post(reverse('tasks:task_delete', args=[self.test_task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='testtask').exists())
