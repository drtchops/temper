#!/usr/bin/env python


from __future__ import print_function

from temper import Temper


def main():
    # init and call temper to render
    temper = Temper()
    print(temper.render(Index().render))
    print(temper.render(Page().render))
    print(temper.render(SeriousPage().render))


class Index(object):
    '''
        <!DOCTYPE html>
        <!-- Index -->
        <html>
            <head>
                <title>
                    Hello, Example!
                </title>
                <style type="text/css">
                    .bold { font-weight: bold; }
                </style>
            </head>
            <body>
                <p class="bold">
                    Hello, World!
                </p>
            </body>
        </html>
    '''

    title = 'Hello, Example!'

    def body(self, t, c):
        # a "block" can be any python function or property
        t('Hello, World!')

    def render(self, t, c):
        # render the base template
        t.doctype
        t.comment(self.__class__.__name__)
        with t.html():
            with t.head():
                with t.title():
                    t(self.title)

                with t.style(type='text/css'):
                    t('.bold { font-weight: bold; }')

            with t.body():
                with t.p(class_='bold'):
                    self.body(t, c)


class Page(Index):
    '''
        <!DOCTYPE html>
        <!-- Page -->
        <html>
            <head>
                <title>
                    Hello, Example!
                </title>
                <style type="text/css">
                    .bold { font-weight: bold; }
                </style>
            </head>
            <body>
                <p class="bold">
                    Hello, World!
                    Hello, Temper!
                </p>
            </body>
        </html>
    '''

    def body(self, t, c):
        # use python inheritance for blocks
        super(Page, self).body(t, c)
        t('Hello, Temper!')


class SeriousPage(Index):
    '''
        <!DOCTYPE html>
        <!-- SeriousPage -->
        <html>
            <head>
                <title>
                    Now then...
                </title>
                <style type="text/css">
                    .bold { font-weight: bold; }
                </style>
            </head>
            <body>
                <p class="bold">
                    Let&#39;s get down to business.
                </p>
            </body>
        </html>
    '''

    title = 'Now then...'

    def body(self, t, c):
        # don't call super to completely override
        t("Let's get down to business.")


if __name__ == '__main__':
    main()
