# encoding=utf-8

from django.db import models
import uuid


def default_uuid():
    return str(uuid.uuid4()).replace('-', '')


class BaseModel(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=default_uuid, editable=False)
    ctime = models.DateTimeField(auto_now=True, db_index=True, help_text=u'创建时间')
    utime = models.DateTimeField(auto_now_add=True, help_text=u'更新时间')
    deleted = models.BooleanField(default=False, db_index=True, help_text=u'是否删除')

    def delete(self):
        self.deleted = True
        self.save()

    def _delete(self):
        super(BaseModel, self).delete()

    class Meta:
        abstract = True


class Novel(BaseModel):
    '''小说'''
    name = models.CharField(max_length=32, help_text=u'书名')
    name_en = models.CharField(max_length=64, help_text=u'英文名')


class Chapter(BaseModel):
    '''章节'''
    novel = models.ForeignKey(Novel)
    seq = models.PositiveIntegerField(unique=True, help_text=u'章节编号')
    title = models.CharField(max_length=32, help_text=u'章节标题')
    text = models.TextField(help_text=u'正文,HTML格式')
