from textwrap import dedent

from temper.tags import ALL_TAGS, Tag
from temper.utils import Param, escape


class Temper:
    '''
        Main Temper object which powers the DSL to convert Python code
        into HTML. Keeps a rendered string template in memory which
        its methods will append to.
        Main entry point is Temper.render
    '''

    def __init__(self, settings=None):
        '''
            Constructor. Takes an optional settings dict to set the following:
            indent: What str to use for indents. Default '    '.
            end: What str to use for line endings. Default '\\n'.
            safe: Whether to assume appended text is safe. Default False.
            strip: Whether to strip appended text of whitespace. Default False.
            tag_class: Allows you to use your own class for Tag objects.
        '''
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
        '''
            Shortcut for temper.tag(tag_name)
        '''
        if tag_name in ALL_TAGS:
            return lambda **attrs: self.tag(tag_name, **attrs)
        raise AttributeError("{0} instance has no attribute '{1}'".format(
            self.__class__.__name__, tag_name))

    def __call__(self, text, **kwargs):
        '''
            Shortcut for temper.append(text, **kwargs)
        '''
        self.append(text, **kwargs)

    def render(self, template_fn, context=None):
        '''
            Takes a callback function and optionally a context dict.
            Returns a rendered string of HTML.
        '''
        context = context or {}
        c = Param(**context)
        self.stack.append(self.tree)
        self.tree = ''
        template_fn(self, c)
        output = self.tree
        self.tree = self.stack.pop()
        return output

    def append(self, value, safe=None, strip=None, end=None):
        '''
            Appends a str value on the template. Any given arguments will
            override the temper object's settings. Optional agruments are:
            safe: Whether to escape any dangerous characters to HTML entities.
            strip: Whether to strip the str on whitespace.
            end: What str to append to the end of the str.
        '''
        if value.__class__ is self.settings.tag_class:
            value = value.start_tag

        if value is not None:
            if safe is False or (safe is None and not self.settings.safe):
                value = escape(value)
            if self.settings.indent:
                value = '{0}{1}'.format(self.settings.indent * self.depth, value)
            if strip or (strip is None and self.settings.strip):
                value = dedent(value).strip()
            if end is None:
                value = '{0}{1}'.format(value, self.settings.end)
            else:
                value = '{0}{1}'.format(value, end)
            self.tree += value

    def tag(self, tag_name, **attrs):
        '''
            Appends a tag object based on the given name and attrs.
        '''
        return self.settings.tag_class(tag_name, self, **attrs)

    def comment(self, text, **kwargs):
        '''
            Appends a comment with the given content.
            Will pass any kwargs through to append.
            Always assumes safe = True.
        '''
        kwargs['safe'] = True
        self.append('<!-- {0} -->'.format(text), **kwargs)

    @property
    def doctype(self):
        '''
            Appends the HTML5 doctype declaration.
        '''
        self.append('<!DOCTYPE html>', safe=True)
