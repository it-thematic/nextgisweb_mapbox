# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals, print_function, absolute_import
import os
import logging

from nextgisweb.env import Env, setenv

logger = logging.getLogger(__name__)


def pkginfo():
    components = (
        'style',
        'sprite',
        'glyph'
    )

    return dict(
        components={
            comp: dict(
                module='nextgisweb_mapbox.{}'.format(comp)) for comp in components
        }
    )


def amd_packages():
    return (
        ('mapbox-gl-style-spec', 'nextgisweb_mapbox:amd_packages/@mapbox/mapbox-gl-style-spec'),
        ('ngw-style', 'nextgisweb_mapbox:style/amd/ngw-style'),
        ('ngw-sprite', 'nextgisweb_mapbox:sprite/amd/ngw-sprite'),
        ('ngw-glyph', 'nextgisweb_mapbox:glyph/amd/ngw-glyph')
    )
