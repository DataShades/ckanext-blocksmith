The `GrapeJS` has a plugin system, that allows you to extend the editor with new features.

You can find more information about the plugins in the [GrapeJS documentation](https://grapesjs.com/docs/modules/Plugins.html).


### Override the default plugins and options

You can change the list of plugins and options for the GrapesJS editor that we use in the extension. For this, you have to initialize a regular CKAN JS module first.

You can learn more about this in the [CKAN documentation](https://docs.ckan.org/en/latest/contributing/frontend/javascript-module-tutorial.html).

???+ note
    Your JS module, that overrides the default plugins and options, must be loaded after the `blocksmith-editor.js` file. It means, that your extension should be loaded after the `blocksmith` extension in the `ckan.plugins` in the config file.

    For example:
    ```ini
    ckan.plugins =
            ...
            blocksmith
            your_extension
            ...
    ```

Imagine you already have a basic JS module, that is already being initialized.

```javascript
ckan.module('my-module', function (jQuery) {
    return {
        initialize: function () {
            console.log('I am a module');
        }
    };
});
```

Now you can extend update the GrapeJS initialization options by adding the following to the module.

```javascript
ckan.module('my-module', function (jQuery) {
    Object.assign(ckan.sandbox().blocksmith, {
        plugins: ["my-plugin"],
        pluginsOpts: {
            "my-plugin": {
                // ...
            }
        }
    });

    return {
        initialize: function () {
            console.log('I am a module');
        }
    };
});
```

This will completely override the list of plugins and options for the GrapesJS editor.

If you want to add a new plugin, you can do so by adding it to the list of plugins. For example, if you want to add the `grapesjs-my-plugin` plugin, you can do so by adding it to the list of plugins.

```javascript
ckan.sandbox().blocksmith.plugins.push("grapesjs-my-plugin");
```
