from marshmallow.fields import Nested

from apps.currency.serializers import CurrencyModelSerializer, CurrencyTypeModelSerializer
from apps.product_manager.routes.serializers import document_serializers, common_serializers


class NestedSerializerMixin:
    currency = Nested(CurrencyModelSerializer, many=False)
    currency_type = Nested(CurrencyTypeModelSerializer, many=False)
    item = Nested(common_serializers.ItemModelSerializer, many=False)
    document = Nested(document_serializers.DocumentModelSerializer, many=False)
    category = Nested(common_serializers.CategoryModelSerializer, many=False)
    units = Nested(common_serializers.UnitModelSerializer, many=True)
