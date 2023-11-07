from django.http import HttpResponse
from pathlib import Path


def mocked_departments(request):
    mocked_html_path = Path(__file__).parent.absolute()

    with open(mocked_html_path / 'mock/departments.html', 'r') as html_file:
        content = html_file.read()

    return HttpResponse(content, content_type='text/html')
