"""rename user to users

Revision ID: a1b2c3d4e5f6
Revises: 6eea3c2a9579
Create Date: 2026-01-31 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '6eea3c2a9579'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('user', 'users')


def downgrade():
    op.rename_table('users', 'user')
