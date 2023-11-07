from django.http import HttpResponse
from pathlib import Path


def mocked_sigaa(request):
    mocked_html_path = Path(__file__).parent.absolute()

    with open(mocked_html_path / 'mock/sigaa.html', 'r') as html_file:
        content = html_file.read()

    return HttpResponse(content, content_type='text/html')


def mocked_empty(request):
    mocked_html_path = Path(__file__).parent.absolute()

    with open(mocked_html_path / 'mock/empty.html', 'r') as html_file:
        content = html_file.read()

    return HttpResponse(content, content_type='text/html')


def mocked_just_table(request):
    mocked_html_path = Path(__file__).parent.absolute()

    with open(mocked_html_path / 'mock/just_table.html', 'r') as html_file:
        content = html_file.read()

    return HttpResponse(content, content_type='text/html')
