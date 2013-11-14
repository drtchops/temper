Temper is a pure Python HTML DSL for angry developers.


```python
from django.http import HttpResponse
from django.template import RequestContext
from django.views.generic.base import TemplateView
from temper import Temper

from .utils import css_link
from .utils import js_link
# from .utils import select
from .utils import url


class View(TemplateView):
    ############################### VIEW
    # Do your logic and querying here
    def get(self, *args, **kwargs):
        return self.render_to_response()

    def render_to_string(self, context=None):
        t = Temper()
        d = {}
        for c in RequestContext(self.request):
            d.update(c)
        if context:
            d.update(context)
        return t.render(self.render, d)

    def render_to_response(self, context=None):
        return HttpResponse(self.render_to_string(context))
    ############################### /VIEW

    ############################### TEMPLATE
    # This can also be done in a separate class or file
    def render(self, t, c):
        t.doctype
        t.meta(charset='utf-8')
        with t.html():
            with t.head():
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
    ############################### /TEMPLATE


@url(r'^$', name='home')
class MyView(View):
    ############################### VIEW
    def get(self, request, *args, **kwargs):
        context_test = {
            'test': '<strong>Hello World</strong>',
        }
        return self.render_to_response(context_test)
    ############################### /VIEW

    ############################### TEMPLATE
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
    ############################### /TEMPLATE
```

This will render:

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>
            It works!
        </title>
        <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet">
        <link href="http://getbootstrap.com/examples/starter-template/starter-template.css" rel="stylesheet">
        <script src="//code.jquery.com/jquery-1.10.2.min.js" type="text/javascript">
        </script>
        <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js" type="text/javascript">
        </script>
    </head>
    <body>
        <div class="navbar navbar-inverse navbar-fixed-top">
            <div class="container">
                <div class="navbar-header">
                    <a class="navbar-brand" href="#">
                        Temper Test
                    </a>
                </div>
            </div>
        </div>
        <div class="container">
            <div class="starter-template">
                <h1>
                    Hello World!
                </h1>
                <p>
                    The is just an example template using <strong>Temper</strong>, <strong>Django</strong> and <strong>Bootstrap</strong>!
                </p>
                <p>
                    You passed &#39;&lt;strong&gt;Hello World&lt;/strong&gt;&#39; as context variable &#39;test&#39;
                </p>
            </div>
        </div>
    </body>
</html>
```
