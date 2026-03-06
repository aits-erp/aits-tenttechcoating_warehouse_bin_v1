import frappe

def update_bin_in_ledger(doc, method):

    if not getattr(doc, "items", None):
        return

    for item in doc.items:

        # find ledger entries of this voucher + item
        sle_list = frappe.get_all(
            "Stock Ledger Entry",
            filters={
                "voucher_no": doc.name,
                "item_code": item.item_code
            },
            fields=["name", "actual_qty"]
        )

        for sle in sle_list:

            # Purchase / Delivery / Invoice
            if item.get("custom_warehouse_bin"):
                frappe.db.set_value(
                    "Stock Ledger Entry",
                    sle.name,
                    "custom_warehouse_bin",
                    item.custom_warehouse_bin,
                    update_modified=False
                )

            # Stock Entry Source (negative qty)
            elif sle.actual_qty < 0 and item.get("custom_source_warehouse_bin"):
                frappe.db.set_value(
                    "Stock Ledger Entry",
                    sle.name,
                    "custom_warehouse_bin",
                    item.custom_source_warehouse_bin,
                    update_modified=False
                )

            # Stock Entry Target (positive qty)
            elif sle.actual_qty > 0 and item.get("custom_target_warehouse_bin"):
                frappe.db.set_value(
                    "Stock Ledger Entry",
                    sle.name,
                    "custom_warehouse_bin",
                    item.custom_target_warehouse_bin,
                    update_modified=False
                )


# import frappe

# def update_bin_in_ledger(doc, method):

#     if not getattr(doc, "items", None):
#         return

#     for item in doc.items:
#         if not item.get("custom_warehouse_bin"):
#             continue

#         sle_list = frappe.get_all(
#             "Stock Ledger Entry",
#             filters={
#                 "voucher_no": doc.name,
#                 "item_code": item.item_code
#             },
#             pluck="name"
#         )

#         for sle in sle_list:
#             frappe.db.set_value(
#                 "Stock Ledger Entry",
#                 sle,
#                 "custom_warehouse_bin",
#                 item.custom_warehouse_bin,
#                 update_modified=False
#             )


# import frappe

# def add_bin_in_ledger(doc, method):

#     if not doc.items:
#         return

#     for item in doc.items:
#         if not item.custom_warehouse_bin:
#             continue

#         sle_list = frappe.get_all(
#             "Stock Ledger Entry",
#             filters={
#                 "voucher_no": doc.name,
#                 "item_code": item.item_code
#             },
#             pluck="name"
#         )

#         for sle in sle_list:
#             frappe.db.set_value(
#                 "Stock Ledger Entry",
#                 sle,
#                 "custom_warehouse_bin",
#                 item.custom_warehouse_bin
#             )   