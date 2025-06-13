ckan.module("blocksmith-menus-list", function ($) {
    return {
        initialize: function () {
            $.proxyAll(this, /_/);

            this.menuData = null;
            this.searchTimeout = null;
            this.searchInput = $("#blocksmith-search");
            this.searchClear = $("#blocksmith-clear");
            this.createMenu = $("#blocksmith-create-menu");
            this.createMenuModal = $("#blocksmith-create-menu-modal");

            this.table = new Tabulator("#blocksmith-menus-list", {
                ajaxURL: this.sandbox.client.url('/api/action/blocksmith_list_menus'),
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
                minHeight: "400px",
                placeholder: this._("No menus found"),

            });

            // Event listeners

            this.table.on("tableBuilt", () => {
                $(".blocksmith-search").show();
            });

            this.el.on("click", ".btn-delete", this._onMenuDelete);
            this.el.on("click", ".btn-cell-edit", this._onCellEdit);
            this.searchInput.on("keyup", this._onSearch);
            this.searchClear.on("click", this._onSearchClear);
            this.createMenu.on("click", this._onCreateMenu);

            this.createMenuModal.on("hidden.bs.modal", (e) => {
                this.createMenuModal.find("input").val("");
            });
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

            this.menuData = data.result.map(menu => ({
                id: menu.id,
                name: menu.name,
                created: new Date(menu.created_at + 'Z').toLocaleString(),
                modified: new Date(menu.modified_at + 'Z').toLocaleString(),
                actions: "" // Filled dynamically by _formatActionCell
            }));

            // After rendering, hook the delete buttons
            setTimeout(() => {
                $("#blocksmith-grid").on("click", ".btn-delete", function () {
                    const pageId = $(this).data('id');
                    self._onDelete(pageId);
                });
            }, 100);

            return this.menuData;
        },


        /**
         * Get the columns for the table
         *
         * @returns {Array} The columns for the table
         */
        _getColumns: function () {
            return [
                { title: 'ID', field: 'id', visible: false },
                {
                    title: this._("Name"),
                    field: 'name',
                    resizable: false,
                    editor: "input",
                    cellEdited: (cell) => {
                        this._onNameColumnEdit(cell)
                    },
                },
                { title: this._("Created"), field: 'created', resizable: false, maxWidth: 170 },
                { title: this._("Modified"), field: 'modified', resizable: false, maxWidth: 170 },
                {
                    title: this._("Actions"),
                    field: 'actions',
                    headerSort: false,
                    maxWidth: 160,
                    formatter: (cell, formatterParams, onRendered) => {
                        return this._formatActionCell(cell);
                    },
                }
            ]
        },

        /**
         * Validate the name
         *
         * @param {String} name The name
         *
         * @returns {Boolean} True if valid, false otherwise
         */
        _validateName: function (name) {
            if (name.length > 255) {
                return false;
            }

            if (name.length < 2) {
                return false;
            }

            return true;
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
         * Format the action cell
         *
         * @param {Cell} cell The cell
         *
         * @returns {String} The formatted action cell
         */
        _formatActionCell: function (cell) {
            const rowData = cell.getData();
            const rowIndex = cell.getRow().getIndex();

            const itemsUrl = this.sandbox.client.url('/blocksmith/menu/' + rowData.name);

            return `
                <div class="d-flex gap-2">
                    <a class="btn btn-outline-primary" href="${itemsUrl}" title="${this._("View items")}">
                        <i class="fa fa-sitemap"></i>
                    </a>
                    <a class="btn btn-outline-primary btn-cell-edit" data-id="${rowIndex}" title="${this._("Edit")}">
                        <i class="fa fa-pencil"></i>
                    </a>
                    <a class="btn btn-outline-danger btn-delete" data-id="${rowData.id}" title="${this._("Delete")}">
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
        _onMenuDelete: function (e) {
            const menuId = $(e.currentTarget).data('id');
            const self = this;

            Swal.fire({
                text: this._("Are you sure you wish to delete this menu?"),
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
                    "blocksmith_delete_menu",
                    { id: menuId },
                    function (data) {
                        Swal.fire("Menu has been deleted", "", "success");
                        self.table.replaceData(); // Reload
                    },
                    function (err) {
                        Swal.fire("Unable to delete menu", "", "error");
                    }
                );
            });
        },

        _onCellEdit: function (e) {
            e.preventDefault();

            const rowId = $(e.currentTarget).data('id');
            const row = this.table.getRow(rowId);
            const cell = row.getCell("name");

            if (cell) {
                cell.edit();
            }
        },

        /**
         * Handle the name column edit
         *
         * @param {Cell} cell The cell
         */
        _onNameColumnEdit: function (cell) {
            const self = this;

            const newValue = cell.getValue();
            const slug = self._slugify(newValue);
            const rowIndex = cell.getRow().getIndex();

            Swal.fire({
                text: self._("Are you sure you to change the menu name?"),
                icon: "warning",
                showConfirmButton: true,
                showDenyButton: true,
                denyButtonColor: "#206B82",
                confirmButtonColor: "#3A833A",
                denyButtonText: self._("Cancel"),
                confirmButtonText: self._("Update"),
                allowEnterKey: false
            }).then((result) => {
                if (result.isDenied) {
                    cell.restoreOldValue();
                    return;
                }

                self.sandbox.client.call(
                    "POST",
                    "blocksmith_update_menu",
                    { id: rowIndex, name: slug },
                    function (_) {
                        Swal.fire("Menu name has been updated", "", "success");
                        self.table.replaceData();
                    },
                    function (resp) {
                        const errorReason = resp.responseJSON.error.name[0];
                        Swal.fire(`Unable to update menu name: ${errorReason}`, "", "error");
                        cell.restoreOldValue();
                    }
                );
            });
        },

        _onCreateMenu: function (e) {
            e.preventDefault();

            const self = this;
            const value = this.createMenuModal.find("input").val();
            const slug = this._slugify(value);
            const modal = bootstrap.Modal.getOrCreateInstance(this.createMenuModal[0]);

            this.sandbox.client.call(
                "POST",
                "blocksmith_create_menu",
                { name: slug },
                function (_) {
                    Swal.fire("Menu name has been created", "", "success");
                    self.table.replaceData();
                    modal.hide();
                },
                function (resp) {
                    const errorReason = resp.responseJSON.error.name[0];
                    Swal.fire(`Unable to create menu: ${errorReason}`, "", "error");
                    modal.hide();
                }
            );
        },

        /**
         * Search for a menu
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
