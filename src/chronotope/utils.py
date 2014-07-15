import html2text


def html_2_text(value):
    if not isinstance(value, unicode):
        value = value.decode('utf-8')
    return html2text.html2text(value)


def html_index_transform(instance, value):
    return html_2_text(value)
