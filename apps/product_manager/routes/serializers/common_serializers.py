from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from apps.product_manager.models import ItemModel, UnitModel, CategoryModel
from apps.base.serializer_fields import SerializerExcludeFields


class CategoryModelSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = CategoryModel
        load_instance = True
        fields = ('id', 'name') + SerializerExcludeFields.date_fields


class UnitModelSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = UnitModel
        load_instance = True
        fields = ('id', 'value') + SerializerExcludeFields.date_fields


class ItemModelSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_instance = True
        fields = ('id', 'name', 'barcode', 'category', 'units') + SerializerExcludeFields.date_fields

    category = Nested(CategoryModelSerializer, many=False)
    units = Nested(UnitModelSerializer, many=True)
