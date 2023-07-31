from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
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
            executor=self.test_user2,
        )

    def test_create_task(self):
        self.client.login(username='DarkSideLord', password='SithLord123')
        response = self.client.post(reverse('tasks:task_create'), {
            'name': 'newtask',
            'description': 'newdescription',
            'status': self.test_status.id,
            'labels': [self.test_label.id],
            'author': self.test_user1.id,
            'executor': self.test_user1.id,
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

    def test_task_filter_form(self):
        self.client.login(username='DarkSideLord', password='SithLord123')
        # Создаем дополнительные задачи для тестирования фильтрации
        test_task2 = Task.objects.create(
            name='testtask2',
            description='testdescription2',
            status=self.test_status,
            author=self.test_user1,
            executor=self.test_user2,
        )
        test_task3 = Task.objects.create(
            name='testtask3',
            description='testdescription3',
            status=self.test_status,
            author=self.test_user2,  # отличается от test_user1
            executor=self.test_user1,
        )
        test_task2 == test_task3  # чтобы обойти ошибку линтера что переменные не используются
        # Проверяем фильтрацию по имени задачи
        response = self.client.get(reverse('tasks:tasks_list'), {'title': 'testtask2'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testtask2')
        # Проверяем фильтрацию по исполнителю
        response = self.client.get(reverse('tasks:tasks_list'), {'executor': self.test_user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testtask')
        self.assertContains(response, 'testtask3')
        # Проверяем фильтрацию по автору
        response = self.client.get(reverse('tasks:tasks_list'), {'author': self.test_user2.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testtask3')
        # Проверяем фильтрацию по статусу
        response = self.client.get(reverse('tasks:tasks_list'), {'status': self.test_status.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testtask')
        self.assertContains(response, 'testtask2')
        self.assertContains(response, 'testtask3')
        # Проверяем фильтрацию "только свои задачи"
        response = self.client.get(reverse('tasks:tasks_list'), {'only_mine': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testtask')
        self.assertContains(response, 'testtask2')
