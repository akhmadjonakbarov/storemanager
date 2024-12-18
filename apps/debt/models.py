from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from apps.base.models import Base


class DebtModel(Base):
    __tablename__ = 'debts'  # Adjust table name as needed

    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(15), nullable=False)  # Adjust max_length as needed
    phone_number2 = Column(String(15), nullable=True, default=None)  # Adjust max_length as needed
    address = Column(String(255), nullable=False)
    is_paid = Column(Boolean, default=False)
    amount = Column(Numeric(15, 3), nullable=False)

    # Relationship to UserModel
    user_id = Column(
        Integer, ForeignKey('users.id'),
        nullable=False
    )
    user = relationship(
        'UserModel',
        back_populates='debts'
    )
