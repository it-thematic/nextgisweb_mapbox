# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
from json import loads

from nextgisweb.resource.scope import ResourceScope
from nextgisweb.resource.view import resource_factory
from pyramid.response import Response

from .model import MapboxStyle


def style_json(resource, request):
    request.resource_permission(ResourceScope.read)

    sprite_url = request.route_url('mapbox.sprite', id=resource.sprite) if resource.sprite else None
    glyphs_url = request.route_url('mapbox.glyphs', id=resource.glyphs) if resource.glyphs else None

    style_dict = loads(resource.style)
    style_dict['sprite'] = sprite_url if sprite_url else "{style}"
    style_dict['glyphs'] = glyphs_url + "{fontstack}/{range}.pbf" if glyphs_url else "{fontstack}/{range}.pbf"

    response = Response(
        body=resource.style,
        charset='utf-8',
        content_type='application/json',
        content_disposition='attachment; filename=%d.json' % resource.id
    )
    return response


def setup_pyramid(comp, config):
    config.add_route(
        'mapbox.style_json', '/api/resource/{id}/json',
        factory=resource_factory) \
        .add_view(style_json, context=MapboxStyle, request_method='GET')
