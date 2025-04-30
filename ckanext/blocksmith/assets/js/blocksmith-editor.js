/**
 * Initialize the GrapesJS editor
 */
ckan.module("blocksmith-editor", function ($) {
    return {
        constants: {
            fieldUrlID: "save-page-url",
            fieldTitleID: "save-page-title",
            fieldFullscreenID: "save-page-fullscreen",
            fieldPublishedID: "save-page-published",
            fieldConfirmSaveID: "confirm-save-page",
        },
        saveIcon: `
            <svg width="19" height="19" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                <path fill="currentColor" d="M433.9 129.9l-83.9-83.9A48 48 0 0 0 316.1 32H48C21.5 32 0 53.5 0 80v352c0 26.5 21.5 48 48 48h352c26.5 0 48-21.5 48-48V163.9a48 48 0 0 0 -14.1-33.9zM224 416c-35.3 0-64-28.7-64-64 0-35.3 28.7-64 64-64s64 28.7 64 64c0 35.3-28.7 64-64 64zm96-304.5V212c0 6.6-5.4 12-12 12H76c-6.6 0-12-5.4-12-12V108c0-6.6 5.4-12 12-12h228.5c3.2 0 6.2 1.3 8.5 3.5l3.5 3.5A12 12 0 0 1 320 111.5z"/>
            </svg>
        `,
        getModalTemplate: function (page) {
            return `
                <div style="padding: 10px;">
                    <div class="form-group control-medium">
                        <label class="form-label">Title</label><br>
                    <input type="text" id="${this.constants.fieldTitleID}" class="form-control" value="${page.title || ""}" />
                </div>

                <div class="form-group control-medium">
                    <label class="form-label">URL</label><br>
                    <input type="text" id="${this.constants.fieldUrlID}" class="form-control" value="${page.url || ""}" />
                </div>

                <div class="form-group control-medium">
                    <label class="form-label">Full screen</label><br>
                    <select id="${this.constants.fieldFullscreenID}">
                        <option value="no" ${page.fullscreen ? "selected" : ""}>No</option>
                        <option value="yes" ${page.fullscreen ? "selected" : ""}>Yes</option>
                    </select>
                </div>

                <div class="form-group control-medium">
                    <label class="form-label">Published</label><br>
                    <input type="checkbox" value="yes" id="${this.constants.fieldPublishedID}" ${page.published ? "checked" : ""} />
                </div>

                <div class="form-actions">
                    <button id="${this.constants.fieldConfirmSaveID}" class="btn btn-default">Save</button>
                </div>
            </div>
        `
        },
        options: {
            pageId: null,
            defaultContent: null,
            test: null
        },
        initialize: function () {
            $.proxyAll(this, /_/);

            this.page = null;
            this.editor = null;

            this._loadPageData();
        },

        _loadPageData: function () {
            if (!this.options.pageId) {
                return this._initGrapesJS();
            }

            $.ajax({
                method: "GET",
                url: this.sandbox.client.url("/api/action/blocksmith_get_page"),
                data: { id: this.options.pageId },
                success: (resp) => {
                    this.page = resp.result;
                    this._initGrapesJS();
                },
                error: (_) => {
                    this._initGrapesJS();
                }
            });
        },

        _initGrapesJS: function () {
            this.editor = grapesjs.init({
                projectData: this.page ? JSON.parse(this.page.data) : {
                    pages: [{ component: this.options.defaultContent }]
                },
                container: this.el[0],
                plugins: [
                    "gjs-blocks-basic",
                    "grapesjs-preset-webpage",
                    "grapesjs-navbar",
                    "grapesjs-plugin-forms",
                    "grapesjs-blocks-flexbox",
                    "grapesjs-component-code-editor",
                    "grapesjs-parser-postcss"
                ],
                pluginsOpts: {
                    "grapesjs-preset-webpage": {
                        textCleanCanvas: "Are you sure you want to clear the canvas?",
                        modalImportContent: editor => this._getFullHtml(editor)
                    },
                    "gjs-blocks-basic": {
                        blocks: [
                            "column1",
                            "column2",
                            "column3",
                            "column3-7",
                            "text",
                            "link",
                            "image",
                            "video",
                            "map"
                        ]
                    },
                    "grapesjs-navbar": {
                        classPrefix: "gjs-navbar"
                    },
                    "grapesjs-plugin-forms": {
                        blocks: [
                            "form",
                            "input",
                            "textarea",
                            "select",
                            "button",
                            "label",
                            "checkbox",
                            "radio"
                        ]
                    },
                    "grapesjs-blocks-flexbox": {
                        stylePrefix: "gjs-",
                    }
                },
            });

            this.editor.Panels.addButton("views", {
                id: "open-code",
                className: 'fa fa-code',
                command: "open-code",
                attributes: { title: "Open Code" }
            });

            this.editor.Panels.addButton("options", {
                id: "save-page",
                label: this.saveIcon,
                command: "open-save-modal",
                attributes: { title: "Save Page" }
            });

            this.editor.Commands.add("open-save-modal", this._onSaveButtonClick);
        },

        _getFullHtml: function (editor) {
            const fullHtml = `
                <style>${editor.getCss()}</style>
                ${editor.getHtml()}
            `;
            return fullHtml;
        },

        _onSaveButtonClick: function (editor, sender) {
            sender && sender.set("active", 0); // turn off the button if toggled
            const modal = editor.Modal;
            const container = document.createElement("div");

            container.innerHTML = this.getModalTemplate(this.page || {});

            modal.setTitle("Save Page");
            modal.setContent(container);
            modal.open();

            container
                .querySelector(`#${this.constants.fieldConfirmSaveID}`)
                .onclick = () => this._onPageSave(editor, container);

            container
                .querySelector(`#${this.constants.fieldTitleID}`)
                .addEventListener("blur", this._onTitleBlur);

            container
                .querySelector(`#${this.constants.fieldUrlID}`)
                .addEventListener("blur", this._onUrlBlur);
        },

        _onPageSave: function (editor, container) {
            if (!this._validateSaveForm(container)) {
                return;
            }

            this._savePage(container, this.page ? "blocksmith_update_page" : "blocksmith_create_page");
        },

        _savePage: function (container, action) {
            var formData = this._getFormData(container);
            var csrf_field = $('meta[name=csrf_field_name]').attr('content');
            var csrf_token = $('meta[name=' + csrf_field + ']').attr('content');

            $.ajax({
                method: "POST",
                url: this.sandbox.client.url(`/api/action/${action}`),
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
                headers: {
                    'X-CSRFToken': csrf_token
                },
                success: (resp) => {
                    window.location.href = this.sandbox.client.url(resp.result.url);
                },
                error: (resp) => {
                    this._showErrorModal(resp);
                }
            });
        },

        _getFormData: function (container) {
            const title = container.querySelector(`#${this.constants.fieldTitleID}`).value;
            const url = container.querySelector(`#${this.constants.fieldUrlID}`).value;
            const fullscreen = container.querySelector(`#${this.constants.fieldFullscreenID}`).value;
            const fullHtml = this._getFullHtml(this.editor);
            const editorData = this.editor.getProjectData();
            const published = container.querySelector(`#${this.constants.fieldPublishedID}`).checked ? "yes" : "no";
            const formData = new FormData();

            if (this.page) {
                formData.append("id", this.page.id);
            }

            formData.append("title", title);
            formData.append("url", url);
            formData.append("fullscreen", fullscreen);
            formData.append("html", fullHtml);
            formData.append("data", JSON.stringify(editorData));
            formData.append("published", published);

            return formData;
        },

        /**
         * Simple front-end validation for the save form.
         *
         * @param {HTMLDivElement} container
         * @returns {boolean}
         */
        _validateSaveForm: function (container) {
            const fields = [
                container.querySelector(`#${this.constants.fieldTitleID}`),
                container.querySelector(`#${this.constants.fieldUrlID}`)
            ];

            return fields.every(field => {
                const isValid = field.value.trim().length > 0;
                field.classList.toggle("is-invalid", !isValid);
                return isValid;
            });
        },

        /**
         * Convert a string to a slug.
         *
         * @param {string} text
         *
         * @returns {string}
         */
        _onTitleBlur: function (e) {
            document.querySelector(`#${this.constants.fieldUrlID}`).value = this._slugify(e.target.value);
        },

        /**
         * Convert a string to a URL-friendly slug.
         *
         * Allow slashes, dashes, and underscores.
         *
         * @param {string} text
         *
         * @returns {string}
         */
        _slugify: function (text) {
            return text
                .toLowerCase()
                .trim()
                .replace(/[^a-z0-9\/\-_]+/g, '-')  // Replace non-allowed chars with dash
                .replace(/^-+|-+$/g, '')      // Trim leading/trailing dashes
                .replace(/\/+/g, '/');        // Replace multiple slashes with single slash
        },

        /**
         * Convert a string to a slug.
         *
         * @param {string} text
         *
         * @returns {string}
         */
        _onUrlBlur: function (e) {
            e.target.value = this._slugify(e.target.value);
        },

        /**
         * Show an error modal.
         *
         * @param {object} resp
         */
        _showErrorModal: function (resp) {
            const modal = this.editor.Modal;
            modal.setTitle('Save Error');
            modal.setContent(`
                    <div style="padding: 10px;">
                        <p><strong>There was a problem saving the page.</strong></p>
                        <pre style="background: white; color: black; padding: 10px; border-radius: 3px;">
                            ${JSON.stringify(resp.responseJSON, null, 2)}
                        </pre>
                    </div>
                `);
            modal.open();
        },
    }
});
