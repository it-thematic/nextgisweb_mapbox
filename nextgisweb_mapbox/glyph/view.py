# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nextgisweb.resource import Widget

from .model import MapboxGlyph


class GlyphWidget(Widget):
    resource = MapboxGlyph
    operation = ('create', 'update')
    amdmod = 'ngw-glyph/Widget'
