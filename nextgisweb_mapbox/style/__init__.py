# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import os

from nextgisweb.component import Component, require
from nextgisweb.lib.config import Option

from .model import Base, MapboxStyle
from .util import COMP_ID


class StyleComponent(Component):
    identity = COMP_ID
    metadata = Base.metadata

    @require('resource')
    def setup_pyramid(self, config):
        from . import view, api, adapter

        view.setup_pyramid(self, config)
        api.setup_pyramid(self, config)

    def maintenance(self):
        super(StyleComponent, self).maintenance()
        self.cleanup()

    def cleanup(self):
        self.logger.info('Cleaning up style storage...')

    option_annotations = (
        (Option("tileserver.host", default="http://localhost:8080", doc="Host of tileserver_gl")),
        (Option("tileserver.timeout", float, default=5.0, doc="Timeout to tileserver_gl")),
        (Option("tileserver.config", required=True, doc="Path to tileserver_gl's configuration json-file"))
    )
