# encoding=utf-8

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from util.model import to_dict
from web.models import *

@require_http_methods(['GET'])
def novels(request):
    nvs = []
    for nv in Novel.objects.all():
        nvs.append({
            'pk': nv.pk,
            'name': nv.name,
            'name_en': nv.name_en,
            'description': nv.description,
        })
    return JsonResponse(nvs, safe=False)

@require_http_methods(['GET'])
def novel_chapters(request, npk):
    chapters = []
    for c in Chapter.objects.filter(novel__pk=npk).defer('text').order_by('ctime'):
        chapters.append({
            'pk': c.pk,
            'title': c.title,
            'description': c.description,
        })
    return JsonResponse(chapters, safe=False)

@require_http_methods(['GET'])
def chapter(request, pk):
    chapter = Chapter.objects.get(pk=pk)
    return JsonResponse(to_dict(chapter))
