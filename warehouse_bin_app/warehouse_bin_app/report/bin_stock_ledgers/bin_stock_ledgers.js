// Copyright (c) 2026, pankaj yadav and contributors
// For license information, please see license.txt

frappe.query_reports["Bin Stock Ledgers"] = {

    filters: [

        {
            fieldname: "item_code",
            label: "Item",
            fieldtype: "Link",
            options: "Item"
        },

        {
            fieldname: "warehouse",
            label: "Warehouse",
            fieldtype: "Link",
            options: "Warehouse"
        }

    ]

};