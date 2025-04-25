/**
 * Initialize the GrapesJS editor
 */
ckan.module("blocksmith-editor", function ($) {
    return {
        templates: {
            saveIcon: `
                <svg width="19" height="19" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                    <path d="M433.9 129.9l-83.9-83.9A48 48 0 0 0 316.1 32H48C21.5 32 0 53.5 0 80v352c0 26.5 21.5 48 48 48h352c26.5 0 48-21.5 48-48V163.9a48 48 0 0 0 -14.1-33.9zM224 416c-35.3 0-64-28.7-64-64 0-35.3 28.7-64 64-64s64 28.7 64 64c0 35.3-28.7 64-64 64zm96-304.5V212c0 6.6-5.4 12-12 12H76c-6.6 0-12-5.4-12-12V108c0-6.6 5.4-12 12-12h228.5c3.2 0 6.2 1.3 8.5 3.5l3.5 3.5A12 12 0 0 1 320 111.5z"/>
                </svg>
            `,
            getModalTemplate: function (page) {
                return `
                    <div style="padding: 10px;">
                        <div class="form-group control-medium">
                            <label class="form-label">Title</label><br>
                        <input type="text" id="save-page-title" class="form-control" value="${page.title}" />
                    </div>

                    <div class="form-group control-medium">
                        <label class="form-label">Name</label><br>
                        <input type="text" id="save-page-name" class="form-control" value="${page.name}" />
                    </div>

                    <div class="form-group control-medium">
                        <label class="form-label">Full screen</label><br>
                        <select id="save-page-fullscreen">
                            <option value="yes" ${page.fullscreen ? "selected" : ""}>Yes</option>
                            <option value="no" ${page.fullscreen ? "selected" : ""}>No</option>
                        </select>
                    </div>

                    <div class="form-actions">
                        <button id="confirm-save-page" class="btn btn-default">Save</button>
                    </div>
                </div>
            `
            },
        },
        options: {
            pageName: null
        },
        initialize: function () {
            $.proxyAll(this, /_/);

            this.page = null;
            this.editor = null;

            this._loadPageData();
        },

        _loadPageData: function () {
            if (!this.options.pageName) {
                return this._initGrapesJS();
            }

            $.ajax({
                method: "GET",
                url: this.sandbox.client.url("/api/action/blocksmith_get_page"),
                data: { name: this.options.pageName },
                success: (resp) => {
                    this.page = resp.result;
                    this._initGrapesJS();
                },
                error: (resp) => {
                    this._initGrapesJS();
                }
            });
        },

        _initGrapesJS: function () {
            this.editor = grapesjs.init({
                projectData: this.page?.editor_data || {
                    pages: [
                        {
                            component: `
                            <div class="page-wrapper" style="font-family: sans-serif; padding: 40px;">
                                <header style="text-align: center; padding: 20px 0;">
                                    <h1 style="margin: 0; font-size: 2.5em;">Welcome to Your Page</h1>
                                    <p style="color: #555;">Customize this page with the builder</p>
                                </header>

                                <section class="hero-section" style="background: #f0f4f8; padding: 60px 20px; border-radius: 12px; margin-bottom: 40px;">
                                    <h2 style="margin-bottom: 10px; font-size: 2em;">Hero Section</h2>
                                    <p style="max-width: 600px; margin: auto;">Use this space to make a great first impression. Highlight something important or add a call to action.</p>
                                    <button style="margin-top: 20px; padding: 10px 20px; font-size: 1em; border: none; border-radius: 8px; background-color: #007bff; color: white; cursor: pointer;">
                                        Get Started
                                    </button>
                                </section>

                                <section class="content-section" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                                    <div style="background: white; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                                        <h3>Feature One</h3>
                                        <p>Describe a feature or section of your page here.</p>
                                    </div>
                                    <div style="background: white; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                                        <h3>Feature Two</h3>
                                        <p>Use blocks and drag-and-drop to customize your layout.</p>
                                    </div>
                                    <div style="background: white; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                                        <h3>Feature Three</h3>
                                        <p>Bring your ideas to life easily with GrapesJS.</p>
                                    </div>
                                </section>
                            </div>
                        `
                        }
                    ]
                },
                container: this.el[0],
                plugins: ["grapesjs-preset-webpage", "gjs-blocks-basic"],
                pluginsOpts: {
                    "grapesjs-preset-webpage": {
                        textCleanCanvas: "Are you sure you want to clear the canvas?"
                    },
                    "gjs-blocks-basic": {
                        blocks: [
                            "column1",
                            "column2",
                            "column3",
                            "column3-7",
                            "text",
                            "link",
                            "image", "video", "map"]
                    }
                }
            });

            this.editor.Panels.addButton("options", {
                id: "save-page",
                label: this.templates.saveIcon,
                command: "open-save-modal",
                attributes: { title: "Save Page" }
            });

            this.editor.Commands.add("open-save-modal", this._onSaveButtonClick);
        },

        _onSaveButtonClick: function (editor, sender) {
            sender && sender.set("active", 0); // turn off the button if toggled
            const modal = editor.Modal;
            const container = document.createElement("div");

            container.innerHTML = this.templates.getModalTemplate(this.page);

            modal.setTitle("Save Page");
            modal.setContent(container);
            modal.open();

            container
                .querySelector("#confirm-save-page")
                .onclick = () => this._onPageSave(editor, container);
        },

        _onPageSave: function (editor, container) {
            const title = container.querySelector("#save-page-title").value;
            const name = container.querySelector("#save-page-name").value;
            const fullscreen = container.querySelector("#save-page-fullscreen").value;
            const fullHtml = `
                <style>${editor.getCss()}</style>
                ${editor.getHtml()}
            `;
            const editorData = editor.getProjectData();

            const formData = new FormData();

            formData.append("title", title);
            formData.append("name", name);
            formData.append("fullscreen", fullscreen);
            formData.append("html", fullHtml);
            formData.append("editor_data", JSON.stringify(editorData));

            var csrf_field = $('meta[name=csrf_field_name]').attr('content');
            var csrf_token = $('meta[name=' + csrf_field + ']').attr('content');

            $.ajax({
                method: "POST",
                url: this.sandbox.client.url("/api/action/blocksmith_save_page"),
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
                headers: {
                    'X-CSRFToken': csrf_token
                },
                success: (resp) => {
                    window.location.href = `/page/${name}`;
                },
                error: (resp) => {
                    console.error(resp);
                }
            });
        }
    }
});
