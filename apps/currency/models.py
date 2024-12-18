from sqlalchemy import String, Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from apps.base.models import Base


class CurrencyModel(Base):
    __tablename__ = 'currencies'  # Specify the database table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Numeric(15, 3), default=0.0, nullable=True)
    # Relationship to CustomUserModel
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ForeignKey to CustomUserModel
    user = relationship('UserModel', back_populates='currencies')

    # Relationship to DocumentItemBalanceModel
    document_items = relationship('DocumentItemModel', back_populates='currency')
    document_item_balances = relationship('DocumentItemBalanceModel', back_populates='currency')


class CurrencyTypeModel(Base):
    __tablename__ = 'currency_types'  # Specify the database table name
    name = Column(String(10), unique=True)

    # Relationship to CurrencyModel
    document_items = relationship('DocumentItemModel', back_populates='currency_type')
    document_item_balances = relationship('DocumentItemBalanceModel', back_populates='currency_type')
