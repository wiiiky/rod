# encoding=utf-8

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from web.models import Novel, Chapter

@require_http_methods(['GET'])
def index(request):
    novels = Novel.objects.filter(user=request.user, deleted=False).order_by('ctime')
    return render(request, 'writer/index.html', locals())

@require_http_methods(['GET', 'POST'])
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

@require_http_methods(['GET'])
def logout(request):
    authlogout(request)
    return HttpResponseRedirect(reverse('w.login'))

@require_http_methods(['GET'])
def novel(request, pk):
    n = get_object_or_404(Novel, pk=pk, deleted=False)
    chapters = Chapter.objects.filter(novel=n).defer('text').order_by('seq')
    return render(request, 'writer/novel.html', locals())
