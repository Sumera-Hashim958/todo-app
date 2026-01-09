"""Add users table for Phase II authentication

Revision ID: 002
Revises: 001
Create Date: 2026-01-06
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    # Create index on email for fast lookups
    op.create_index('ix_users_email', 'users', ['email'], unique=True)


def downgrade():
    # Drop index and table
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
