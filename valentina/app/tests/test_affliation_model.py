from django.contrib.auth.models import User
from django.test import TestCase
from valentina.app.models import Affiliation, Chat


class TestAffiliationModel(TestCase):

    def setUp(self):
        self.chat = Chat.objects.create(person='42')
        self.user = User.objects.create_user(username='olivia')

    def test_create(self):
        Affiliation.objects.create(chat=self.chat, user=self.user,
                                   alias='johndoe')
        self.assertTrue(Affiliation.objects.exists())
