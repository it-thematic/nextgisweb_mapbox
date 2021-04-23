# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os

from json import loads, dumps
from nextgisweb import db
from nextgisweb.models import declarative_base
from nextgisweb.render import on_style_change
from nextgisweb.resource import Resource, ResourceGroup, Serializer, SerializedProperty, SerializedResourceRelationship
from nextgisweb.resource.exception import ValidationError
from nextgisweb.resource.scope import ResourceScope

from nextgisweb_mapbox.helper import get_mapbox_helper
from nextgisweb_mapbox.sprite.model import MapboxSprite
from nextgisweb_mapbox.glyphs.model import MapboxGlyph

from .util import _

Base = declarative_base()


class MapboxStyle(Base, Resource):
    identity = 'mapbox_style'
    cls_display_name = _('Mapbox style')

    style = db.Column(db.Unicode, nullable=False)
    sprite_id = db.Column(db.ForeignKey(MapboxSprite.id, ondelete="SET NULL"), nullable=True)
    glyphs_id = db.Column(db.ForeignKey(MapboxGlyph.id, ondelete="SET NULL"), nullable=True)

    sprite = db.relationship(MapboxSprite, foreign_keys=sprite_id, cascade=False, cascade_backrefs=False)
    glyphs = db.relationship(MapboxGlyph, foreign_keys=glyphs_id, cascade=False, cascade_backrefs=False)

    @classmethod
    def check_parent(cls, parent):
        return isinstance(parent, ResourceGroup)


class StyleAttr(SerializedProperty):

    def setter(self, srlzr, value):
        style_dir = get_mapbox_helper().style_dir
        if srlzr.obj.id is not None:
            old_style = loads(srlzr.obj.style)
            old_style_name = old_style.setdefault('name', srlzr.obj.display_name)
            if os.path.exists(os.path.join(style_dir, old_style_name + '.json')):
                os.unlink(os.path.join(style_dir, old_style_name + '.json'))

        mb_style = loads(value)
        style_name = mb_style.setdefault('name', srlzr.obj.display_name)
        mb_style['name'] = style_name

        if os.path.exists(os.path.join(style_dir, style_name + '.json')):
            raise ValidationError(_("Mapbox Style with name '%s' exists") % style_name)
        with open(os.path.join(style_dir, style_name + '.json'), mode='w', encoding='utf-8') as fs:
            fs.write(dumps(mb_style, ensure_ascii=True, indent=4))
        super(StyleAttr, self).setter(srlzr, dumps(mb_style, ensure_ascii=True))
        on_style_change.fire(srlzr.obj)


class MapboxStyleSerializer(Serializer):
    identity = MapboxStyle.identity
    resclass = MapboxStyle

    style = StyleAttr(read=ResourceScope.read, write=ResourceScope.update)
    sprite = SerializedResourceRelationship(read=ResourceScope.read, write=ResourceScope.update)
    glyphs = SerializedResourceRelationship(read=ResourceScope.read, write=ResourceScope.update)
