from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apps.product_manager import models as product_models
from .nested_serializers import NestedSerializerMixin


class DocumentItemModelSerializer(SQLAlchemyAutoSchema, NestedSerializerMixin):
    class Meta:
        model = product_models.DocumentItemModel
        fields = (
            'id', 'item', 'created_at', 'updated_at', 'currency_type',
            'qty', 'qty_kg', 'selling_price', 'selling_percentage',
            'income_price_usd', 'income_price',
            'document', 'currency'
        )


class DocumentItemModelSerializerForItem(SQLAlchemyAutoSchema, NestedSerializerMixin):
    class Meta:
        model = product_models.DocumentItemModel
        fields = (
            'id', 'created_at', 'updated_at', 'currency_type',
            'qty', 'qty_kg', 'selling_price', 'selling_percentage',
            'income_price_usd', 'income_price', 'document'
        )
