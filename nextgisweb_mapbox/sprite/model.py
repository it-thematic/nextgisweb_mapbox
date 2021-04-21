# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os.path
import tempfile
import zipfile

from shutil import copyfileobj

from nextgisweb import db
from nextgisweb.env import env
from nextgisweb.file_storage import FileObj
from nextgisweb.models import declarative_base
from nextgisweb.render import on_style_change
from nextgisweb.resource import Resource, ResourceGroup, Serializer, SerializedProperty
from nextgisweb.resource.exception import ValidationError
from nextgisweb.resource.scope import ResourceScope

from ..helper import get_mapbox_helper
from .util import _


Base = declarative_base()


class MapboxSprite(Base, Resource):
    identity = 'mapbox_sprite'
    cls_display_name = _("Mapbox sprite")

    sprite_fileobj_id = db.Column(db.ForeignKey(FileObj.id), nullable=True)

    sprite_fileobj = db.relationship(FileObj, cascade='all')

    @classmethod
    def check_parent(cls, parent):
        return isinstance(parent, ResourceGroup)


class SpriteAttr(SerializedProperty):

    def setter(self, srlzr, value):
        srcfile, srcmeta = env.file_upload.get_filename(value['id'])
        fileobj = env.file_storage.fileobj(component='sprite')
        srlzr.obj.sprite_fileobj = fileobj
        dstfile = env.file_storage.filename(fileobj, makedirs=True)

        with open(srcfile, 'r+b') as fs, open(dstfile, 'w+b') as fd:
            copyfileobj(fs, fd)

        sprite_dir = get_mapbox_helper().sprite_dir

        if not zipfile.is_zipfile(dstfile):
            raise ValidationError(_("Sprite must be a *.zip archive"))

        with tempfile.TemporaryDirectory():
            with zipfile.ZipFile(dstfile) as zip_sprite:
                for sprite_name in zip_sprite.namelist():
                    if os.path.exists(os.path.join(sprite_dir, sprite_name)):
                        raise ValidationError(_("Sprite with name `%s` already exists" % sprite_name))
                zip_sprite.extractall(path=sprite_dir)
        on_style_change.fire(srlzr.obj)


class MapboxSpriteSerializer(Serializer):
    identity = MapboxSprite.identity
    resclass = MapboxSprite

    sprite = SpriteAttr(read=None, write=ResourceScope.update)
