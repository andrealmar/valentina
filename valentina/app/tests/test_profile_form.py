from django.test import TestCase

from valentina.app.forms import ProfileForm


class ProfileFormtest(TestCase):

    def test_form_has_fields(self):
        form = ProfileForm()
        self.assertSequenceEqual(list(form.fields), ['nickname'])
