import json
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter


def json_prettify(json_string):
    """
    Adapted from:
    https://www.pydanny.com/pretty-formatting-json-django-admin.html
    """

    formatter = HtmlFormatter(style='igor')

    json_data = json.loads(json_string)
    json_text = highlight(
        json.dumps(json_data, sort_keys=True, indent=2,
                   ensure_ascii=False).encode('utf-8'),
        JsonLexer(),
        formatter
    )

    json_text = json_text \
        .replace('<span class="p">{</span>\n', '') \
        .replace('<span class="p">}</span>\n', '')

    style = "<style>" + formatter.get_style_defs() + "</style>"

    return mark_safe(style + json_text)
