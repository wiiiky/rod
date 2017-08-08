# encoding=utf-8

from django.db import models
from django.contrib.auth.models import User
from web.utils import num2chinese
import uuid


def default_uuid():
    return str(uuid.uuid4()).replace('-', '')


class BaseModel(models.Model):
    id = models.CharField(max_length=32, primary_key=True,
                          default=default_uuid, editable=False)
    ctime = models.DateTimeField(
        auto_now_add=True, db_index=True, help_text=u'创建时间')
    utime = models.DateTimeField(auto_now=True, help_text=u'更新时间')

    class Meta:
        abstract = True


class Novel(BaseModel):
    '''小说'''
    name = models.CharField(max_length=32, help_text=u'书名')
    name_en = models.CharField(max_length=64, help_text=u'英文名')
    user = models.ForeignKey(User, help_text=u'创建者')
    deleted = models.BooleanField(
        default=False, db_index=True, help_text=u'是否删除')


class Chapter(BaseModel):
    '''章节'''
    novel = models.ForeignKey(Novel)
    title = models.CharField(max_length=32, help_text=u'章节标题')
    text = models.TextField(help_text=u'正文,HTML格式')
