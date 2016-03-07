from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from valentina.app.models import Profile


class TestProfile(TestCase):

    fixtures = ['users.json', 'profiles.json']

    def setUp(self):
        self.user = User.objects.create_user('valentinavc', password='valentinavc')
        Profile.objects.create(user=self.user, gender=Profile.FEMALE, nickname='fulana')

    def test_get_without_login(self):
        resp = self.client.get(resolve_url('app:profile'))
        self.assertEqual(302, resp.status_code)

    def test_get_with_login(self):
        self.login = self.client.login(username='valentinavc', password='valentinavc')
        resp = self.client.get(resolve_url('app:profile'))
        self.assertEqual(405, resp.status_code)

    def test_post_without_login(self):
        resp = self.client.post(resolve_url('app:profile'), {'nickname': 'ciclana'})
        user = User.objects.get(pk=self.user.pk)
        with self.subTest():
            self.assertEqual(302, resp.status_code)
            self.assertEqual('fulana', user.profile.nickname)

    def test_post_with_login(self):
        self.login = self.client.login(username='valentinavc', password='valentinavc')
        resp = self.client.post(resolve_url('app:profile'), {'nickname': 'ciclana'})
        user = User.objects.get(pk=self.user.pk)
        with self.subTest():
            self.assertEqual(200, resp.status_code)
            self.assertEqual('ciclana', user.profile.nickname)
