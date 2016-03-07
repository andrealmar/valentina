
from django.conf import settings
from django.db import models
from django.utils.text import Truncator
from faker import Factory


class Profile(models.Model):

    FEMALE = 'F'
    MALE = 'M'
    OTHER = 'O'
    GENDERS = ((FEMALE, 'Feminino'), (MALE, 'Masculino'), (OTHER, 'Outro'))

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='Usuária')
    gender = models.CharField('gênero', max_length=1, choices=GENDERS)
    timezone = models.CharField('fuso-horário', max_length=255)
    nickname = models.CharField('apelido', max_length=255)

    def __str__(self):
        return self.nickname if self.nickname else self.user.get_full_name()

    @staticmethod
    def create_nickname():
        faker = Factory.create(settings.LANGUAGE_CODE)
        suffix = 'a'
        exceptions = ('Valentina', 'Lucca')
        nickname = faker.first_name_female()
        while not nickname.endswith(suffix) or nickname in exceptions:
            nickname = faker.first_name_female()
        return nickname

    class Meta:
        ordering = ['nickname']
        verbose_name = 'usuária'
        verbose_name_plural = 'usuárias'


class Chat(models.Model):

    person = models.CharField('identificador', max_length=255)
    created_at = models.DateTimeField('criado em', auto_now_add=True)

    def __str__(self):
        return self.person

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'chat'
        verbose_name_plural = 'chats'


class Message(models.Model):

    chat = models.ForeignKey('Chat')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField('conteúdo', null=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)

    def __str__(self):
        return Truncator(self.content).words(7)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'mensagem'
        verbose_name_plural = 'mensagens'


class Affiliation(models.Model):

    chat = models.ForeignKey('Chat')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='Usuária')
    alias = models.CharField('Nome fictício', max_length=140)

    class Meta:
        verbose_name = 'afiliação'
        verbose_name_plural = 'afiliações'
