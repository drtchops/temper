#!/usr/bin/env python


from __future__ import print_function

from temper import Temper


t = Temper()


def main():
    print(t.render(template))


def template(*args):
    t.doctype
    with t.html():
        with t.head():
            with t.title():
                t('Temper Example')
        with t.body():
            t('Hello, World!')


if __name__ == '__main__':
    main()
