# encoding=utf-8

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import resolve, reverse
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
