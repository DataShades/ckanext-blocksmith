ckan.module("blocksmith-slugify", function ($, _) {
    "use strict";

    return {
        options: {},

        initialize: function () {
            this.el.slug()
        }
    };
});
