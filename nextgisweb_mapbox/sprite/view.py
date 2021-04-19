# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nextgisweb.resource import Widget

from .model import MapboxSprite


class SpriteWidget(Widget):
    resource = MapboxSprite
    operation = ('create', 'update')
    amdmod = 'ngw-sprite/Widget'
