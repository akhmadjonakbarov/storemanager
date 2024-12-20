from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from apps.product_manager.models import DocumentModel
from apps.base.serializer_fields import SerializerExcludeFields


class DocumentModelSerializer(SQLAlchemyAutoSchema):
    type_of_items = fields.Method("get_type_of_items")
    total_items_qty = fields.Method("get_total_items_qty")
    total_price = fields.Method("get_total_price")

    class Meta:
        model = DocumentModel
        load_instance = True
        fields = (
                     'id', 'reg_date', 'doc_type',
                     'type_of_items', 'total_items_qty', 'total_price'
                 ) + SerializerExcludeFields.date_fields

    def get_type_of_items(self, doc: DocumentModel):
        return len(doc.document_items)  # Assuming `doc.items` is a relationship

    def get_total_items_qty(self, doc: DocumentModel):
        return sum(item.qty for item in doc.document_items)  # Assuming `qty` is a field in the related items

    def get_total_price(self, doc: DocumentModel):
        if doc.doc_type == DocumentModel.SELL:
            return sum(
                item.selling_price * item.qty for item in doc.document_items)  # Replace with your actual field names
        else:
            return sum(item.income_price * item.qty for item in doc.document_items)
