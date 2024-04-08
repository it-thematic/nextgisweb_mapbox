from nextgisweb.resource import Widget

from .model import MapboxGlyph


class GlyphWidget(Widget):
    resource = MapboxGlyph
    operation = ('create', 'update')
    amdmod = 'ngw-glyphs/Widget'
