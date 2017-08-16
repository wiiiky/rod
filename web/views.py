# encoding=utf-8

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from web.models import Novel, Chapter, ChapterComment
from web.utils import get_client_ip


@require_http_methods(['GET'])
def index(request):
    n = Novel.objects.filter(deleted=False).first()
    return render_to_response('web/index.html', context=locals())


@require_http_methods(['GET'])
def novel(request, pk):
    return chapter(request, pk, '')


@require_http_methods(['GET'])
def chapter(request, pk, cpk):
    n = get_object_or_404(Novel, pk=pk, deleted=False)
    if cpk:
        c = get_object_or_404(Chapter, novel=n, pk=cpk)
    else:
        c = get_list_or_404(Chapter.objects.order_by('ctime'), novel=n)[0]
    if request.GET.get('type') == 'raw':
        return JsonResponse(model_to_dict(c))
    pc = Chapter.objects.filter(novel=n, ctime__lt=c.ctime).order_by('-ctime').first()
    nc = Chapter.objects.filter(novel=n, ctime__gt=c.ctime).order_by('ctime').first()
    chapters = Chapter.objects.filter(novel=n).defer('text').order_by('ctime')
    comments = ChapterComment.objects.filter(chapter=c).order_by('ctime')
    title = '%s - %s' % (n.name, c.title)
    return render_to_response('web/novel.html', context=locals())


@require_http_methods(['POST'])
def chapter_comment(request, pk, cpk):
    c = get_object_or_404(Chapter, novel__pk=pk, pk=cpk)
    nickname = request.data.get('nickname')
    content = request.data.get('content')
    ip = get_client_ip(request)
    if not content:
        return JsonResponse({'retcode': 1})
    if not nickanme:
        nickname = 'Anonymous'
    cc = ChapterComment(Chapter=c, nickname=nickname, content=content, ip=ip)
    cc.save()
    return JsonResponse(model_to_dict(cc))
