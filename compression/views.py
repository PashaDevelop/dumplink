from django.views.decorators.http import require_GET, require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .utils import dump_link, restore_link, remove_link


@require_GET
def dump(request):
    """
    Сжимает длинную ссылку
    На входе ожидается один GET параметр 'url'
    Пример: http://host:port/?url=url
    :param request:
    :return: Сжатую ссылку, переданную в GET параметре url
    """
    url = request.GET.get('url')
    if not url:
        return HttpResponseBadRequest('Необходимо передать url для сжатия')
    new_url = dump_link(request._current_scheme_host, url)
    return HttpResponse(new_url)


@require_GET
def restore(request):
    """
    Распаковывает сжатую ссылку
    Ожидаются два GET параметра redirect, paramId
    redirect - флаг true/false, который определяет, нужно выполнить перенаправление,
     либо вернуть распакованную ссылку
    paramId - уникальный идентификатор сжатой ссылки. Поле генерируется автоматически
    Пример: http://host:port/comp/restore/?paramId=731b1d24-86ef-4241-ace5-223b76007f97&redirect=false
    :param request:
    :return: Распакованная ссылка, либо перенаправление на неё
    """
    redirect = request.GET.get('redirect', 'false')
    param_id = request.GET.get('paramId')
    if not param_id:
        return HttpResponseBadRequest('Необходимо передать param_id для распаковки url')
    url = restore_link(param_id)
    if not url:
        return HttpResponse('Данный ссылка больше недействительна')
    if redirect == 'true':
        return HttpResponseRedirect(url)
    return HttpResponse(url)


@csrf_exempt
@require_http_methods(['DELETE'])
def remove(request, param_id):
    """
    Удаляет из кеша сжатую ссылку
    Пример: http://host:port/comp/remove/731b1d24-86ef-4241-ace5-223b76007f97/
    :param request:
    :param paramId: уникальный идентификатор сжатой ссылки. Поле генерируется автоматически
    :return: 204 No Content
    """
    remove_link(param_id)
    return HttpResponse(status=204)
