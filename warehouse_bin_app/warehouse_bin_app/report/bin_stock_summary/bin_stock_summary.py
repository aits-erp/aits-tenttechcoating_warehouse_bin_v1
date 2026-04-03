# Copyright (c) 2026, pankaj yadav and contributors
# For license information, please see license.txt

# import frappe


import frappe

def execute(filters=None):

    columns = [
        {"label": "Item", "fieldname": "item", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
        {"label": "Bin", "fieldname": "warehouse_bin", "fieldtype": "Data", "width": 150},
        {"label": "Available Qty", "fieldname": "qty", "fieldtype": "Float", "width": 120},
    ]

    data = frappe.db.get_all(
        "Bin Stock",
        fields=["item", "warehouse", "warehouse_bin", "qty"],
        order_by="item, warehouse"
    )

    return columns, data