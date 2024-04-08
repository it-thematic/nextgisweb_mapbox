from nextgisweb.env import Component
from nextgisweb.lib.config import Option, OptionAnnotations


class StyleComponent(Component):

    def setup_pyramid(self, config):
        from . import view, api, adapter  # noqa

        view.setup_pyramid(self, config)
        api.setup_pyramid(self, config)

    def maintenance(self):
        super(StyleComponent, self).maintenance()
        self.cleanup()

    def cleanup(self):
        self.logger.info('Cleaning up style storage...')

    option_annotations = OptionAnnotations((
        (Option("tileserver.host", str, default="http://localhost:8080", doc="Host of tileserver_gl")),
        (Option("tileserver.timeout", float, default=5.0, doc="Timeout to tileserver_gl")),
        (Option("tileserver.config", str, required=True, doc="Path to tileserver_gl's configuration json-file"))
    ))
