from compressor.templatetags.compress import CompressorMixin
from compressor.templatetags.compress import OUTPUT_FILE

from temper import Temper
from temper.utils import block


class Compressor(CompressorMixin):
    def compress(self, kind, mode, body):
        forced = False
        mode = mode or OUTPUT_FILE
        context = {
            'original_content': body,
        }
        return self.render_compressed(context, kind, mode, forced=forced)

    def get_original_content(self, context):
        return context['original_content']


class TemperCompressorMixin:
    @block
    def compress(self, kind):
        if not hasattr(self, 'compressor'):
            self.compressor = Compressor()

        self.stack.append(self.tree)
        self.tree = ''
        yield
        tree = self.compressor.compress(kind, None, self.tree)
        self.tree = self.stack.pop() + tree


class CompressorTemper(TemperCompressorMixin, Temper):
    pass
