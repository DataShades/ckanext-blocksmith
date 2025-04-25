import ckan.plugins as plugins
import ckan.plugins.toolkit as tk


@tk.blanket.blueprints
@tk.blanket.actions
@tk.blanket.auth_functions
class BlocksmithPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer
    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_resource("assets", "blocksmith")
