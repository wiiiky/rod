# encoding=utf-8

from django.forms.models import model_to_dict


def to_dict(obj):
    data = model_to_dict(obj)
    data['pk'] = obj.pk
    return data
