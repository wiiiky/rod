# encoding=utf-8

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.forms.models import model_to_dict
from web.models import Novel, Chapter


def index(request):
    n = Novel.objects.filter(deleted=False).first()
    return render_to_response('web/index.html', context=locals())


def novel(request, pk):
    return chapter(request, pk, 1)

def chapter(request, pk, seq):
    n = get_object_or_404(Novel, pk=pk, deleted=False)
    c = get_object_or_404(Chapter, novel=n, seq=seq)
    if request.GET.get('type') == 'raw':
        return JsonResponse(model_to_dict(c))
    pc = Chapter.objects.filter(novel=n, seq__lt=c.seq).order_by('-seq').first()
    nc = Chapter.objects.filter(novel=n, seq__gt=c.seq).order_by('seq').first()
    chapters = Chapter.objects.filter(novel=n).defer('text').order_by('seq')
    return render_to_response('web/novel.html', context=locals())
