from django.conf.urls import url
from valentina.app.views import welcome, chat, profile, logout

urlpatterns = [
    url(r'^$', welcome, name='welcome'),
    url(r'^chat/(?P<pk>\d+)/$', chat, name='chat'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^logout/$', logout, name='logout'),
]
