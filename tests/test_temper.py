#!/usr/bin/env python

import unittest

from temper import Temper
from temper.tags import Tag


class TemperTestCase(unittest.TestCase):
    def _basic_template_fn(self, t, c):
        t.doctype
        with t.html():
            with t.head():
                t.meta(charset='utf-8')
                t.title()('Basic template')
            with t.body():
                with t.form():
                    with t.label():
                        t.input(type='checkbox', name='working', value='1')
                        t('Is this working?')
                    t.button(type='submit')('Test')

    def _unsafe_template_fn(self, t, c):
        t('<script>alert("bad");</script>')

    def setUp(self):
        self.basic_temper = Temper()
        self.min_temper = Temper({
            'indent': '',
            'end': '',
            'strip': True,
        })
        self.safe_temper = Temper({
            'safe': True,
        })

    def test_examples_hello(self):
        from examples.hello import template

        expected = template.__doc__
        actual = self.basic_temper.render(template)
        self.assertEqual(expected, actual)

    def test_examples_subclasses_index(self):
        from examples.subclasses import Index

        expected = Index.__doc__
        actual = self.basic_temper.render(Index().render)
        self.assertEqual(expected, actual)

    def test_examples_subclasses_page(self):
        from examples.subclasses import Page

        expected = Page.__doc__
        actual = self.basic_temper.render(Page().render)
        self.assertEqual(expected, actual)

    def test_examples_subclasses_serious_page(self):
        from examples.subclasses import SeriousPage

        expected = SeriousPage.__doc__
        actual = self.basic_temper.render(SeriousPage().render)
        self.assertEqual(expected, actual)

    def test_basic_template(self):
        expected = '''\
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Basic template</title>
    </head>
    <body>
        <form>
            <label>
                <input type="checkbox" name="working" value="1">
                Is this working?
            </label>
            <button type="submit">Test</button>
        </form>
    </body>
</html>
'''
        actual = self.basic_temper.render(self._basic_template_fn)
        self.assertEqual(expected, actual)

    def test_minify_template(self):
        expected = (
            '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Basic '
            'template</title></head><body><form><label><input type="checkbox" '
            'name="working" value="1">Is this working?</label><button '
            'type="submit">Test</button></form></body></html>')
        actual = self.min_temper.render(self._basic_template_fn)
        self.assertEqual(expected, actual)

    def test_safe_input(self):
        expected = '<script>alert("bad");</script>\n'
        actual = self.safe_temper.render(self._unsafe_template_fn)
        self.assertEqual(expected, actual)

    def test_unsafe_input(self):
        expected = '&lt;script&gt;alert(&#34;bad&#34;);&lt;/script&gt;\n'
        actual = self.basic_temper.render(self._unsafe_template_fn)
        self.assertEqual(expected, actual)

    def test_subclass_tag(self):
        class TagestTag(Tag):
            @property
            def start_tag(self):
                return '<tag>'

            @property
            def end_tag(self):
                return '</tag>'

        t = Temper({
            'tag_class': TagestTag,
        })
        tmpl = lambda t, c: t.div(class_='t')('est')

        expected = '<tag>est</tag>\n'
        actual = t.render(tmpl)
        self.assertEqual(expected, actual)

    def test_valid_block_tag(self):
        tmpl = lambda t, c: t.div()('test')
        expected = '<div>test</div>\n'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_valid_void_tag(self):
        tmpl = lambda t, c: t.input()
        expected = '<input>\n'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_invalid_block_tag(self):
        tmpl = lambda t, c: t.input()('test')
        self.assertRaises(TypeError, self.basic_temper.render, tmpl)

    def test_block_with(self):
        def tmpl(t, c):
            with t.div():
                t('test')

        expected = '<div>\n    test\n</div>\n'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_block_inline(self):
        tmpl = lambda t, c: t.div()('test')
        expected = '<div>test</div>\n'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_block_chain(self):
        def tmpl(t, c):
            with t.div(id=1), t.div(id=2), t.div(id=3):
                t('test')

        expected = '''\
<div id="1">
    <div id="2">
        <div id="3">
            test
        </div>
    </div>
</div>
'''
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_append(self):
        tmpl = lambda t, c: t.append('test')
        expected = 'test\n'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_append_call(self):
        tmpl = lambda t, c: t('test')
        expected = 'test\n'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_append_safe(self):
        tmpl = lambda t, c: t.append('<test>', safe=True)
        expected = '<test>\n'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_append_unsafe(self):
        tmpl = lambda t, c: t.append('<test>', safe=False)
        expected = '&lt;test&gt;\n'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_append_strip(self):
        tmpl = lambda t, c: t.append('\t    test  \n', strip=True)
        expected = 'test\n'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_append_end_newline(self):
        tmpl = lambda t, c: t.append('test', end='END')
        expected = 'testEND'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_comment(self):
        tmpl = lambda t, c: t.comment('test')
        expected = '<!-- test -->\n'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_attributes(self):
        tmpl = lambda t, c: t.div(id='test')()
        expected = '<div id="test"></div>\n'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_attributes_with_underscore(self):
        tmpl = lambda t, c: t.div(class_='test', zattr_='another')()
        expected = '<div class="test" zattr="another"></div>\n'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_data_attributes(self):
        tmpl = lambda t, c: t.div(data={'count': 5})()
        expected = '<div data-count="5"></div>\n'
        actual = self.basic_temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_variables(self):
        tmpl = lambda t, c: t('Hello, %s!' % c.get('name'))
        context = {'name': 'Temper'}
        expected = 'Hello, Temper!\n'
        actual = self.basic_temper.render(tmpl, context)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
