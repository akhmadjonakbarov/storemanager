from sqlalchemy.orm import relationship
from apps.base.models import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Numeric


class CompanyModel(Base):
    __tablename__ = 'companies'
    name = Column(String(100), unique=True, nullable=True)


class CategoryModel(Base):
    __tablename__ = 'categories'
    name = Column(String(100), unique=True, nullable=True)

    # relationships
    items = relationship('ItemModel', back_populates='category')


class UnitModel(Base):
    __tablename__ = 'units'
    value = Column(String(25), unique=True, nullable=False)

    # relationships
    items = relationship('ItemModel', back_populates='unit')


class ItemModel(Base):
    __tablename__ = 'items'
    name = Column(String(100), nullable=False)
    barcode = Column(String(100), nullable=False, unique=True)
    # categories relationships
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    category = relationship('CategoryModel', back_populates='items')

    # unit relationships
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    unit = relationship('UnitModel', back_populates='items')

    # user relationships
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('UserModel', back_populates='items')

    # document item relationships
    document_items = relationship('DocumentItemModel', back_populates='item')
    document_item_balances = relationship('DocumentItemBalanceModel', back_populates='item')


class DocumentModel(Base):
    __tablename__ = 'documents'
    SELL = 'sell'
    BUY = 'buy'
    reg_date = Column(DateTime, default=Base.get_tashkent_time)
    doc_type = Column(String(length=4), nullable=False)
    # relationships
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship('UserModel', back_populates='documents')

    # back_populates
    document_items = relationship('DocumentItemModel', back_populates='document')
    document_item_balances = relationship('DocumentItemBalanceModel', back_populates='document')


class DocumentItemModel(Base):
    __tablename__ = 'document_items'
    qty = Column(Integer, default=0, nullable=False)
    income_price_usd = Column(Numeric(15, 3), default=0.0)  # DecimalField equivalent
    income_price = Column(Numeric(15, 3), default=0.0)  # DecimalField equivalent
    selling_price = Column(Numeric(15, 3), default=0.0)  # DecimalField equivalent
    selling_percentage = Column(Numeric(15, 3), default=0.0)  # DecimalField equivalent
    # relationships
    # user
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('UserModel', back_populates='document_items')
    # doc
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False)
    document = relationship('DocumentModel', back_populates='document_items')
    # currency type
    currency_type_id = Column(Integer, ForeignKey('currency_types.id'), nullable=False)
    currency_type = relationship('CurrencyTypeModel', back_populates='document_items')
    # currency
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=True)
    currency = relationship('CurrencyModel', back_populates='document_items')
    # item
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    item = relationship('ItemModel', back_populates='document_items')

    document_item_balances = relationship('DocumentItemBalanceModel', back_populates='document_item')


class DocumentItemBalanceModel(Base):
    __tablename__ = 'document_item_balances'
    qty = Column(Integer, default=0, nullable=False)
    income_price_usd = Column(Numeric(15, 3), default=0.0)  # DecimalField equivalent
    income_price = Column(Numeric(15, 3), default=0.0)  # DecimalField equivalent
    selling_price = Column(Numeric(15, 3), default=0.0)  # DecimalField equivalent
    selling_percentage = Column(Numeric(15, 3), default=0.0)  # DecimalField equivalent
    # relationships
    # user
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('UserModel', back_populates='document_item_balances')
    # doc
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False)
    document = relationship('DocumentModel', back_populates='document_item_balances')
    # currency type
    currency_type_id = Column(Integer, ForeignKey('currency_types.id'), nullable=False)
    currency_type = relationship('CurrencyTypeModel', back_populates='document_item_balances')
    # currency
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=True)
    currency = relationship('CurrencyModel', back_populates='document_item_balances')
    # item
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    item = relationship('ItemModel', back_populates='document_item_balances')
    # doc_item
    document_item_id = Column(Integer, ForeignKey('document_items.id'), nullable=False)
    document_item = relationship('DocumentItemModel', back_populates='document_item_balances')
