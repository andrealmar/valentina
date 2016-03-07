from django.contrib import admin
from valentina.app.models import Affiliation, Chat, Message, Profile


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'gender', 'email', 'last_login',
                    'date_joined')
    search_fields = ('nickname', 'name', 'email')

    def email(self, obj):
        return obj.user.email

    email.short_description = 'e-mail'

    def last_login(self, obj):
        return obj.user.last_login

    last_login.short_description = 'último login'

    def date_joined(self, obj):
        return obj.user.date_joined

    date_joined.short_description = 'criado em'


class ChatModelAdmin(admin.ModelAdmin):
    list_display = ('person', )


class MessageModelAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'chat', 'excerpt', 'created_at')

    def user_full_name(self, obj):
        name = obj.user.get_full_name()
        return name if name else obj.user.profile.nickname

    user_full_name.short_description = 'usuário'

    def excerpt(self, obj):
        return obj.__str__()

    excerpt.short_description = 'conteúdo'


class AffiliationModelAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'chat', 'alias')

    def user_full_name(self, obj):
        name = obj.user.get_full_name()
        return name if name else obj.user.profile.nickname

    user_full_name.short_description = 'usuário'

admin.site.register(Profile, ProfileModelAdmin)
admin.site.register(Chat, ChatModelAdmin)
admin.site.register(Message, MessageModelAdmin)
admin.site.register(Affiliation, AffiliationModelAdmin)
