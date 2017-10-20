# encoding=utf-8

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import resolve, reverse
from writer.errors import HttpExecption
from django.conf import settings
import json


class WriterAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        path = request.path
        url = resolve(path)
        url_name = url.url_name
        if not url_name.startswith('w.') or url_name == "w.login":
            return
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('w.login'))


class DataPreprocessMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.method not in ('POST', 'PUT'):
            return
        if request.content_type == 'application/json':
            request.data = json.loads(request.body.decode("utf-8"))


class ExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, e):
        print(e)
        if isinstance(e, HttpExecption):
            return HttpResponse(status=e.status_code, content=e.message)
        if settings.DEBUG:
            return HttpResponse(status=500, content=str(e))
        return HttpResponse(status=500, content='unknown error')
