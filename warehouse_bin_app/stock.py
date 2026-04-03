import frappe

# 🔹 MAIN FUNCTION
def update_bin_stock(doc, method):

    if not getattr(doc, "items", None):
        return

    for item in doc.items:

        if not item.item_code:
            continue

        qty = item.qty or 0

        # 🔻 OUT (Sales / Delivery)
        if doc.doctype in ["Sales Invoice", "Delivery Note"]:

            if not item.get("custom_warehouse_bin"):
                frappe.throw(f"Row {item.idx}: Please select Bin")

            update_bin_qty(
                item_code=item.item_code,
                bin_name=item.custom_warehouse_bin,
                qty=-qty
            )

        # 🔺 IN (Purchase)
        elif doc.doctype in ["Purchase Receipt", "Purchase Invoice"]:

            if not item.get("custom_warehouse_bin"):
                frappe.throw(f"Row {item.idx}: Please select Bin")

            update_bin_qty(
                item_code=item.item_code,
                bin_name=item.custom_warehouse_bin,
                qty=qty
            )

        # 🔁 TRANSFER (Stock Entry)
        elif doc.doctype == "Stock Entry":

            # OUT
            if item.get("custom_source_warehouse_bin"):
                update_bin_qty(
                    item_code=item.item_code,
                    bin_name=item.custom_source_warehouse_bin,
                    qty=-qty
                )

            # IN
            if item.get("custom_target_warehouse_bin"):
                update_bin_qty(
                    item_code=item.item_code,
                    bin_name=item.custom_target_warehouse_bin,
                    qty=qty
                )


# 🔹 UPDATE BIN STOCK
def update_bin_qty(item_code, bin_name, qty):

    if not bin_name:
        return

    # Get warehouse from bin
    warehouse = frappe.db.get_value(
        "Warehouse Bin",
        bin_name,
        "warehouse"
    )

    if not warehouse:
        frappe.throw(f"❌ Warehouse not found for Bin {bin_name}")

    # Get existing record
    record = frappe.db.get_value(
        "Bin Stock",
        {
            "item": item_code,
            "warehouse": warehouse,
            "warehouse_bin": bin_name
        },
        ["name", "qty"],
        as_dict=True
    )

    # 🔄 UPDATE
    if record:
        new_qty = (record.qty or 0) + qty

        if new_qty < 0:
            frappe.throw(
                f"❌ Negative stock not allowed in Bin {bin_name}"
            )

        frappe.db.set_value(
            "Bin Stock",
            record.name,
            "qty",
            new_qty
        )

    # ➕ CREATE
    else:
        if qty < 0:
            frappe.throw(
                f"❌ No stock available in Bin {bin_name}"
            )

        doc = frappe.get_doc({
            "doctype": "Bin Stock",
            "item": item_code,
            "warehouse": warehouse,
            "warehouse_bin": bin_name,
            "qty": qty
        })
        doc.insert(ignore_permissions=True)


# 🔹 VALIDATION BEFORE SUBMIT
def validate_bin_stock(doc, method):

    for item in doc.items:

        qty = item.qty or 0

        # 🔻 Only OUT validation
        if doc.doctype in ["Sales Invoice", "Delivery Note"]:

            bin_name = item.get("custom_warehouse_bin")

            if not bin_name:
                frappe.throw(f"Row {item.idx}: Please select Bin")

            available_qty = frappe.db.get_value(
                "Bin Stock",
                {
                    "item": item.item_code,
                    "warehouse_bin": bin_name
                },
                "qty"
            ) or 0

            if available_qty < qty:
                frappe.throw(
                    f"❌ Row {item.idx}: Not enough stock in Bin {bin_name}. Available: {available_qty}"
                )


# import frappe

# # 🔹 MAIN FUNCTION
# def update_bin_stock(doc, method):

#     for item in doc.items:

#         qty = item.qty or 0

#         # 🔻 OUT
#         if doc.doctype in ["Sales Invoice", "Delivery Note"]:
#             update_bin_qty(
#                 item.item_code,
#                 item.custom_warehouse_bin,
#                 -qty
#             )

#         # 🔺 IN
#         elif doc.doctype in ["Purchase Receipt", "Purchase Invoice"]:
#             update_bin_qty(
#                 item.item_code,
#                 item.custom_warehouse_bin,
#                 qty
#             )

#         # 🔁 TRANSFER
#         elif doc.doctype == "Stock Entry":

#             if item.get("custom_source_warehouse_bin"):
#                 update_bin_qty(
#                     item.item_code,
#                     item.custom_source_warehouse_bin,
#                     -qty
#                 )

#             if item.get("custom_target_warehouse_bin"):
#                 update_bin_qty(
#                     item.item_code,
#                     item.custom_target_warehouse_bin,
#                     qty
#                 )


# # 🔹 UPDATE FUNCTION (FINAL FIXED)
# def update_bin_qty(item_code, bin_name, qty):

#     if not bin_name:
#         return

#     # 🔹 Get warehouse from Warehouse Bin
#     warehouse = frappe.db.get_value(
#         "Warehouse Bin",
#         bin_name,
#         "warehouse"
#     )

#     record = frappe.db.get_value(
#         "Bin Stock",
#         {
#             "item": item_code,
#             "warehouse_bin": bin_name,
#             "warehouse": warehouse
#         },
#         ["name", "qty"],
#         as_dict=True
#     )

#     # 🔄 Update existing
#     if record:
#         frappe.db.set_value(
#             "Bin Stock",
#             record.name,
#             "qty",
#             (record.qty or 0) + qty
#         )

#     # ➕ Create new
#     else:
#         doc = frappe.get_doc({
#             "doctype": "Bin Stock",
#             "item": item_code,
#             "warehouse": warehouse,
#             "warehouse_bin": bin_name,
#             "qty": qty
#         })
#         doc.insert(ignore_permissions=True)


# # 🔹 VALIDATION
# def validate_bin(doc, method):

#     if not getattr(doc, "items", None):
#         return

#     for item in doc.items:

#         if not item.get("custom_warehouse_bin") \
#            and not item.get("custom_source_warehouse_bin") \
#            and not item.get("custom_target_warehouse_bin"):

#             frappe.throw(
#                 f"Row {item.idx}: Please select Bin for Item {item.item_code}"
#             )



# def update_sle_bin(doc, method):

#     for item in doc.items:

#         sle_list = frappe.get_all(
#             "Stock Ledger Entry",
#             filters={
#                 "voucher_no": doc.name,
#                 "item_code": item.item_code
#             },
#             fields=["name"]
#         )

#         for sle in sle_list:
#             frappe.db.set_value(
#                 "Stock Ledger Entry",
#                 sle.name,
#                 "custom_warehouse_bin",
#                 item.get("custom_warehouse_bin")
#             )


# def validate_bin_stock(doc, method):

#     for item in doc.items:

#         bin_name = item.get("custom_warehouse_bin")

#         if not bin_name:
#             frappe.throw(f"Row {item.idx}: Please select Bin")

#         qty = frappe.db.get_value(
#             "Bin Stock",
#             {
#                 "item": item.item_code,
#                 "warehouse_bin": bin_name
#             },
#             "qty"
#         ) or 0

#         # 🔴 Only for OUT transactions
#         if doc.doctype in ["Sales Invoice", "Delivery Note"]:
#             if qty < item.qty:
#                 frappe.throw(
#                     f"❌ Not enough stock in Bin {bin_name}. Available: {qty}"
#                 )




# import frappe

# # 🔹 MAIN FUNCTION (trigger on submit)
# def update_bin_stock(doc, method):

#     if not getattr(doc, "items", None):
#         return

#     for item in doc.items:

#         if not item.item_code:
#             continue

#         qty = item.qty or 0

#         # 🔻 OUT (Source Bin)
#         if item.get("custom_source_warehouse_bin"):
#             update_bin_qty(
#                 item_code=item.item_code,
#                 bin_name=item.custom_source_warehouse_bin,
#                 qty=-qty
#             )

#         # 🔺 IN (Target Bin)
#         elif item.get("custom_target_warehouse_bin"):
#             update_bin_qty(
#                 item_code=item.item_code,
#                 bin_name=item.custom_target_warehouse_bin,
#                 qty=qty
#             )

#         # 🔹 Normal (Purchase / Delivery)
#         elif item.get("custom_warehouse_bin"):
#             update_bin_qty(
#                 item_code=item.item_code,
#                 bin_name=item.custom_warehouse_bin,
#                 qty=qty
#             )


# # 🔹 UPDATE FUNCTION (FIXED)
# def update_bin_qty(item_code, bin_name, qty):

#     if not bin_name:
#         return

#     # 🔍 Match your doctype fields
#     record = frappe.db.get_value(
#         "Bin Stock",   # ✅ correct doctype
#         {
#             "item": item_code,                # ✅ FIXED
#             "warehouse_bin": bin_name         # ✅ FIXED
#         },
#         ["name", "qty"],
#         as_dict=True
#     )

#     # 🔄 Update existing
#     if record:
#         frappe.db.set_value(
#             "Bin Stock",   # ✅ FIXED
#             record.name,
#             "qty",
#             (record.qty or 0) + qty
#         )

#     # ➕ Create new
#     else:
#         doc = frappe.get_doc({
#             "doctype": "Bin Stock",          # ✅ FIXED
#             "item": item_code,               # ✅ FIXED
#             "warehouse_bin": bin_name,       # ✅ FIXED
#             "qty": qty
#         })
#         doc.insert(ignore_permissions=True)


# # 🔹 VALIDATION
# def validate_bin(doc, method):

#     if not getattr(doc, "items", None):
#         return

#     for item in doc.items:

#         if not item.get("custom_warehouse_bin") \
#            and not item.get("custom_source_warehouse_bin") \
#            and not item.get("custom_target_warehouse_bin"):

#             frappe.throw(
#                 f"Row {item.idx}: Please select Bin for Item {item.item_code}"
#             )




# import frappe

# def update_bin_in_ledger(doc, method):

#     if not getattr(doc, "items", None):
#         return

#     for item in doc.items:

#         # find ledger entries of this voucher + item
#         sle_list = frappe.get_all(
#             "Stock Ledger Entry",
#             filters={
#                 "voucher_no": doc.name,
#                 "item_code": item.item_code
#             },
#             fields=["name", "actual_qty"]
#         )

#         for sle in sle_list:

#             # Purchase / Delivery / Invoice
#             if item.get("custom_warehouse_bin"):
#                 frappe.db.set_value(
#                     "Stock Ledger Entry",
#                     sle.name,
#                     "custom_warehouse_bin",
#                     item.custom_warehouse_bin,
#                     update_modified=False
#                 )

#             # Stock Entry Source (negative qty)
#             elif sle.actual_qty < 0 and item.get("custom_source_warehouse_bin"):
#                 frappe.db.set_value(
#                     "Stock Ledger Entry",
#                     sle.name,
#                     "custom_warehouse_bin",
#                     item.custom_source_warehouse_bin,
#                     update_modified=False
#                 )

#             # Stock Entry Target (positive qty)
#             elif sle.actual_qty > 0 and item.get("custom_target_warehouse_bin"):
#                 frappe.db.set_value(
#                     "Stock Ledger Entry",
#                     sle.name,
#                     "custom_warehouse_bin",
#                     item.custom_target_warehouse_bin,
#                     update_modified=False
#                 )

