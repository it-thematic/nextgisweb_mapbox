# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import tempfile
import zipfile

from nextgisweb import db
from nextgisweb.env import env
from nextgisweb.file_storage import FileObj
from nextgisweb.models import declarative_base
from nextgisweb.resource import Resource, ResourceGroup, Serializer, SerializedProperty
from nextgisweb.resource.exception import ValidationError
from nextgisweb.resource.scope import ResourceScope

from nextgisweb_mapbox.mixinx import TileserverGLMixin
from .util import _


Base = declarative_base()


class MapboxSprite(Base, Resource, TileserverGLMixin):
    identity = 'mapbox_sprite'
    cls_display_name = _("Mapbox sprite")

    sprite_fileobj_id = db.Column(db.ForeignKey(FileObj.id), nullable=True)

    sprite_fileobj = db.relationship(FileObj, cascade='all')

    @classmethod
    def check_parent(cls, parent):
        return isinstance(parent, ResourceGroup)


class SpriteAttr(SerializedProperty):

    def setter(self, srlzr, value):
        super(SpriteAttr, self).setter(srlzr, value)
        datafile, metafile = env.file_upload.get_filename(value['id'])

        if not zipfile.is_zipfile(datafile):
            raise ValidationError(_("Sprite must be a *.zip archive"))

        with tempfile.TemporaryDirectory as tmp:
            with zipfile.ZipFile(datafile) as zip_sprite:
                zip_sprite.extractall(path=tmp)


class MapboxSpriteSerializer(Serializer):
    identity = MapboxSprite.identity
    resclass = MapboxSprite

    sprite = SpriteAttr(read=ResourceScope.read, write=ResourceScope.update)
