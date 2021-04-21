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


class MapboxGlyph(Base, Resource):
    identity = 'mapbox_glyph'
    cls_display_name = _("Mapbox glyph")

    glyph_fileobj_id = db.Column(db.ForeignKey(FileObj.id), nullable=True)

    glyph_fileobj = db.relationship(FileObj, cascade='all')

    @classmethod
    def check_parent(cls, parent):
        return isinstance(parent, ResourceGroup)


class GlyphAttr(SerializedProperty):

    def setter(self, srlzr, value):
        srcfile, srcmeta = env.file_upload.get_filename(value['id'])
        fileobj = env.file_storage.fileobj(component='glyphs')
        srlzr.obj.glyph_fileobj = fileobj
        dstfile = env.file_storage.filename(fileobj, makedirs=True)

        with open(srcfile, 'r+b') as fs, open(dstfile, 'w+b') as fd:
            copyfileobj(fs, fd)

        glyphs_dir = get_mapbox_helper().glyphs_dir

        if not zipfile.is_zipfile(dstfile):
            raise ValidationError(_("Sprite must be a *.zip archive"))

        with tempfile.TemporaryDirectory():
            with zipfile.ZipFile(dstfile) as zip_sprite:
                for sprite_name in zip_sprite.namelist():
                    if os.path.exists(os.path.join(glyphs_dir, sprite_name)):
                        raise ValidationError(_("Sprite with name `%s` already exists" % sprite_name))
                zip_sprite.extractall(path=glyphs_dir)
        on_style_change.fire(srlzr.obj)


class MapboxGlyphsSerializer(Serializer):
    identity = MapboxGlyph.identity
    resclass = MapboxGlyph

    glyphs = GlyphAttr(read=None, write=ResourceScope.update)
