# encoding=utf-8

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.urls import reverse
from writer.utils import to_dict
from writer.errors import HttpExecption
from web.models import Novel, Chapter
from datetime import datetime
from furl import furl
import hashlib
import tempfile
import stat
import os


@require_http_methods(['GET'])
def index(request):
    novels = Novel.objects.filter(
        user=request.user, deleted=False).order_by('ctime')
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
    chapters = Chapter.objects.filter(novel=n).defer('text').order_by('ctime')
    return render(request, 'writer/novel.html', locals())


@require_http_methods(['GET', 'POST', 'DELETE'])
def chapter(request, pk, cpk):
    n = get_object_or_404(Novel, pk=pk, deleted=False)
    if request.method == 'GET':
        c = {'title': '', 'text': '', 'pk': 'new'}
        image_field = settings.UPLOADS['IMAGE']['FIELD']
        if cpk != 'new':
            c = get_object_or_404(Chapter, novel=n, pk=cpk)
        return render(request, 'writer/chapter.html', locals())
    elif request.method == 'POST':
        text = request.data['text']
        title = request.data['title']
        if cpk != 'new':
            c = get_object_or_404(Chapter, novel=n, pk=cpk)
        else:
            c = Chapter(novel=n)
        c.text = text
        c.title = title
        c.save()
        return JsonResponse(to_dict(c))
    c = get_object_or_404(Chapter, novel=n, pk=cpk)
    c.delete()
    return JsonResponse({'retcode': 0})


def get_upload_image_extension(content_type):
    extension = settings.UPLOADS['IMAGE'][
        'ALLOWED_CONTENT_TYPES'].get(content_type)
    if not extension:
        raise HttpExecption(status_code=400, message='unallowed content type')
    return extension


@require_http_methods(['POST'])
def upload_image(request):
    setting = settings.UPLOADS['IMAGE']
    field = setting['FIELD']
    uploaded = request.FILES.get(field)
    extension = get_upload_image_extension(uploaded.content_type)
    md5 = hashlib.md5()
    f = tempfile.NamedTemporaryFile(
        prefix='rod-', suffix='-image', delete=False)
    try:
        for data in uploaded.chunks():
            f.write(data)
            md5.update(data)
        prefix = datetime.now().strftime(setting.get('PREFIX', ''))
        name = prefix + md5.hexdigest() + extension
        path = os.path.join(setting['PATH'], name)
        os.rename(f.name, path)
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR |
                 stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)
        url = str(furl(setting['URL']).add(path=name))
        return JsonResponse({'link': url})
    except Exception as e:
        raise e
    finally:
        os.remove(f.name) if os.path.exists(f.name) else None
