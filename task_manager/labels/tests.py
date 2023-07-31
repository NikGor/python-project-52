from django.contrib.messages import get_messages
from django.urls import reverse
from django.test import TestCase, Client
from task_manager.labels.models import Label
from task_manager.users.models import User


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_label = Label.objects.create(name='testlabel')
        self.username = 'DarkSideLord'
        self.password = 'SithLord123'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_create_label(self):
        response = self.client.post(reverse('labels:label_create'), {'name': 'newlabel'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='newlabel').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно создана")

    def test_update_label(self):
        response = self.client.post(reverse('labels:label_update',
                                            kwargs={'pk': self.test_label.pk}),
                                    {'name': 'updatedlabel'})
        self.assertEqual(response.status_code, 302)
        self.test_label.refresh_from_db()
        self.assertEqual(self.test_label.name, 'updatedlabel')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно изменена")

    def test_delete_label(self):
        # Если есть связанные задачи, проверьте сообщение об ошибке
        if self.test_label.tasks.exists():
            response = self.client.post(reverse('labels:label_delete',
                                                kwargs={'pk': self.test_label.pk}),
                                        follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(Label.objects.filter(name='testlabel').exists())
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(str(messages[0]), "Невозможно удалить метку, связанную с задачами.")
        else:
            # Если связанных задач нет, проверьте успешное удаление
            response = self.client.post(reverse('labels:label_delete',
                                                kwargs={'pk': self.test_label.pk}),
                                        follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(Label.objects.filter(name='testlabel').exists())
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(str(messages[0]), "Метка успешно удалена")
