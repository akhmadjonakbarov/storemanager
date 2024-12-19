import re
from sqlalchemy.orm import relationship, validates
from sqlalchemy import Column, String, Boolean
from sqlalchemy import Enum as SQLAlchemyEnum
import enum

from apps.base.models import Base


class UserRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class UserModel(Base):
    __tablename__ = 'users'

    first_name = Column(String(length=30))
    last_name = Column(String(length=30))
    is_active = Column(Boolean, default=True)
    email = Column(String(length=100), unique=True)
    password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.ADMIN)  # Default role

    # relationships
    debts = relationship('DebtModel', back_populates='user')
    items = relationship('ItemModel', back_populates='user')
    currencies = relationship('CurrencyModel', back_populates='user')
    documents = relationship('DocumentModel', back_populates='user')
    document_items = relationship('DocumentItemModel', back_populates='user')
    document_item_balances = relationship('DocumentItemBalanceModel', back_populates='user')
    customers = relationship('CustomerModel', back_populates='user')

    @validates('phone_number', 'phone_number2')
    def validate_phone_number(self, key, value):
        if value and not re.match(r'^\+?\d{9,15}$', value):
            raise ValueError('Invalid phone number format. Expected format: 901234567.')
        return value
