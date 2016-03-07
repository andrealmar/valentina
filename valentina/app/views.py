import arrow
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.conf import settings
from valentina.app.forms import MessageForm, ProfileForm
from valentina.app.models import Profile, Chat, Message, Affiliation


@login_required(login_url='/')
def welcome(request):

    # abort if request has no user
    if not request.user:
        return redirect(resolve_url('home'))

    # abort if user is not valid
    if not _valid_user(request.user):
        return redirect(resolve_url('female_only'))

    context = {'chats': _affiliations_to_ctx(request.user),
               'nickname': request.user.profile.nickname}

    return render(request, 'app/home.html', context)


@login_required(login_url='/')
def chat(request, pk):
    if request.method == 'POST':
        return save_message(request, pk)
    if request.method == 'GET':
        return list_messages(request, pk)
    return HttpResponseNotAllowed(['GET', 'POST'])


@login_required(login_url='/')
def list_messages(request, pk):

    chat = get_object_or_404(Chat, pk=pk)
    affiliation = get_object_or_404(Affiliation, chat=chat, user=request.user)
    messages = Message.objects.filter(chat=chat)[:50]

    chat_details = {'id': chat.pk, 'alias': affiliation.alias}
    messages = [_message_to_dict(request, msg) for msg in messages]

    return JsonResponse({'chat': chat_details, 'messages': messages})


@login_required(login_url='/')
def save_message(request, pk):

    form = MessageForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': form.errors}, status=400)

    chat = Chat.objects.get(pk=pk)
    if not chat:
        return JsonResponse({'error': 'Invalid chat'}, status=401)

    affiliation = Affiliation.objects.filter(chat=chat, user=request.user)
    if not affiliation:
        return JsonResponse({'error': 'User does not belongs to chat'},
                            status=401)

    message = Message.objects.create(chat=chat, user=request.user,
                                     content=form.cleaned_data.get('content'))

    return JsonResponse(_message_to_dict(request, message), status=201)


@login_required(login_url='/')
def profile(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data.get('nickname')
            request.user.profile.nickname = nickname
            request.user.profile.save()
            return JsonResponse({'nickname': nickname})
        else:
            return JsonResponse({'error': form.errors}, status=400)

    return HttpResponseNotAllowed(['POST'])


def logout(request):
    auth_logout(request)
    return redirect(resolve_url('home'))


def _valid_user(user):

    # authorize if user is staff
    if user.is_staff:
        return True

    # authorize if user is female
    if hasattr(user, 'profile'):
        if user.profile.gender == Profile.FEMALE:
            return True

    return False


def _message_to_dict(request, message):
    created_at = arrow.get(message.created_at)
    css_class = 'me' if request.user == message.user else ''
    return {'content': message.content,
            'ago': created_at.humanize(locale=settings.LANGUAGE_CODE[:2]),
            'author': message.user.profile.nickname,
            'id': message.pk,
            'className': css_class}


def _affiliations_to_ctx(user):
    output = list()
    for affiliation in Affiliation.objects.filter(user=user):
        data = dict(url=resolve_url('app:chat', affiliation.chat.pk),
                    alias=affiliation.alias,
                    valentinas=affiliation.chat.affiliation_set.count())
        output.append(data)
    return output
