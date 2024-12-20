from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import CurrencyModel, CurrencyTypeModel


class CurrencyModelSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = CurrencyModel
        load_instance = True
        fields = ('id', 'value', 'created_at')


class CurrencyTypeModelSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = CurrencyTypeModel
        load_instance = True
        fields = ('id', 'name')
