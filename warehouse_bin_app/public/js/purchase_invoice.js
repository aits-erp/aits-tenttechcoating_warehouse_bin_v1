frappe.ui.form.on("Purchase Invoice", {
    refresh(frm) {

        // NEW field
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

        // OLD field (important)
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






// frappe.ui.form.on("Purchase Invoice", {
//     refresh(frm) {

//         frm.set_query("custom_warehouse_bin", "items", function(doc) {

//             if (!doc.set_warehouse) {
//                 return {
//                     filters: {
//                         name: ["=", ""]
//                     }
//                 };
//             }

//             return {
//                 filters: {
//                     warehouse: doc.set_warehouse
//                 }
//             };

//         });

//     }
// });