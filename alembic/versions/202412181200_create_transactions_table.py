"""create transactions table

Revision ID: 202412181200
Revises: 
Create Date: 2024-12-18 12:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '202412181200'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'transactions',
        sa.Column('transaction_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('transaction_id'),
        sa.UniqueConstraint('transaction_id', name='uix_transaction_id')
    )

    op.create_index('ix_transactions_transaction_id', 'transactions', ['transaction_id'])
    op.create_index('ix_transactions_user_id', 'transactions', ['user_id'])


def downgrade():
    op.drop_index('ix_transactions_transaction_id', table_name='transactions')
    op.drop_index('ix_transactions_user_id', table_name='transactions')
    op.drop_table('transactions')
