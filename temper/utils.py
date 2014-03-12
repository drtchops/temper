try:
    # python2
    from contextlib import GeneratorContextManager
except ImportError:
    # python3
    from contextlib import _GeneratorContextManager as GeneratorContextManager
from functools import wraps


class Dummy(object):
    '''
        Dummy object for setting arbitrary attributes.
    '''
    pass


class Param(dict):
    '''
        Allows a dict to be accessed like an object.
    '''
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("{0} instance has no attribute '{1}'".format(
                self.__class__.__name__, name))

    def __setattr__(self, name, value):
        self[name] = value


class TemperBlock(GeneratorContextManager):
    '''
        Temper wrapper around a context manager.
        Provides a shorthand for instant closing.
    '''
    def __call__(self):
        self.close()

    def close(self):
        self.__enter__()
        self.__exit__(None, None, None)


def block(func):
    '''
        Decorator for defining your own block functions when extending Temper.
    '''
    @wraps(func)
    def helper(*args, **kwargs):
        return TemperBlock(func(*args, **kwargs))
    return helper


def attributes_string(attrs):
    '''
        Takes a dict and returns an HTML rendered string of attributes.
    '''
    attributes = ''
    for k, v in attrs.items():
        n = k
        if n.endswith('_'):
            n = n[:-1]

        if n == 'data' and issubclass(v.__class__, dict):
            for attr, value in v.items():
                s = 'data-{0}="{1}"'.format(attr, value)
                attributes = ' '.join([attributes, s])
            continue

        s = ''
        if v is False:
            continue
        elif v is True:
            s = n
        else:
            s = '{0}="{1}"'.format(n, v)
        attributes = ' '.join([attributes, s])
    return attributes


def escape(s):
    '''
        Replaces dangerous characters with HTML escaped entities.
    '''
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
