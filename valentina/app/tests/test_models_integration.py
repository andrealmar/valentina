from django.test import TestCase
from valentina.app.models import Profile, Chat, Affiliation, Message


class TestModelsIntegration(TestCase):

    fixtures = ['users.json', 'profiles.json', 'chats.json',
                'affiliations.json', 'messages.json']

    def test_objects_were_created(self):
        with self.subTest():
            self.assertEqual(2, Profile.objects.count())
            self.assertEqual(1, Chat.objects.count())
            self.assertEqual(2, Affiliation.objects.count())
            self.assertEqual(2, Message.objects.count())
