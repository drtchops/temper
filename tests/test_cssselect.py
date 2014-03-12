import unittest

from temper.ext.cssselect_ext import CSSSelectTemper


class CSSSelectTestCast(unittest.TestCase):
    def setUp(self):
        self.temper = CSSSelectTemper()

    def test_selector_basic(self):
        tmpl = lambda t, c: t['div']()
        expected = '<div></div>\n'
        actual = self.temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_selector_id(self):
        tmpl = lambda t, c: t['div#the-test']()
        expected = '<div id="the-test"></div>\n'
        actual = self.temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_selector_class(self):
        tmpl = lambda t, c: t['div.testing']()
        expected = '<div class="testing"></div>\n'
        actual = self.temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_selector_attribute(self):
        tmpl = lambda t, c: t['div[name=example]']()
        expected = '<div name="example"></div>\n'
        actual = self.temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_selector_everything(self):
        tmpl = lambda t, c: t['div#t.e.s[name=t][data-el="will pass"]']()
        expected = '<div class="e s" id="t" name="t" data-el="will pass"></div>\n'
        actual = self.temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_selector_method(self):
        tmpl = lambda t, c: t.tag('div.cls')()
        expected = '<div class="cls"></div>\n'
        actual = self.temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_selector_getitem(self):
        tmpl = lambda t, c: t['div.cls']()
        expected = '<div class="cls"></div>\n'
        actual = self.temper.render(tmpl)
        self.assertEqual(expected, actual)

    def test_invalid_selector(self):
        tmpl = lambda t, c: t['div div']()
        self.assertRaises(ValueError, self.temper.render, tmpl)


if __name__ == '__main__':
    unittest.main()
