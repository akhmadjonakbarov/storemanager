"""create debts table

Revision ID: 8ae50bab9b90
Revises: 
Create Date: 2024-12-18 05:09:23.474889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from apps.base.models import Base

revision: str = '8ae50bab9b90'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'debts',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=lambda: Base.get_tashkent_time()),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column(
            'updated_at', sa.DateTime(), nullable=False,
            default=lambda: Base.get_tashkent_time(), onupdate=lambda: Base.get_tashkent_time()
        ),
        sa.Column(
            'is_deleted', sa.Boolean(),
            default=False,
            index=True, nullable=True,
        ),
        sa.Column('phone_number', sa.String(length=15), nullable=False),
        sa.Column('phone_number2', sa.String(length=15), nullable=True, default=None),
        sa.Column('address', sa.String(length=255), nullable=False),
        sa.Column('paid_date', sa.DateTime(), nullable=True, default=None, onupdate=lambda: Base.get_tashkent_time()),
        sa.Column('is_paid', sa.Boolean(), default=False),
        sa.Column('user_id', sa.Integer()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )

    def downgrade() -> None:
        pass
