import re


def multiple_replace(text, replacement=None):
    replacement_dict = replacement
    if not replacement: # pragma: no cover
        replacement_dict = {
            '\n': '',
            '\t': '',
            '\r': '',
        }

    pattern = re.compile('|'.join(map(re.escape, replacement_dict.keys())))
    return pattern.sub(lambda match: replacement_dict[match.group(0)], text)
