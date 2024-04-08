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
from ..glyphs.model import MapboxGlyph
from ..helper import get_mapbox_helper


def glyphs(resource, request):
    font_names = request.matchdict['fontstack'].split(',')
    if not font_names:
        return Response(status=404)

    range_from = request.matchdict['from']
    range_to = request.matchdict['to']
    dstfile = env.file_storage.filename(resource.glyph_fileobj, makedirs=False)
    with zipfile.ZipFile(dstfile) as fzip:
        for font_name in font_names:
            if font_name in set((fzipname.split('/')[0] for fzipname in fzip.namelist())):
                glyphs_dir = get_mapbox_helper().glyphs_dir
                return FileResponse(os.path.join(glyphs_dir, font_name,
                                                 '%s-%s.pbf' % (min(range_from, range_to), max(range_from, range_to))))
    return Response(status=404, body='The Fonts not available' % font_name)


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
    style_dict = loads(resource.style)

    sprite_url = request.route_url('mapbox.sprite', id=resource.sprite_id, format='') if resource.sprite else None
    if sprite_url:
        style_dict['sprite'] = sprite_url

    glyphs_url = request.route_url('mapbox.glyphs', id=resource.glyphs_id) if resource.glyphs else None
    if glyphs_url:
        style_dict['glyphs'] = glyphs_url

    response = Response(
        body=dumps(style_dict, ensure_ascii=False, indent=4),
        charset='utf-8',
        content_type='application/json',
        content_disposition='attachment; filename=%d.json' % resource.id
    )
    return response


def setup_pyramid(comp, config):
    config.add_route(
        'mapbox.style_json',
        '/api/resource/{id}/json',
        types=dict(id=int),
        get=style_json
    )

    config.add_route(
        'mapbox.sprite',
        '/api/resource/{id}/sprite{format:any}',
        types=dict(id=int, format=str),
        get=sprite
    )

    config.add_route(
        'mapbox.glyphs',
        '/api/resource/{id}/glyphs',
        types=dict(id=int, ),
        get=glyphs
        )

    config.add_route(
        'mapbox.glyphs.fonts',
        '/api/resource/{id:int}/glyphs/{fontstack:str}/{from:int}-{to:int}.pbf',
        get=glyphs
    )

