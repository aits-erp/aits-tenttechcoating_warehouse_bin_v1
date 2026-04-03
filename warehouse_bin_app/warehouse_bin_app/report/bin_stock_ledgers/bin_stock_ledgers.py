import frappe


def execute(filters=None):

    columns = get_columns()
    data = get_data(filters)

    return columns, data


# 🔹 COLUMNS
def get_columns():

    return [
        {"label": "Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
        {"label": "Item", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
        {"label": "Warehouse Bin", "fieldname": "bin_code", "fieldtype": "Data", "width": 150},
        {"label": "Qty Change", "fieldname": "actual_qty", "fieldtype": "Float", "width": 120},
        {"label": "Balance Qty", "fieldname": "qty_after_transaction", "fieldtype": "Float", "width": 120},
        {"label": "Voucher Type", "fieldname": "voucher_type", "fieldtype": "Data", "width": 120},
        {"label": "Voucher No", "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 150},
    ]


# 🔹 DATA
def get_data(filters):

    conditions = ""
    values = {}

    # 🔍 FILTERS (optional but useful)
    if filters.get("item_code"):
        conditions += " AND sle.item_code = %(item_code)s"
        values["item_code"] = filters.get("item_code")

    if filters.get("warehouse"):
        conditions += " AND sle.warehouse = %(warehouse)s"
        values["warehouse"] = filters.get("warehouse")

    if filters.get("from_date"):
        conditions += " AND sle.posting_date >= %(from_date)s"
        values["from_date"] = filters.get("from_date")

    if filters.get("to_date"):
        conditions += " AND sle.posting_date <= %(to_date)s"
        values["to_date"] = filters.get("to_date")

    # 🔥 FINAL QUERY (FIXED)
    return frappe.db.sql(f"""
        SELECT
            sle.posting_date,
            sle.item_code,
            sle.warehouse,
            sle.custom_warehouse_bin AS bin_code,   -- ✅ CORRECT FIELD
            sle.actual_qty,
            sle.qty_after_transaction,
            sle.voucher_type,
            sle.voucher_no
        FROM `tabStock Ledger Entry` sle
        WHERE sle.docstatus = 1
        {conditions}
        ORDER BY sle.posting_date DESC, sle.creation DESC
    """, values, as_dict=1)




# # Copyright (c) 2026, pankaj yadav and contributors
# # For license information, please see license.txt

# # import frappe


# import frappe

# def execute(filters=None):

#     columns = get_columns()
#     data = get_data(filters)

#     return columns, data


# def get_columns():

#     return [
#         {"label": "Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
#         {"label": "Item", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
#         {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
#         {"label": "Warehouse Bin", "fieldname": "bin_code", "fieldtype": "Data", "width": 150},
#         {"label": "Qty Change", "fieldname": "actual_qty", "fieldtype": "Float", "width": 120},
#         {"label": "Balance Qty", "fieldname": "qty_after_transaction", "fieldtype": "Float", "width": 120},
#         {"label": "Voucher Type", "fieldname": "voucher_type", "fieldtype": "Data", "width": 120},
#         {"label": "Voucher No", "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 150},
#     ]


# def get_data(filters):

#     return frappe.db.sql("""
#         SELECT
#             sle.posting_date,
#             sle.item_code,
#             sle.warehouse,
#             sle.custom_warehouse_bin AS bin_code,   -- ✅ FIXED
#             sle.actual_qty,
#             sle.qty_after_transaction,
#             sle.voucher_type,
#             sle.voucher_no
#         FROM `tabStock Ledger Entry` sle
#         LEFT JOIN `tabWarehouse Bin` wb
#         ON sle.custom_warehouse_bin = wb.name
#         ORDER BY sle.posting_date DESC
#     """, as_dict=1)