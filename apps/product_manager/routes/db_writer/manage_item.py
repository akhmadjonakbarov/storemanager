from apps import DocumentItemModel, DocumentItemBalanceModel
from apps.product_manager.schemes import DocumentItemModelScheme


def create_doc_item(element: DocumentItemModelScheme, document_id, user_id) -> DocumentItemModel:
    """
    Create a new ProductDocItem in the database within a transaction.

    Args:
        element: A dictionary containing item data.
        document_id: The ID of the product document.
        user_id: The ID of the user creating the document item.

    Returns:
        DocumentItemModelScheme: The created document item instance.
    """
    doc_item = DocumentItemModel(
        document_id=document_id,
        qty=element.qty,
        currency_id=element.currency_id if element.currency_id != -1 else None,
        income_price=element.income_price,
        selling_price=element.selling_price,
        currency_type_id=element.currency_type_id,
        income_price_usd=element.income_price_usd,
        selling_percentage=element.selling_percentage,
        item_id=element.item_id,
        user_id=user_id,
    )
    return doc_item


def create_doc_item_balance(user_id: int, doc_item: DocumentItemModel) -> DocumentItemBalanceModel:
    """
               Create a new ProductDocItemBalance in the database.

               Args:
                   user_id: The ID of the user creating the document item balance.
                   item_id: The ID of the item.
                   new_product_doc_item: An instance of the product document item.

               Returns:
                   ProductDocItemBalance: The created document item balance instance.
                   :param user_id:
                   :param doc_item:
               """

    item_balance = DocumentItemBalanceModel(
        item_id=doc_item.item_id,
        qty=doc_item.qty,
        currency_type_id=doc_item.currency_type_id,
        income_price=doc_item.income_price,
        selling_price=doc_item.selling_price,
        user_id=user_id,
        currency_id=doc_item.currency_id,
        income_price_usd=doc_item.income_price_usd,
        document_id=doc_item.document_id,
        document_item_id=doc_item.id,
        selling_percentage=doc_item.selling_percentage,
    )
    return item_balance

# def update_doc_item_balance(total_product, total_qty_kg, new_doc_item, product_item_balance):
#     """
#     Update an existing ProductDocItemBalance in the database.
#
#     Args:
#         total_product: The new total quantity of the product.
#         new_doc_item: An instance of the product document item with updated values.
#         product_item_balance: The instance of ProductDocItemBalance to update.
#
#     Returns:
#         ProductDocItemBalance: The updated document item balance instance.
#     """
#     with transaction.atomic():  # Begin a transaction
#         product_item_balance.qty = total_product
#         product_item_balance.qty_kg = total_qty_kg
#         product_item_balance.income_price = new_doc_item.income_price
#         product_item_balance.income_price_usd = new_doc_item.income_price_usd
#         product_item_balance.selling_price = new_doc_item.selling_price
#         product_item_balance.selling_percentage = new_doc_item.selling_percentage
#
#         product_item_balance.save()  # Save the updated instance
#
#     return product_item_balance
