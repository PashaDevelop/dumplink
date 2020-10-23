import os
import requests
from urllib.parse import urlparse, urljoin

from django.test import TestCase
from django.core.cache import cache

from dump_link import settings
from .utils import dump_link, restore_link, remove_link


class CompressionTestCase(TestCase):

    def setUp(self) -> None:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def test_dump_link(self):
        link = dump_link('host', 'url')
        url = urlparse(link)
        params = params_to_dict(url.query)
        link = cache.get(params['paramId'])
        cache.delete(params['paramId'])
        assert link

    def test_dump_400(self):
        response = requests.get(urljoin(settings.TEST_URL, '/comp/dump/'))
        assert response.status_code

    def test_dump_functional(self):
        url = 'https://yandex.ru/search/?text=ф'
        res = requests.get(urljoin(settings.TEST_URL, f'/comp/dump/?url={url}'))
        res = requests.get(res.text)
        assert res.text == url

    def test_restore_params(self):
        link = dump_link('host', 'url')
        url = urlparse(link)
        params = params_to_dict(url.query)
        assert restore_link(params['paramId']) == 'url'

    def test_restore_not_exists_link(self):
        link = dump_link('host', 'url')
        url = urlparse(link)
        params = params_to_dict(url.query)
        cache.delete(params['paramId'])
        assert restore_link(params['paramId']) is None

    def test_remove_link(self):
        link = dump_link('host', 'url')
        url = urlparse(link)
        params = params_to_dict(url.query)
        remove_link(params['paramId'])
        assert cache.get(params['paramId']) is None

    def test_remove_functional(self):
        url = 'https://yandex.ru/search/?text=ф'
        res = requests.get(urljoin(settings.TEST_URL, f'/comp/dump/?url={url}'))
        url = urlparse(res.text)
        params = params_to_dict(url.query)
        res = requests.delete(urljoin(settings.TEST_URL, f"/comp/remove/{params['paramId']}/"))
        assert res.status_code == 204

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def tearDown(self) -> None:
        pass


def params_to_dict(query):
    params = {}
    query = query.split('&')
    for param in query:
        param = param.split('=')
        params[param[0]] = param[1]
    return params
