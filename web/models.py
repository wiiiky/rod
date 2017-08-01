# encoding=utf-8

from django.db import models
from web.utils import num2chinese
import uuid


def default_uuid():
    return str(uuid.uuid4()).replace('-', '')


class BaseModel(models.Model):
    id = models.CharField(max_length=32, primary_key=True,
                          default=default_uuid, editable=False)
    ctime = models.DateTimeField(
        auto_now=True, db_index=True, help_text=u'创建时间')
    utime = models.DateTimeField(auto_now_add=True, help_text=u'更新时间')

    class Meta:
        abstract = True


class Novel(BaseModel):
    '''小说'''
    name = models.CharField(max_length=32, help_text=u'书名')
    name_en = models.CharField(max_length=64, help_text=u'英文名')
    deleted = models.BooleanField(
        default=False, db_index=True, help_text=u'是否删除')


class Chapter(BaseModel):
    '''章节'''
    novel = models.ForeignKey(Novel)
    seq = models.PositiveIntegerField(default=1, help_text=u'章节编号')
    title = models.CharField(max_length=32, help_text=u'章节标题')
    text = models.TextField(help_text=u'正文,HTML格式')

    class Meta:
        unique_together = ('novel', 'seq')

    @property
    def seq_name(self):
        return '第%s章' % num2chinese(self.seq, big=False, simp=True)

    @property
    def fullname(self):
        return '%s %s' % (self.seq_name, self.title)
