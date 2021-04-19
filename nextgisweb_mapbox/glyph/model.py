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

from nextgisweb_mapbox.style.model import TileserverGLMixin
from .util import _


Base = declarative_base()


class MapboxGlyph(Base, Resource, TileserverGLMixin):
    identity = 'mapbox_glyph'
    cls_display_name = _("Mapbox glyph")

    glyph_fileobj_id = db.Column(db.ForeignKey(FileObj.id), nullable=True)

    glyph_fileobj = db.relationship(FileObj, cascade='all')

    @classmethod
    def check_parent(cls, parent):
        return isinstance(parent, ResourceGroup)


class GlyphAttr(SerializedProperty):

    def setter(self, srlzr, value):
        super(GlyphAttr, self).setter(srlzr, value)
        datafile, metafile = env.file_upload.get_filename(value['id'])

        if not zipfile.is_zipfile(datafile):
            raise ValidationError(_("Sprite must be a *.zip archive"))

        with tempfile.TemporaryDirectory as tmp:
            with zipfile.ZipFile(datafile) as zip_sprite:
                zip_sprite.extractall(path=tmp)


class MapboxGlyphSerializer(Serializer):
    identity = MapboxGlyph.identity
    resclass = MapboxGlyph

    sprite = GlyphAttr(read=ResourceScope.read, write=ResourceScope.update)
