# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os

from json import loads, dumps
from nextgisweb import db
from nextgisweb.models import declarative_base
from nextgisweb.render import on_style_change
from nextgisweb.resource import Resource, ResourceGroup, Serializer, SerializedProperty
from nextgisweb.resource.exception import ValidationError
from nextgisweb.resource.scope import ResourceScope

from nextgisweb_mapbox.mixinx import TileserverGLMixin
from nextgisweb_mapbox.sprite.model import MapboxSprite
from nextgisweb_mapbox.glyph.model import MapboxGlyph
from .util import _

Base = declarative_base()


class MapboxStyle(Base, Resource, TileserverGLMixin):
    identity = 'mapbox_style'
    cls_display_name = _('Mapbox style')

    style = db.Column(db.Unicode, nullable=False)
    sprite_id = db.Column(db.ForeignKey(MapboxSprite.id), nullable=True)
    glyphs_id = db.Column(db.ForeignKey(MapboxGlyph.id), nullable=True)

    sprite = db.relationship(MapboxSprite, foreign_keys=sprite_id)
    glyphs = db.relationship(MapboxGlyph, foreign_keys=glyphs_id)

    @classmethod
    def check_parent(cls, parent):
        return isinstance(parent, ResourceGroup)

    def __init__(self, *args, **kwargs):
        super(MapboxStyle, self).__init__(*args, **kwargs)
        # self._init_directories()


class StyleAttr(SerializedProperty):

    def setter(self, srlzr, value):
        tsgl_basedir = srlzr.obj.base_dir
        if srlzr.obj.pk is not None:
            old_style = loads(srlzr.obj.style)
            old_style_name = old_style.setdefault('name', srlzr.obj.display_name)
            if os.path.exists(os.path.join(tsgl_basedir, old_style_name + '.json')):
                os.unlink(os.path.join(tsgl_basedir, old_style_name + '.json'))

        mb_style = loads(value)
        style_name = mb_style.setdefault('name', srlzr.obj.display_name)
        mb_style['name'] = style_name
        if os.path.exists(os.path.join(tsgl_basedir, style_name + '.json')):
            raise ValidationError(_("Style with name '%s' exists" % style_name))
        with open(os.path.join(tsgl_basedir, style_name + '.json'), mode='w', encoding='utf-8') as fs:
            fs.write(dumps(mb_style, ensure_ascii=True, indent=4))
        super(StyleAttr, self).setter(srlzr, dumps(mb_style, ensure_ascii=True))
        on_style_change.fire(srlzr.obj)


class MapboxStyleSerializer(Serializer):
    identity = MapboxStyle.identity
    resclass = MapboxStyle

    style = StyleAttr(read=ResourceScope.read, write=ResourceScope.update)
