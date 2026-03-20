frappe.ui.form.on("Sales Invoice", {
    refresh(frm) {

        frm.set_query("custom_warehouse_bin", "items", function(doc) {

            if (!doc.set_warehouse) {
                return {
                    filters: {
                        name: ["=", ""]
                    }
                };
            }

            return {
                filters: {
                    warehouse: doc.set_warehouse
                }
            };

        });

    }
});