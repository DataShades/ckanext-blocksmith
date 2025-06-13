ckan.module("blocksmith-codemirror", function ($, _) {
    "use strict";

    return {
        options: {
            editable: true,
        },
        initialize: function () {
           $.proxyAll(this, /_/);
           CodeMirrorEditor.EditorFromTextArea(this.el[0], this.options.editable);
        }
    };
});
