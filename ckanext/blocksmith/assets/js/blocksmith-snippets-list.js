ckan.module("blocksmith-snippets-list", function ($) {
    return {
        initialize: function () {
            $.proxyAll(this, /_/);

            this.snippetData = null;
            this.searchTimeout = null;
            this.searchInput = $("#blocksmith-search");
            this.searchClear = $("#blocksmith-clear");

            this.table = new Tabulator("#blocksmith-snippets-list", {
                ajaxURL: this.sandbox.client.url('/api/action/blocksmith_list_snippets'),
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
                minHeight: "400",
                placeholder: this._("No snippets found"),
            });

            // Event listeners

            this.table.on("tableBuilt", () => {
                $(".blocksmith-search").show();
            });

            this.el.on("click", ".btn-delete", this._onSnippetDelete);
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

            this.snippetData = data.result.map(snippet => ({
                id: snippet.id,
                title: snippet.title,
                name: snippet.name,
                created: new Date(snippet.created_at + 'Z').toLocaleString(),
                modified: new Date(snippet.modified_at + 'Z').toLocaleString(),
                actions: "" // Filled dynamically by _formatActionCell
            }));

            // After rendering, hook the delete buttons
            setTimeout(() => {
                $("#blocksmith-grid").on("click", ".btn-delete", function () {
                    const snippetId = $(this).data('id');
                    self._onDelete(snippetId);
                });
            }, 100);

            return this.snippetData;
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
                { title: this._("Name"), field: 'name', resizable: true},
                { title: this._("Created"), field: 'created', resizable: false, maxWidth: 160 },
                { title: this._("Modified"), field: 'modified', resizable: false, maxWidth: 160 },
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
            const readUrl = this.sandbox.client.url('/blocksmith/snippet/read/' + rowData.id);
            const editUrl = this.sandbox.client.url('/blocksmith/snippet/edit/' + rowData.id);

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
         * Delete a snippet
         *
         * @param {Event} e The event
         */
        _onSnippetDelete: function (e) {
            const snippetId = $(e.currentTarget).data('id');
            const self = this;

            Swal.fire({
                text: this._("Are you sure you wish to delete this snippet?"),
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
                    "blocksmith_delete_snippet",
                    { id: snippetId },
                    function (_) {
                        Swal.fire("The snippet has been deleted", "", "success");
                        self.table.replaceData(); // Reload
                    },
                    function (_) {
                        Swal.fire("Unable to delete the snippet", "", "error");
                    }
                );
            });
        },

        /**
         * Search for a snippet
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
                            row.name,
                            row.created,
                            row.modified,
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
