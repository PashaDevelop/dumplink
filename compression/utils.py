import uuid

from django.core.cache import cache


def dump_link(host, url, redirect=False):
    """
    Выполняет сжатие ссылки
    :param host: адрес, на который перенаправляем
    :param url: ссылка, которую сжимаем
    :param redirect: Флаг, который определяет, доложить redirect=true или redirect=false в GET параметры ссылки.
    :return:
    """
    param_id = str(uuid.uuid4())
    cache.set(param_id, url)
    return '{host}{path}paramId={param_id}&redirect={redirect}'.format(
        host=host, path='/comp/restore/?', param_id=param_id, redirect=str(redirect).lower())


def restore_link(param_id):
    """
    Выполняет распаковку ссылки
    :param param_id: Уникальный идентификатор сжатой ссылки
    :return: Распакованную ссылку
    """
    return cache.get(param_id)


def remove_link(param_id):
    """
    Выполняет удаление сжатой ссылки
    :param param_id:
    :return:
    """
    cache.delete(param_id)
