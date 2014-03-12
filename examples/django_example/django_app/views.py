from django.http import HttpResponse
from django.template import RequestContext
from django.views.generic.base import TemplateView
from temper import Temper

from .utils import css_link, js_link, url  # , select


class View(TemplateView):
    def render_to_string(self, context=None):
        t = Temper({
            'indent': None,
            'end': '',
            'strip': True,
        })
        d = {}
        for c in RequestContext(self.request):
            d.update(c)
        if context:
            d.update(context)
        return t.render(self.render, d)

    def render_to_response(self, context=None):
        return HttpResponse(self.render_to_string(context))

    def render(self, t, c):
        t.doctype
        with t.html():
            with t.head():
                t.meta(charset='utf-8')
                with t.title():
                    self.title(t, c)

                css_link(t, '//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css')
                css_link(t, 'http://getbootstrap.com/examples/starter-template/starter-template.css')
                js_link(t, '//code.jquery.com/jquery-1.10.2.min.js')
                js_link(t, '//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js')

            with t.body():
                with t.div(class_='navbar navbar-inverse navbar-fixed-top'), t.div(class_='container'), t.div(class_='navbar-header'), t.a(href='#', class_='navbar-brand'):
                    t('Temper Test')

                with t.div(class_='container'), t.div(class_='starter-template'):
                    self.content(t, c)

    def title(self, t, c):
        t('It works!')

    def content(self, t, c):
        pass


@url(r'^$', name='home')
class MyView(View):
    def get(self, request, *args, **kwargs):
        context_test = {
            'test': '<strong>Hello World</strong>',
        }
        return self.render_to_response(context_test)

    def content(self, t, c):
        with t.h1():
            t('Hello World!')
        with t.p():
            t('The is just an example template using <strong>Temper</strong>, <strong>Django</strong> and <strong>Bootstrap</strong>!', safe=True)

        with t.p():
            if 'test' in c:
                # try with safe=True
                t("You passed '{}' as context variable 'test'".format(c['test']))
            else:
                t("You did not pass 'test' in the context")

        # with t.div():
        #     select(t, 'test', ((1, 'One'), (2, 'Two')), 2)
