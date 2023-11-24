from rest_framework.request import Request
from django.http import HttpResponse
from pathlib import Path

actual_path = {
    'sigaa': 'sigaa',
    'empty': 'empty',
    'table': 'just_table'
}

def mock_sigaa(request: Request, path: str) -> HttpResponse:
    mocked_html_path = Path(__file__).parent.absolute()

    with open(mocked_html_path / f"mock/{actual_path[path]}.html", 'r') as html_file:
        content = html_file.read()

    return HttpResponse(content, content_type='text/html')