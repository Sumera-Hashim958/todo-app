"""Add conversations and messages tables for Phase III

Revision ID: 001
Revises:
Create Date: 2026-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON
from datetime import datetime

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', UUID, primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('ix_conversations_user_updated', 'conversations', ['user_id', 'updated_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', UUID, primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('conversation_id', UUID, sa.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.Enum('user', 'assistant', name='messagerole'), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('tool_calls', JSON, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_index('ix_messages_conversation_time', 'messages', ['conversation_id', 'created_at'])

    # Enhance tasks table
    op.add_column('tasks', sa.Column('conversation_id', UUID, sa.ForeignKey('conversations.id', ondelete='SET NULL'), nullable=True))
    op.add_column('tasks', sa.Column('created_via', sa.Enum('chat', 'api', name='taskcreatedvia'), nullable=False, server_default='api'))
    op.create_index('ix_tasks_conversation_id', 'tasks', ['conversation_id'])


def downgrade():
    # Drop indexes and columns from tasks
    op.drop_index('ix_tasks_conversation_id', table_name='tasks')
    op.drop_column('tasks', 'created_via')
    op.drop_column('tasks', 'conversation_id')

    # Drop messages table
    op.drop_index('ix_messages_conversation_time', table_name='messages')
    op.drop_table('messages')

    # Drop conversations table
    op.drop_index('ix_conversations_user_updated', table_name='conversations')
    op.drop_index('ix_conversations_user_id', table_name='conversations')
    op.drop_table('conversations')

    # Drop enums
    op.execute('DROP TYPE IF EXISTS messagerole')
    op.execute('DROP TYPE IF EXISTS taskcreatedvia')
