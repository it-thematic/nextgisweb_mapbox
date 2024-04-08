import os
from json import loads

import requests

from nextgisweb.env import env
from nextgisweb.lib.logging import logger
from requests.exceptions import Timeout


class TileserverGLHelper:

    def __init__(self):
        # Initialize style, sprite, glyphs directories
        self.base_url = env.style.options["tileserver.host"]

        ts_config = env.style.options["tileserver.config"]
        if not os.path.exists(ts_config):
            raise ValueError("Tileserver configuration file don't exists!")
        with open(ts_config, encoding='utf-8') as f:
            ts_config_dict = loads(f.read())
        ts_options = ts_config_dict.setdefault('options', dict())

        _root_dir = ts_options.setdefault('paths', dict()).get('root', None)

        self.base_dir = os.path.dirname(env.style.options["tileserver.config"])
        if _root_dir:
            self.base_dir = os.path.join(self.base_dir, _root_dir)
        self.style_dir = os.path.join(self.base_dir, ts_options['paths'].get('styles', ''))
        self.sprite_dir = os.path.join(self.base_dir, ts_options['paths'].get('sprites', ''))
        self.glyphs_dir = os.path.join(self.base_dir, ts_options['paths'].get('fonts', ''))

    def _request(self, url, params=None):

        try:
            res = requests.get(
                url,
                params=params,
                timeout=env.mapbox.options["tileserver.timeout"]
            )
        except Timeout as e:
            logger.error(e)
        else:
            res.raise_for_status()
            return res.json()

    def load_styles(self):
        data = self._request(self.base_url + '/styles.json')
        if data is not None:
            return [style['id'] for style in data]

    def load_glyph(self):
        return self._request(self.base_url + '/fonts.json')


MAPBOX_HELPER = None


def get_mapbox_helper():
    global MAPBOX_HELPER
    if MAPBOX_HELPER is None:
        MAPBOX_HELPER = TileserverGLHelper()
    return MAPBOX_HELPER


__all__ = ['get_mapbox_helper']
