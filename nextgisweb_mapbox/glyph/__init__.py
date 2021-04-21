# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from nextgisweb.component import Component, require

from .model import Base
from .util import COMP_ID


class SpriteComponent(Component):
    identity = COMP_ID
    metadata = Base.metadata

    @require('resource')
    def setup_pyramid(self, config):
        from . import view, api
