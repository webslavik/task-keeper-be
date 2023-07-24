"""add birthday field to User

Revision ID: f3f01c71e8ca
Revises: f14469ef8e76
Create Date: 2023-07-24 17:13:32.052722

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'f3f01c71e8ca'
down_revision = 'f14469ef8e76'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('birthday', postgresql.TIMESTAMP(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'birthday')
