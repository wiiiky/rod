# encoding=utf-8

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login as authlogin
from django.http import JsonResponse

def index(request):
    return render(request, 'writer/index.html', locals())

#@csrf_protect
def login(request):
    if request.method == 'GET':
        return render(request, 'writer/login.html', locals())
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user and user.has_perm('writable'):
        authlogin(request, user)
        return JsonResponse({'retcode': 0})
    return JsonResponse({'retcode': 1})
