# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import nextgisweb.dynmenu as dm

from nextgisweb.resource import Resource, Widget

from .model import MapboxStyle
from .util import _


class StyleWidget(Widget):
    resource = MapboxStyle
    operation = ('create', 'update')
    amdmod = 'ngw-style/Widget'


def setup_pyramid(comp, config):

    class LayerMenuExt(dm.DynItem):
        def build(self, args):
            if isinstance(args.obj, MapboxStyle):
                yield dm.Label("mapbox_style", _("Mapbox style"))
                yield dm.Link(
                    "mapbox_style/json",
                    _("Mapbox style"),
                    lambda args: args.request.route_url(
                        "mapbox.style_json", id=args.obj.id
                    ),
                )

    Resource.__dynmenu__.add(LayerMenuExt())
