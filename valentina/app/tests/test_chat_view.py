from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from valentina.app.models import Profile, Chat, Affiliation, Message


class TestGetWithoutLogin(TestCase):

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def setUp(self):
        self.chat = Chat.objects.all().first()
        self.resp = self.client.get(resolve_url('app:chat', self.chat.pk))

    def test_get_without_login(self):
        home_url = resolve_url('home')
        chat_url = resolve_url('app:chat', self.chat.pk)
        expected = '{}?next={}'.format(home_url, chat_url)
        self.assertRedirects(self.resp, expected)


class TestGetWithLogin(TestCase):

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def setUp(self):

        # create user with password and affiliate her to a chatroom
        user = User.objects.create_user('valentinavc', password='valentina')
        self.chat = Chat.objects.all().first()
        Profile.objects.create(user=user, gender=Profile.FEMALE)
        Affiliation.objects.create(chat=self.chat, user=user, alias='Geek')

        # login and GET
        self.login = self.client.login(username='valentinavc',
                                       password='valentina')
        self.resp = self.client.get(resolve_url('app:chat', self.chat.pk))

    def test_get_with_login(self):
        with self.subTest():
            self.assertTrue(self.login)
            self.assertEqual(200, self.resp.status_code)

    def test_type(self):
        self.assertEqual('application/json', self.resp['Content-Type'])

    def test_contents(self):
        json_resp = self.resp.json()
        with self.subTest():
            self.assertEqual(json_resp['chat']['id'], self.chat.pk)
            self.assertEqual(json_resp['chat']['alias'], 'Geek')
            self.assertEqual(2, len(json_resp['messages']))


class TestPostWithoutLogin(TestCase):

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def setUp(self):
        self.chat = Chat.objects.all().first()
        data = {'content': 'Hello, world', 'chat': self.chat.pk}
        self.resp = self.client.post(resolve_url('app:chat', self.chat.pk), data)

    def test_post_without_login(self):
        home_url = resolve_url('home')
        chat_url = resolve_url('app:chat', self.chat.pk)
        expected = '{}?next={}'.format(home_url, chat_url)
        self.assertRedirects(self.resp, expected)


class TestPostWithLogin(TestCase):

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def setUp(self):

        # create user with password and affiliate her to a chatroom
        self.user = User.objects.create_user('valentinavc', password='valentina')
        self.chat = Chat.objects.all().first()
        Profile.objects.create(user=self.user, gender=Profile.FEMALE, nickname='valanon')
        Affiliation.objects.create(chat=self.chat, user=self.user, alias='Geek')

        # login and POST
        self.login = self.client.login(username='valentinavc',
                                       password='valentina')
        data = {'content': 'Hello, world', 'chat': self.chat.pk}
        self.resp = self.client.post(resolve_url('app:chat', self.chat.pk), data)

    def test_get_with_login(self):
        with self.subTest():
            self.assertTrue(self.login)
            self.assertEqual(201, self.resp.status_code)

    def test_type(self):
        self.assertEqual('application/json', self.resp['Content-Type'])

    def test_contents(self):
        json_resp = self.resp.json()
        with self.subTest():
            self.assertEqual(json_resp['content'], 'Hello, world')
            self.assertEqual(json_resp['ago'], 'agora')
            self.assertEqual(json_resp['author'], 'valanon')
            self.assertEqual(json_resp['className'], 'me')

    def test_message_count_increased(self):
        self.assertEqual(3, Message.objects.filter(chat=self.chat).count())
