from nextgisweb.env import _
from nextgisweb.webmap.adapter import WebMapAdapter


@WebMapAdapter.registry.register
class MVTAdapter:
    identity = 'mvt'
    mid = 'ngw-style/MVTAdapter'
    display_name = _("MVT Vector Tiles")
