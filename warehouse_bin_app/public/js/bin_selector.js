frappe.ui.form.on('* Item', {

    warehouse: function(frm, cdt, cdn) {
        set_bin_filter(frm, cdt, cdn);
    },

    item_code: function(frm, cdt, cdn) {
        set_bin_filter(frm, cdt, cdn);
    }

});


function set_bin_filter(frm, cdt, cdn) {

    let row = locals[cdt][cdn];

    if (!row.warehouse) return;

    frm.fields_dict.items.grid.get_field("custom_warehouse_bin").get_query = function(doc, cdt, cdn) {

        let child = locals[cdt][cdn];

        return {
            filters: {
                warehouse: child.warehouse   // ✅ MAIN FILTER
            }
        };
    };
}