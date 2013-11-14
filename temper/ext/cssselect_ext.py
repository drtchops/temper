import cssselect

from temper import Temper


class TemperCSSSelectMixin:
    def __getitem__(self, key):
        return self.tag(key)

    def tag(self, selector, **attrs):
        parsed = cssselect.parse(selector)
        if len(parsed) > 1:
            raise ValueError('Cannot specify more than 1 tag.')

        tag_name = None
        kwargs = {}
        item = parsed[0].parsed_tree
        while item:
            if item.__class__ is cssselect.parser.Hash:
                kwargs['id'] = item.id
                item = item.selector
            elif item.__class__ is cssselect.parser.Class:
                kwargs['class_'] = ' '.join([
                    kwargs.get('class_', ''), item.class_name]).strip()
                item = item.selector
            elif item.__class__ is cssselect.parser.Attrib:
                kwargs[item.attrib] = item.value
                item = item.selector
            elif item.__class__ is cssselect.parser.Element:
                tag_name = item.element
                break
            else:
                raise ValueError('Unsupported selector: %s.' % selector)
        kwargs.update(attrs)

        return self.settings.tag_class(tag_name, self, **kwargs)


class CSSSelectTemper(TemperCSSSelectMixin, Temper):
    pass
