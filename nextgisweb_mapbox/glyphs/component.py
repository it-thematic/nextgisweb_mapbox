from nextgisweb.env import Component


class GlyphsComponent(Component):
    def setup_pyramid(self, config):
        from . import view  # noqa
