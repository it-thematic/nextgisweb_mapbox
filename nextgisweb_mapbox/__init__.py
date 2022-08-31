# -*- coding: utf-8 -*-
from nextgisweb.env import Env, setenv
from nextgisweb.lib.logging import logger


def pkginfo():
    components = (
        'style',
        'sprite',
        'glyphs'
    )

    return dict(
        components={
            comp: dict(
                module='nextgisweb_mapbox.{}'.format(comp)) for comp in components
        }
    )


def amd_packages():
    return (
        ('ngw-style', 'nextgisweb_mapbox:style/amd/ngw-style'),
        ('ngw-sprite', 'nextgisweb_mapbox:sprite/amd/ngw-sprite'),
        ('ngw-glyphs', 'nextgisweb_mapbox:glyphs/amd/ngw-glyphs')
    )
