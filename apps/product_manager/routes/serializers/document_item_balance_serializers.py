from marshmallow.fields import Nested
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from apps.product_manager.models import DocumentItemBalanceModel
from apps.currency.serializers import CurrencyModelSerializer, CurrencyTypeModelSerializer
from .common_serializers import ItemModelSerializer
from .document_serializers import DocumentModelSerializer
from apps.base.serializer_fields import SerializerExcludeFields
from .nested_serializers import NestedSerializerMixin


class DocumentItemBalanceModelSerializer(SQLAlchemyAutoSchema, NestedSerializerMixin):
    class Meta:
        model = DocumentItemBalanceModel
        load_instance = True
        fields = (
                     'id', 'item', 'currency_type',
                     'qty', 'selling_price', 'selling_percentage',
                     'income_price_usd', 'income_price', 'document', 'currency'
                 ) + SerializerExcludeFields.date_fields
