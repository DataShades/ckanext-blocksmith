ckan.module("blocksmith-snippet-form", function ($) {
    return {
        initialize: function () {
            $.proxyAll(this, /_/);

            this.titleInput = document.getElementById("title");
            this.nameInput = document.getElementById("name");

            // add event listeners
            this.titleInput.addEventListener("change", this._onTitleChange);
            $(document).on('input', 'input[name="argument[]"]', this._onArgumentInput);
        },

        _onArgumentInput: function (event) {
            const input = event.target;
            const value = input.value;

            // Only allow valid variable name characters
            const sanitizedValue = value.replace(/[^a-zA-Z0-9_]/g, '');

            // Ensure first character is letter/underscore
            if (sanitizedValue && !/^[a-zA-Z_]/.test(sanitizedValue)) {
                input.value = '_' + sanitizedValue;
            } else {
                input.value = sanitizedValue;
            }
        },

        _onTitleChange: function (event) {
            if (this.nameInput.value.length > 0) {
                return;
            }

            const value = this.titleInput.value;
            const slug = value
                .toLowerCase()
                .replace(/\s+/g, '-')           // Replace spaces with -
                .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
                .replace(/\-\-+/g, '-')         // Replace multiple - with single -
                .replace(/^-+/, '')             // Trim - from start
                .replace(/-+$/, '');            // Trim - from end;

            this.nameInput.value = slug;
        },
    };
});
