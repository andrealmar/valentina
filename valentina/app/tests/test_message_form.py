from django.test import TestCase

from valentina.app.forms import MessageForm


class MessageFormTest(TestCase):

    def test_form_has_fields(self):
        form = MessageForm()
        self.assertSequenceEqual(list(form.fields), ['content', 'chat'])
