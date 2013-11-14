from textwrap import dedent

from temper.tags import ALL_TAGS
from temper.tags import Tag
from temper.utils import Param
from temper.utils import escape


class Temper:
    def __init__(self, settings=None):
        self.tree = ''
        self.stack = []
        self.depth = 0

        # defaults
        self.settings = {
            'indent': '    ',
            'end': '\n',
            'safe': False,
            'strip': False,
            'tag_class': Tag,
        }
        if settings:
            # custom
            self.settings.update(settings)
        self.settings = Param(**self.settings)

    def __getattr__(self, tag_name):
        if tag_name in ALL_TAGS:
            return lambda **attrs: self.tag(tag_name, **attrs)
        raise AttributeError("{} instance has no attribute '{}'".format(
            self.__class__.__name__, tag_name))

    def __call__(self, text, **kwargs):
        self.append(text, **kwargs)

    def render(self, template_fn, context=None):
        context = context or {}
        c = Param(**context)
        self.stack.append(self.tree)
        self.tree = ''
        template_fn(self, c)
        output = self.tree
        self.tree = self.stack.pop()
        return output

    def append(self, value, safe=None, strip=None, end=None):
        if value.__class__ is self.settings.tag_class:
            value = value.start_tag

        if value is not None:
            if safe is False or (safe is None and not self.settings.safe):
                value = escape(value)
            if self.settings.indent:
                value = '{}{}'.format(self.settings.indent * self.depth, value)
            if strip or (strip is None and self.settings.strip):
                value = dedent(value).strip()
            if end is None:
                value = '{}{}'.format(value, self.settings.end)
            else:
                value = '{}{}'.format(value, end)
            self.tree += value

    def tag(self, tag_name, **attrs):
        return self.settings.tag_class(tag_name, self, **attrs)

    def comment(self, text, **kwargs):
        kwargs['safe'] = True
        self.append('<!-- {} -->'.format(text), **kwargs)

    @property
    def doctype(self):
        self.append('<!DOCTYPE html>', safe=True)
