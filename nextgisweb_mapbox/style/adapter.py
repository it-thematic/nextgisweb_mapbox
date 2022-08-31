# coding: utf-8
from nextgisweb.webmap.adapter import WebMapAdapter
from .util import _


@WebMapAdapter.registry.register
class MVTAdapter:
    identity = 'mvt'
    mid = 'ngw-style/MVTAdapter'
    display_name = _("MVT")
