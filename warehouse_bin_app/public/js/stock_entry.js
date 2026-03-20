frappe.ui.form.on("Stock Entry", {
    refresh(frm) {

        // Source Warehouse Bin filter
        frm.set_query("custom_source_warehouse_bin", "items", function(doc, cdt, cdn) {
            let row = locals[cdt][cdn];

            if (!row.s_warehouse) {
                return {
                    filters: {
                        name: ["=", ""]
                    }
                };
            }

            return {
                filters: {
                    warehouse: row.s_warehouse
                }
            };
        });

        // Target Warehouse Bin filter
        frm.set_query("custom_target_warehouse_bin", "items", function(doc, cdt, cdn) {
            let row = locals[cdt][cdn];

            if (!row.t_warehouse) {
                return {
                    filters: {
                        name: ["=", ""]
                    }
                };
            }

            return {
                filters: {
                    warehouse: row.t_warehouse
                }
            };
        });

    }
});