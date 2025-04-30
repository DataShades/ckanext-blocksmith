import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
import ckan.types as types

from ckanext.blocksmith.middleware import render_page_if_exists


@tk.blanket.blueprints
@tk.blanket.actions
@tk.blanket.auth_functions
@tk.blanket.validators
@tk.blanket.helpers
class BlocksmithPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IMiddleware, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_resource("assets", "blocksmith")

    # IMiddleware
    def make_middleware(self, app: types.CKANApp, _) -> types.CKANApp:
        app.after_request(render_page_if_exists)
        return app
