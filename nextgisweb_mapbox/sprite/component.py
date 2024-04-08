from nextgisweb.env import Component


class SpriteComponent(Component):
    def setup_pyramid(self, config):
        from . import view  # noqa
