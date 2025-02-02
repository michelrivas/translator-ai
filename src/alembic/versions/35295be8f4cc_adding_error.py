"""Adding error

Revision ID: 35295be8f4cc
Revises: ed0aabbe9074
Create Date: 2024-05-22 16:35:32.769288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35295be8f4cc'
down_revision: Union[str, None] = 'ed0aabbe9074'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('translations', sa.Column('error', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('translations', 'error')
    # ### end Alembic commands ###
