from apps.base.models import Base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Date, DateTime, Float
from sqlalchemy.orm import relationship


class CustomerModel(Base):
    __tablename__ = 'customers'  # Specify the database table name
    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(15), nullable=False, unique=True)
    phone_number2 = Column(String(9), nullable=True, unique=True)
    address = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship to UserModel
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('UserModel', back_populates='customers')

    # Relationship to CustomerDebtModel
    customer_debts = relationship('CustomerDebtModel', back_populates='customer')


class CustomerDebtModel(Base):
    __tablename__ = 'customerdebts'
    is_paid = Column(Boolean, default=False)
    paid_date = Column(DateTime, nullable=True, onupdate=lambda: Base.get_tashkent_time())
    amount = Column(Float, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('CustomerModel', back_populates='customer_debts')
