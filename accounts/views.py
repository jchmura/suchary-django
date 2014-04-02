from datetime import datetime, timedelta
from hashlib import md5

import requests
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
            return previous_page(request)
        else:
            return HttpResponse("User " + username + " is not active")
    else:
        return HttpResponse("Invalid username/password")


def signup(request):
    username = request.POST['username']

    if username and User.objects.filter(username=username):
        messages.error(request, '<strong>Błąd!</strong> Nazwa użytkownika <strong>' + escape(username) +
                                '</strong> jest już zajęta')
        return previous_page(request)

    password = request.POST['password']
    User.objects.create_user(username=username, password=password)

    new_user = authenticate(username=username, password=password)
    login(request, new_user)
    return previous_page(request)


def logout_view(request):
    logout(request)
    return previous_page(request)


def previous_page(request):
    page = request.GET.get('next', '/')
    return redirect(page)


def login_with_fb(request, fb_user):
    uid = fb_user.uid
    byte_password = ("fb" + uid + fb_user.username).encode()
    hash_password = md5(byte_password).hexdigest()

    user = authenticate(username='fb' + uid, password=hash_password)
    login(request, user)


def create_fb_user(uid, accessToken, expiresIn, username):
    fb_user = FacebookUser(uid=uid, access_token=accessToken, expires=expiresIn, username=username)
    fb_user.save()

    byte_password = ("fb" + uid + username).encode()
    hash_password = md5(byte_password).hexdigest()
    first_name, last_name = get_fb_name(accessToken)
    user = User.objects.create_user(username='fb' + uid, password=hash_password,
                                    first_name=first_name, last_name=last_name)
    fb_user.user = user
    fb_user.save()

    return fb_user


def fb_login(request):
    uid = request.POST['uid']
    accessToken = request.POST['accessToken']
    token, expires = create_long_token(accessToken)
    username = request.POST['username']

    fb_user = FacebookUser.objects.filter(uid=uid)
    if not fb_user:
        fb_user = create_fb_user(uid, token, expires, username)
    else:
        fb_user = fb_user[0]
        fb_user.access_token = token
        fb_user.expires = expires
        fb_user.save()

    login_with_fb(request, fb_user)
    return redirect('autorski.views.all_jokes')


def create_long_token(short_token):
    app_id = '628784013845093'
    app_secret = '63586567bad48773cc7980e3fa12b682'

    get = 'oauth/access_token?grant_type=fb_exchange_token&' + \
          'client_id={}&client_secret={}&fb_exchange_token={}'.format(app_id, app_secret, short_token)

    r = requests.get('https://graph.facebook.com/' + get)

    response = r.text.split('&')
    long_token, expires = None, None
    for item in response:
        item = item.split('=')
        key = item[0]
        if key == 'access_token':
            long_token = item[1]
        elif key == 'expires':
            expires = datetime.now() + timedelta(seconds=int(item[1]))

    return long_token, expires


def get_fb_name(token):
    url = 'https://graph.facebook.com/me?access_token={}'.format(token)

    r = requests.get(url)
    json = r.json()

    first_name = json['first_name']
    last_name = json['last_name']

    return first_name, last_name

