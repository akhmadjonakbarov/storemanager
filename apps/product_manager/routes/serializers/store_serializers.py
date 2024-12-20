from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apps.base.serializer_fields import SerializerExcludeFields
from apps.product_manager.models import ItemModel, DocumentItemBalanceModel
from .nested_serializers import NestedSerializerMixin


class StoreItemModelSerializer(SQLAlchemyAutoSchema, NestedSerializerMixin):
    class Meta:
        model = ItemModel
        fields = (
                     'id', 'category', 'units',
                     'name', 'barcode',
                 ) + SerializerExcludeFields.date_fields


class StoreDocumentItemBalanceModelSerializer(SQLAlchemyAutoSchema, NestedSerializerMixin):
    class Meta:
        model = DocumentItemBalanceModel
        load_instance = True
        fields = (
                     'id', 'item', 'income_price_usd', 'currency_type',
                     'income_price', 'selling_price',
                     'selling_percentage', 'qty',
                     'document', 'currency'
                 ) + SerializerExcludeFields.date_fields
