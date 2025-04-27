ckan.module("blocksmith-tabulator", function ($) {
    return {
        initialize: function () {
            $.proxyAll(this, /_/);

            this.pageData = null;
            this.searchTimeout = null;
            this.searchInput = $("#blocksmith-search");
            this.searchClear = $("#blocksmith-clear");

            this.table = new Tabulator("#blocksmith-tabulator", {
                ajaxURL: this.sandbox.client.url('/api/action/blocksmith_list_pages'),
                ajaxResponse: (url, params, response) => {
                    return this._prepareData(response);
                },
                columns: this._getColumns(),
                layout: "fitColumns",
                pagination: "local",
                paginationSize: 15,
                movableColumns: false,
                resizableRows: false,
                height: "100%",
                maxHeight: "100%",
                minHeight: "900",
                placeholder: this._("No pages found"),

            });

            // Event listeners

            this.table.on("tableBuilt", () => {
                $(".blocksmith-search").show();
            });

            this.el.on("click", ".btn-delete", this._onPageDelete);
            this.searchInput.on("keyup", this._onSearch);
            this.searchClear.on("click", this._onSearchClear);
        },

        /**
         * Prepare the data received from the backend
         *
         * @param {Object} data The data
         *
         * @returns {Array} The prepared data for tabulator
        */
        _prepareData: function (data) {
            const self = this;

            this.pageData = data.result.map(page => ({
                id: page.id,
                title: page.title,
                url: page.url,
                created: new Date(page.created_at + 'Z').toLocaleString(),
                modified: new Date(page.modified_at + 'Z').toLocaleString(),
                fullscreen: page.fullscreen ? "Yes" : "No",
                published: page.published ? "Yes" : "No",
                actions: "" // Filled dynamically by _formatActionCell
            }));

            // After rendering, hook the delete buttons
            setTimeout(() => {
                $("#blocksmith-grid").on("click", ".btn-delete", function () {
                    const pageId = $(this).data('id');
                    self._onDelete(pageId);
                });
            }, 100);

            return this.pageData;
        },


        /**
         * Get the columns for the table
         *
         * @returns {Array} The columns for the table
         */
        _getColumns: function () {
            return [
                { title: 'ID', field: 'id', visible: false },
                { title: this._("Title"), field: 'title', resizable: true},
                { title: this._("URL"), field: 'url', resizable: true},
                { title: this._("Created"), field: 'created', resizable: false, maxWidth: 160 },
                { title: this._("Modified"), field: 'modified', resizable: false, maxWidth: 160 },
                { title: this._("Fullscreen"), field: 'fullscreen', resizable: false, maxWidth: 120 },
                { title: this._("Published"), field: 'published', resizable: false, maxWidth: 120 },
                {
                    title: this._("Actions"),
                    field: 'actions',
                    headerSort: false,
                    maxWidth: 160,
                    formatter: (cell, formatterParams, onRendered) => {
                        return this._formatActionCell(cell.getData());
                    },
                }
            ]
        },

        /**
         * Format the action cell
         *
         * @param {Object} rowData The row data
         *
         * @returns {String} The formatted action cell
         */
        _formatActionCell: function (rowData) {
            const readUrl = this.sandbox.client.url(rowData.url);
            const editUrl = this.sandbox.client.url('/blocksmith/edit/' + rowData.id);

            return `
                <div class="d-flex gap-2">
                    <a class="btn btn-outline-primary" href="${readUrl}">
                        <i class="fa fa-eye"></i>
                    </a>
                    <a class="btn btn-outline-primary" href="${editUrl}">
                        <i class="fa fa-pencil"></i>
                    </a>
                    <a class="btn btn-outline-danger btn-delete" data-id="${rowData.id}">
                        <i class="fa fa-trash"></i>
                    </a>
                </div>
            `;
        },

        /**
         * Delete a page
         *
         * @param {String} pageId The page id
         */
        _onPageDelete: function (e) {
            const pageId = $(e.currentTarget).data('id');
            const self = this;

            Swal.fire({
                text: this._("Are you sure you wish to delete this page?"),
                icon: "warning",
                showConfirmButton: true,
                showDenyButton: true,
                denyButtonColor: "#206b82",
                confirmButtonColor: "#d43f3a",
                denyButtonText: this._("Cancel"),
                confirmButtonText: this._("Delete"),
            }).then((result) => {
                if (result.isDenied) {
                    return;
                }

                this.sandbox.client.call(
                    "POST",
                    "blocksmith_delete_page",
                    { id: pageId },
                    function (data) {
                        Swal.fire("Page has been deleted", "", "success");
                        self.table.replaceData(); // Reload
                    },
                    function (err) {
                        Swal.fire("Unable to delete page", "", "error");
                    }
                );
            });
        },

        /**
         * Search for a page
         *
         * @param {Event} e The event
         */
        _onSearch: function (e) {
            const self = this;
            const query = self.searchInput.val().toLowerCase();

            clearTimeout(this.searchTimeout);

            this.searchTimeout = setTimeout(() => {
                if (query) {
                    this.searchClear.addClass("search-active");
                    self.table.setFilter((row) => {
                        return [
                            row.title,
                            row.url,
                            row.created,
                            row.modified,
                            row.fullscreen,
                            row.published,
                        ].some(value => value && value.toString().toLowerCase().includes(query));
                    });
                } else {
                    self._onSearchClear();
                }
            }, 300);
        },

        /**
         * Clear the search
         */
        _onSearchClear: function () {
            this.searchInput.val("");
            this.table.clearFilter();
            this.searchClear.removeClass("search-active");
        }
    };
});
