frappe.ui.form.on("Stock Entry", {
    refresh(frm) {

        // ✅ Source Warehouse Bin (NEW)
        frm.set_query("custom_source_warehouse_bin", "items", function(doc, cdt, cdn) {
            let row = locals[cdt][cdn];

            let warehouse = row.s_warehouse || doc.from_warehouse;

            if (!warehouse) {
                return { filters: { name: ["=", ""] } };
            }

            return {
                filters: {
                    warehouse: warehouse
                }
            };
        });

        // ✅ Source Warehouse Bin (OLD - if exists)
        frm.set_query("custom_custom_source_warehouse_bin", "items", function(doc, cdt, cdn) {
            let row = locals[cdt][cdn];

            let warehouse = row.s_warehouse || doc.from_warehouse;

            if (!warehouse) {
                return { filters: { name: ["=", ""] } };
            }

            return {
                filters: {
                    warehouse: warehouse
                }
            };
        });

        // ✅ Target Warehouse Bin (NEW)
        frm.set_query("custom_target_warehouse_bin", "items", function(doc, cdt, cdn) {
            let row = locals[cdt][cdn];

            let warehouse = row.t_warehouse || doc.to_warehouse;

            if (!warehouse) {
                return { filters: { name: ["=", ""] } };
            }

            return {
                filters: {
                    warehouse: warehouse
                }
            };
        });

        // ✅ Target Warehouse Bin (OLD - if exists)
        frm.set_query("custom_custom_target_warehouse_bin", "items", function(doc, cdt, cdn) {
            let row = locals[cdt][cdn];

            let warehouse = row.t_warehouse || doc.to_warehouse;

            if (!warehouse) {
                return { filters: { name: ["=", ""] } };
            }

            return {
                filters: {
                    warehouse: warehouse
                }
            };
        });

    }
});


// frappe.ui.form.on("Stock Entry", {
//     refresh(frm) {

//         // Source Warehouse Bin filter
//         frm.set_query("custom_source_warehouse_bin", "items", function(doc, cdt, cdn) {
//             let row = locals[cdt][cdn];

//             if (!row.s_warehouse) {
//                 return {
//                     filters: {
//                         name: ["=", ""]
//                     }
//                 };
//             }

//             return {
//                 filters: {
//                     warehouse: row.s_warehouse
//                 }
//             };
//         });

//         // Target Warehouse Bin filter
//         frm.set_query("custom_target_warehouse_bin", "items", function(doc, cdt, cdn) {
//             let row = locals[cdt][cdn];

//             if (!row.t_warehouse) {
//                 return {
//                     filters: {
//                         name: ["=", ""]
//                     }
//                 };
//             }

//             return {
//                 filters: {
//                     warehouse: row.t_warehouse
//                 }
//             };
//         });

//     }
// });