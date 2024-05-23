"""Adding models

Revision ID: ed0aabbe9074
Revises: 
Create Date: 2024-05-22 12:42:05.182977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed0aabbe9074'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('translation_texts',
    sa.Column('uuid', sa.UUID(), server_default=sa.text('(gen_random_uuid())'), nullable=False),
    sa.Column('status', sa.Enum('pending', 'completed', name='status_types'), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('translations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text_id', sa.UUID(), nullable=True),
    sa.Column('language', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['text_id'], ['translation_texts.uuid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('translations')
    op.drop_table('translation_texts')
    # ### end Alembic commands ###
