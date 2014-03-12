import sys

from django.conf.urls import patterns, url as django_url


def url(*regexes, **kwargs):
    caller_filename = sys._getframe(1).f_code.co_filename
    for m in sys.modules.values():
        if (m and '__file__' in m.__dict__ and
                m.__file__.startswith(caller_filename)):
            module = m
            break

    def _wrapper(cls):
        if module:
            if 'urlpatterns' not in module.__dict__:
                module.urlpatterns = []

            view = cls.as_view()
            view_name = kwargs.get('name') or cls.__name__
            url_kwargs = dict(kwargs)
            url_kwargs['name'] = view_name
            for regex in regexes:
                module.urlpatterns += patterns(
                    '', django_url(regex, view, **url_kwargs))
        return cls
    return _wrapper


def select(t, name, options=[], value=None):
    with t.select():
        for o in options:
            with t.option(checked=o[0] == value, value=o[0]):
                t(o[1])


def css_link(t, href):
    t.link(rel='stylesheet', href=href)


def js_link(t, href):
    t.script(type='text/javascript', src=href)()
