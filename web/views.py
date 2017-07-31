# encoding=utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from web.models import Novel, Chapter


def index(request):
    n = Novel.objects.filter(deleted=False).first()
    return render_to_response('web/index.html', context=locals())


def novel(request, pk):
    n = get_object_or_404(Novel, pk=pk, deleted=False)
    return render_to_response('web/novel.html', context=locals())
