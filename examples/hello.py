#!/usr/bin/env python

from __future__ import print_function

from temper import Temper


def main():
    print(Temper().render(template))


def template(t, c):
    '''\
<!DOCTYPE html>
<html>
    <head>
        <title>
            Temper Example
        </title>
    </head>
    <body>
        Hello, World!
    </body>
</html>
'''

    t.doctype
    with t.html():
        with t.head():
            with t.title():
                t('Temper Example')
        with t.body():
            t('Hello, World!')


if __name__ == '__main__':
    main()
