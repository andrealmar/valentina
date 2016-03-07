from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from valentina.app.models import Profile, Chat, Affiliation


class TestGetApp(TestCase):

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def setUp(self):
        self.credentials = dict(username='valentinavc', password='valentinavc')
        self.user = User.objects.create_user(**self.credentials)
        data = dict(user=self.user, gender=Profile.FEMALE, nickname='SrtaX')
        Profile.objects.create(**data)
        self.chat = Chat.objects.all().first()
        Affiliation.objects.create(chat=self.chat, user=self.user, alias='Tom')


class TestGetWithFemaleUserAuthenticated(TestGetApp):

    def setUp(self):
        super().setUp()
        self.login = self.client.login(**self.credentials)
        self.resp = self.client.get(resolve_url('app:welcome'))

    def test_get_for_female_user(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'app/home.html')

    def test_context(self):
        variables = ['chats', 'nickname']
        for key in variables:
            with self.subTest():
                self.assertIn(key, self.resp.context)

    def test_chats_attr(self):
        expected = '<li data-chat-url="'
        self.assertContains(self.resp, expected)

    def test_logout_link(self):
        url = resolve_url('app:logout')
        expected = 'href="{}"'.format(url)
        self.assertContains(self.resp, expected)


class TestGetAppWithMaleUser(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('stan', password='password')
        Profile.objects.create(gender=Profile.MALE, user=self.user)


class TestGetWithMaleUserAuthenticated(TestGetAppWithMaleUser):

    def test_get_for_male_user(self):
        self.client.login(username='stan', password='password')
        resp = self.client.get(resolve_url('app:welcome'))
        self.assertRedirects(resp, resolve_url('female_only'))

    def test_get_for_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='stan', password='password')
        resp = self.client.get(resolve_url('app:welcome'))
        self.assertEqual(200, resp.status_code)


class TestGetWithoutUserAuthenticated(TestGetApp):

    def setUp(self):
        super().setUp()
        self.client.login(username='stan', password='password')
        self.resp = self.client.get(resolve_url('app:welcome'))

    def test_get(self):
        home_url = resolve_url('home')
        app_url = resolve_url('app:welcome')
        expected = '{}?next={}'.format(home_url, app_url)
        self.assertRedirects(self.resp, expected)
