ckan.module("blocksmith-grid", function ($) {
    return {
        initialize: function () {
            this.pageData = null;

            this.grid = new gridjs.Grid({
                columns: [
                    { name: 'ID', hidden: true },
                    this._("Title"),
                    this._("Name"),
                    this._("Created"),
                    this._("Modified"),
                    this._("Fullscreen"),
                    this._("Published"),
                    {
                        name: this._("Actions"),
                        formatter: (cell, row) => {
                            const self = this;
                            const readUrl = this.sandbox.client.url('/page/' + row.cells[2].data);
                            const editUrl = this.sandbox.client.url('/blocksmith/edit/' + row.cells[2].data);

                            return gridjs.h('div', { className: 'd-flex gap-2' }, [
                                gridjs.h('a', {
                                    className: 'btn btn-outline-primary',
                                    href: readUrl
                                }, gridjs.html('<i class="fa fa-eye"></i>')),

                                gridjs.h('a', {
                                    className: 'btn btn-outline-primary',
                                    href: editUrl
                                }, gridjs.html('<i class="fa fa-pencil"></i>')),

                                gridjs.h('a', {
                                    className: 'btn btn-outline-danger btn-delete',
                                    onClick: () => this._onDelete(row)
                                }, gridjs.html('<i class="fa fa-trash"></i>'))
                            ]);
                        }
                    }
                ],
                server: {
                    url: this.sandbox.client.url('/api/action/blocksmith_list_pages'),
                    then: (data) => {
                        this.pageData = this._prepareData(data);

                        return this.pageData;
                    }
                },
                pagination: {
                    limit: 5,
                    summary: false
                },
                search: true,
                sort: true
            }).render(document.getElementById("blocksmith-grid"));
        },

        _prepareData: function (data) {
            return data.result.map(page =>
                [
                    page.id,
                    page.title,
                    page.name,
                    new Date(page.created_at + 'Z').toLocaleString(),
                    new Date(page.modified_at + 'Z').toLocaleString(),
                    page.fullscreen ? "Yes" : "No",
                    page.published ? "Yes" : "No",
                    "View | Edit | Delete"
                ]
            );
        },

        _onDelete: function (row) {
            const self = this;

            const pageId = row.cells[0].data;

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
                    {
                        id: pageId,
                    },
                    function (data) {
                        Swal.fire("Page has been deleted", "", "success");
                        self.grid.forceRender();
                    },
                    function (err) {
                        Swal.fire("Unable to delete page", "", "error");
                    },
                );
            });
        }
    };
});
