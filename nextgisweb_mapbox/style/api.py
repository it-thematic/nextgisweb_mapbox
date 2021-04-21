# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import os.path
import zipfile

from json import loads, dumps
from re import match

from nextgisweb.env import env
from nextgisweb.resource.scope import ResourceScope
from nextgisweb.resource.view import resource_factory
from pyramid.response import FileResponse, Response

from .model import MapboxStyle
from ..sprite.model import MapboxSprite
from ..glyph.model import MapboxGlyph
from ..helper import get_mapbox_helper


def glyphs(resource, request):
    font_name = request.matchdict['fontstack']
    if not font_name:
        return Response(status=404)

    range_from = request.matchdict['from']
    range_to = request.matchdict['to']
    dstfile = env.file_storage.filename(resource.glyph_fileobj, makedirs=False)
    with zipfile.ZipFile(dstfile) as fzip:
        if font_name not in set((fzipname.split('/')[0] for fzipname in fzip.namelist())):
            return Response(status=404, body='The Font `%s` is not available' % font_name)
    glyphs_dir = get_mapbox_helper().glyphs_dir
    return FileResponse(os.path.join(glyphs_dir, font_name, '%s-%s.pbf' % (min(range_from, range_to), max(range_from, range_to))))


def sprite(resource, request):
    sprite_name = request.matchdict['format']
    if not sprite_name:
        return Response(status=404)
    dstfile = env.file_storage.filename(resource.sprite_fileobj, makedirs=False)

    sprite_match = match(r'(?P<scale>@\d+x)?\.(?P<format>(png|json))', sprite_name)
    if sprite_match is None:
        return Response(status=404)

    sprite_groups = sprite_match.groupdict()
    sp_scale = sprite_groups['scale']
    sp_format = sprite_groups['format']

    with zipfile.ZipFile(dstfile) as fzip:
        for zipname in (fzname for fzname in fzip.namelist() if fzname.endswith(sp_format)):
            if not sp_scale or sp_scale in zipname:
                sprite_dir = get_mapbox_helper().sprite_dir
                return FileResponse(os.path.join(sprite_dir, zipname))


def style_json(resource, request):
    request.resource_permission(ResourceScope.read)

    sprite_url = request.route_url('mapbox.sprite', id=resource.sprite_id, format='') if resource.sprite else None
    glyphs_url = request.route_url('mapbox.glyphs', id=resource.glyphs_id, fontstack='', range='', format='') if resource.glyphs else None

    style_dict = loads(resource.style)
    style_dict['sprite'] = sprite_url if sprite_url else "{style}"
    style_dict['glyphs'] = glyphs_url + "/{fontstack}/{range}.pbf" if glyphs_url else "{fontstack}/{range}.pbf"

    response = Response(
        body=dumps(style_dict, ensure_ascii=False, indent=4),
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

    config.add_route(
        'mapbox.sprite', '/api/resource/{id}/sprite{format:.*?}', factory=resource_factory) \
        .add_view(sprite, context=MapboxSprite, request_method='GET')

    config.add_route(
        'mapbox.glyphs', '/api/resource/{id}/glyphs', factory=resource_factory)

    config.add_route(
        'mapbox.glyphs.fonts', '/api/resource/{id}/glyphs/{fontstack}/{from}-{to}.pbf', factory=resource_factory) \
        .add_view(glyphs, context=MapboxGlyph, request_method='GET')
