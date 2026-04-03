frappe.ui.form.on("Sales Invoice Item", {
    custom_warehouse_bin(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Bin Stock",
                filters: {
                    item: row.item_code,
                    warehouse_bin: row.custom_warehouse_bin
                },
                fieldname: ["qty"]
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint(
                        `Available Qty in Bin: ${r.message.qty}`
                    );
                }
            }
        });
    }
});



// frappe.ui.form.on("Sales Invoice", {
//     refresh(frm) {

//         // NEW field
//         frm.set_query("custom_warehouse_bin", "items", function(doc, cdt, cdn) {
//             let row = locals[cdt][cdn];

//             if (!row.warehouse && !doc.set_warehouse) {
//                 return {
//                     filters: {
//                         name: ["=", ""]
//                     }
//                 };
//             }

//             return {
//                 filters: {
//                     warehouse: row.warehouse || doc.set_warehouse
//                 }
//             };
//         });

//         // OLD field (important)
//         frm.set_query("custom_custom_warehouse_bin", "items", function(doc, cdt, cdn) {
//             let row = locals[cdt][cdn];

//             if (!row.warehouse && !doc.set_warehouse) {
//                 return {
//                     filters: {
//                         name: ["=", ""]
//                     }
//                 };
//             }

//             return {
//                 filters: {
//                     warehouse: row.warehouse || doc.set_warehouse
//                 }
//             };
//         });

//     }
// });




// frappe.ui.form.on("Sales Invoice", {
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