from temper.utils import attributes_string


BLOCK_TAGS = {
    'a', 'abbr', 'address', 'article', 'aside', 'audio', 'b', 'bdi', 'bdo',
    'blockquote', 'body', 'button', 'canvas', 'caption', 'cite', 'code',
    'colgroup', 'datalist', 'dd', 'del', 'details', 'dfn', 'dir', 'div', 'dl',
    'doctype', 'dt', 'em', 'fieldset', 'figcaption', 'figure', 'footer',
    'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hgroup',
    'html', 'i', 'iframe', 'ins', 'kbd', 'label', 'legend', 'li', 'map',
    'mark', 'menu', 'meter', 'nav', 'noscript', 'object', 'ol', 'optgroup',
    'option', 'output', 'p', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's',
    'samp', 'script', 'section', 'select', 'small', 'span', 'strong', 'style',
    'sub', 'summary', 'sup', 'table', 'tbody', 'td', 'textarea', 'tfoot', 'th',
    'thead', 'time', 'title', 'tr', 'u', 'ul', 'var', 'video',
}
VOID_TAGS = {
    'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input',
    'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr',
}
ALL_TAGS = BLOCK_TAGS | VOID_TAGS


class Tag(object):
    def __init__(self, tag_name, t, **attrs):
        if tag_name == 'doctype':
            tag_name = '!DOCTYPE'
        self.tag_name = tag_name
        # assume custom tags are blocks
        self.is_block = tag_name not in VOID_TAGS
        self.t = t
        self._attrs = attrs

        if not self.is_block:
            self.t(self.start_tag, safe=True)

    def __enter__(self):
        self.t(self.start_tag, safe=True)
        self.t.depth += 1

    def __exit__(self, value, type, traceback):
        self.t.depth -= 1
        self.t(self.end_tag, safe=True)

    def __call__(self, text=None, **kwargs):
        self.close(text, **kwargs)

    @property
    def attr_str(self):
        return attributes_string(self._attrs)

    @property
    def start_tag(self):
        return '<{}{}>'.format(self.tag_name, self.attr_str)

    @property
    def end_tag(self):
        if not self.is_block:
            raise TypeError('{} is a void tag.'.format(self.tag_name))
        return '</{}>'.format(self.tag_name)

    def attrs(self, **attrs):
        self._attrs.update(attrs)

    def close(self, text=None, safe=False):
        self.t(self.start_tag, safe=True, end='')
        if text:
            self.t(text, safe=safe, strip=True, end='')
        self.t(self.end_tag, safe=True, strip=True)
