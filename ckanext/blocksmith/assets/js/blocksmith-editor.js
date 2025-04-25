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
            modalBody: `
                <div style="padding: 10px;">
                    <div class="form-group control-medium">
                    <label class="form-label">Title</label><br>
                    <input type="text" id="save-page-title" class="form-control"/>
                    </div>

                    <div class="form-group control-medium">
                    <label class="form-label">Name</label><br>
                    <input type="text" id="save-page-name" class="form-control"/>
                    </div>

                    <button id="confirm-save-page" class="btn btn-default">Save</button>
                </div>
            `
        },
        initialize: function () {
            $.proxyAll(this, /_on/);

            const self = this;

            const editor = grapesjs.init({
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

            editor.Panels.addButton("options", {
                id: "save-page",
                label: this.templates.saveIcon,
                command: "open-save-modal",
                attributes: { title: "Save Page" }
            });

            editor.Commands.add("open-save-modal", {
                run(editor, sender) {
                    sender && sender.set("active", 0); // turn off the button if toggled
                    const modal = editor.Modal;
                    const container = document.createElement("div");

                    container.innerHTML = self.templates.modalBody;

                    modal.setTitle("Save Page");
                    modal.setContent(container);
                    modal.open();

                    // Handle save click
                    container.querySelector("#confirm-save-page").onclick = () => self._onPageSave(editor, container);
                }
            });
        },

        _onPageSave: function (editor, container) {
            const title = container.querySelector("#save-page-title").value;
            const name = container.querySelector("#save-page-name").value;
            const html = editor.getHtml();
            const css = editor.getCss();
            const editorData = editor.getProjectData();

            const formData = new FormData();

            formData.append("name", name);
            formData.append("title", title);
            formData.append("html", html);
            formData.append("css", css);
            formData.append("editor_data", JSON.stringify(editorData));

            var csrf_field = $('meta[name=csrf_field_name]').attr('content');
            var csrf_token = $('meta[name=' + csrf_field + ']').attr('content');

            $.ajax({
                method: "POST",
                url: this.sandbox.client.url("/api/action/blocksmith_page_save"),
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
                headers: {
                    'X-CSRFToken': csrf_token
                },
                success: (resp) => {
                    console.log(resp);
                    // if (!resp.result.success) {
                    //     return this._showError(resp.result.error);
                    // }

                    // if (resp.result.valid) {
                    //     this.form.off("submit", this._onFormSubmit);
                    //     this.form.submit();
                    // };
                },
                error: (resp) => {
                    console.error(resp);
                },
                complete: () => {
                    // this.submitBtn.prop("disabled", false);
                }
            });
        }
    };
});
