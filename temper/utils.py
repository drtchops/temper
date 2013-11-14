try:
    # python2
    from contextlib import GeneratorContextManager
except ImportError:
    # python3
    from contextlib import _GeneratorContextManager as GeneratorContextManager
from functools import wraps


class Dummy(object):
    pass


class Param(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("{} instance has no attribute '{}'".format(
                self.__class__.__name__, name))

    def __setattr__(self, name, value):
        self[name] = value


class TemperBlock(GeneratorContextManager):
    def __call__(self):
        self.close()

    def close(self):
        self.__enter__()
        self.__exit__(None, None, None)


def block(func):
    @wraps(func)
    def helper(*args, **kwds):
        return TemperBlock(func(*args, **kwds))
    return helper


def attributes_string(attrs):
    attributes = ''
    for k, v in attrs.items():
        n = k
        if n.endswith('_'):
            n = n[:-1]

        if n == 'data' and issubclass(v.__class__, dict):
            for attr, value in v.items():
                s = 'data-{}="{}"'.format(attr, value)
                attributes = ' '.join([attributes, s])
            continue

        s = ''
        if v is False:
            continue
        elif v is True:
            s = n
        else:
            s = '{}="{}"'.format(n, v)
        attributes = ' '.join([attributes, s])
    return attributes


def escape(s):
    return s.replace(
        '&', '&amp;',
    ).replace(
        '>', '&gt;',
    ).replace(
        '<', '&lt;',
    ).replace(
        "'", '&#39;',
    ).replace(
        '"', '&#34;'
    )
