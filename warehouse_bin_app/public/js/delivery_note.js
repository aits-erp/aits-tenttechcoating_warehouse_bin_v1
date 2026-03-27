frappe.ui.form.on("Delivery Note", {
    refresh(frm) {

        // For NEW field
        frm.set_query("custom_warehouse_bin", "items", function(doc, cdt, cdn) {
            let row = locals[cdt][cdn];

            if (!row.warehouse && !doc.set_warehouse) {
                return {
                    filters: {
                        name: ["=", ""]
                    }
                };
            }

            return {
                filters: {
                    warehouse: row.warehouse || doc.set_warehouse
                }
            };
        });

        // For OLD field (important)
        frm.set_query("custom_custom_warehouse_bin", "items", function(doc, cdt, cdn) {
            let row = locals[cdt][cdn];

            if (!row.warehouse && !doc.set_warehouse) {
                return {
                    filters: {
                        name: ["=", ""]
                    }
                };
            }

            return {
                filters: {
                    warehouse: row.warehouse || doc.set_warehouse
                }
            };
        });

    }
});