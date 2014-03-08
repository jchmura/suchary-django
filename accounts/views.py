from datetime import datetime, timedelta
from hashlib import md5

from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.html import escape

from accounts.models import FacebookUser


def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            login(request, user)
            return redirect('autorski.views.all_jokes')
        else:
            return HttpResponse("User " + username + " is not active")
    else:
        return HttpResponse("Invalid username/password")


def signup(request):
    username = request.POST['username']

    if username and User.objects.filter(username=username):
        messages.error(request, '<strong>Błąd!</strong> Nazwa użytkownika <strong>' + escape(username) +
                                '</strong> jest już zajęta')
        return redirect('autorski.views.all_jokes')

    password = request.POST['password']
    User.objects.create_user(username=username, password=password)

    new_user = authenticate(username=username, password=password)
    login(request, new_user)
    return redirect('autorski.views.all_jokes')


def logout_view(request):
    logout(request)
    return redirect('autorski.views.all_jokes')


def login_with_fb(request, fb_user):
    uid = fb_user.uid
    byte_password = ("fb" + uid + fb_user.username).encode()
    password = md5(byte_password).hexdigest()

    user = authenticate(username='fb' + uid, password=password)
    login(request, user)


def create_fb_user(uid, accessToken, expiresIn, username):
    date = datetime.now() + timedelta(seconds=expiresIn)
    fb_user = FacebookUser(uid=uid, access_token=accessToken, expires=date, username=username)
    fb_user.save()

    byte_password = ("fb" + uid + username).encode()
    user = User.objects.create_user(username='fb' + uid, password=md5(byte_password).hexdigest())
    fb_user.user = user
    fb_user.save()

    return fb_user


def fb_login(request):
    uid = request.POST['uid']
    accessToken = request.POST['accessToken']
    expiresIn = int(request.POST['expiresIn'])
    username = request.POST['username']

    fb_user = FacebookUser.objects.filter(uid=uid)
    if not fb_user:
        fb_user = create_fb_user(uid, accessToken, expiresIn, username)
    else:
        fb_user = fb_user[0]

    login_with_fb(request, fb_user)
    return redirect('autorski.views.all_jokes')