# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from nextgisweb.component import Component, require
from nextgisweb.lib.config import Option

from .model import Base
from .util import COMP_ID


class StyleComponent(Component):
    identity = COMP_ID
    metadata = Base.metadata

    @require('resource')
    def setup_pyramid(self, config):
        from . import view, api

        view.setup_pyramid(self, config)
        api.setup_pyramid(self, config)

    option_annotations = (
        (Option("tileserver.host", default="http://localhost:8080", doc="Host of tileserver_gl")),
        (Option("tileserver.timeout", float, default=5.0, doc="Timeout to tileserver_gl")),
        (Option("tileserver.config", required=True, doc="Path to tileserver_gl's configuration json-file"))
    )
