from django import forms
from valentina.app.models import Message, Profile


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['content', 'chat']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['nickname']
