from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class RegistrationTests(TestCase):
    def test_login(self):
        """
        ログイン
        """
        response = self.client.get(reverse('registration:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ログイン')

        username = 'tester'
        password = 'llamapaca'
        user = User.objects.create_user(username, password=password)
        param = {'username': username, 'password': password}
        response = self.client.post(reverse('registration:login'), param, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ホーム')
        self.assertContains(response, 'ユーザー: ' + username)
        
    def test_signup(self):
        """
        ユーザー登録
        """
        response = self.client.get(reverse('registration:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ユーザー登録')

        username = 'tester'
        password = 'llamapaca'
        param = {'username': username, 'password1': password, 'password2': password}
        response = self.client.post(reverse('registration:signup'), param, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ホーム')
        self.assertContains(response, 'ユーザー: ' + username)



