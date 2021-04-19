# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os

from json import loads

from nextgisweb.env import env
from nextgisweb.tmsclient.session_keeper import get_session
from requests.exceptions import ConnectTimeout, ReadTimeout
from six.moves.urllib.parse import urlparse


class TileserverGLMixin:

    def _init_directories(self):
        # Initialize style, sprite, glyphs directories
        self.base_url = env.mapbox.options["tileserver.host"]

        ts_config = env.mapbox.options["tileserver.config"]
        if not os.path.exists(ts_config):
            raise ValueError("Tileserver configuration file don't exists!")
        with open(ts_config, encoding='utf-8') as f:
            ts_config_dict = loads(f.read())
        ts_options = ts_config_dict.setdefault('options', dict())

        _root_dir = ts_options.setdefault('paths', dict()).get('root', None)
        if _root_dir:
            _root_dir = os.path.abspath(_root_dir)
        else:
            _root_dir = os.path.dirname(env.mapbox.options["tileserver.config"])

        self.base_dir = _root_dir
        self.style_dir = os.path.join(_root_dir, ts_options['paths'].get('styles', ''))
        self.sprite_dir = os.path.join(_root_dir, ts_options['paths'].get('sprites', ''))
        self.glyph_dir = os.path.join(_root_dir, ts_options['paths'].get('fonts', ''))

    def _request(self, url, params=None):
        _session = get_session('mapbox', urlparse(self.base_url).scheme)
        try:
            res = _session.get(
                url,
                params=params,
                timeout=env.mapbox.options["tileserver.timeout"]
            )
        except (ConnectTimeout, ReadTimeout) as e:
            env.mapbox.logger.error(e)
        else:
            res.raise_for_status()
            return res.json()

    def load_styles(self):
        data = self._request(self.base_url + '/styles.json')
        if data is not None:
            return [style['id'] for style in data]

    def load_glyph(self):
        return self._request(self.base_url + '/fonts.json')


