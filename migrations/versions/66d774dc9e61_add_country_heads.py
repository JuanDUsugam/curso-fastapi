"""Add country heads

Revision ID: 66d774dc9e61
Revises: 8093fec7cf18
Create Date: 2024-02-21 13:58:36.263144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66d774dc9e61'
down_revision: Union[str, None] = '8093fec7cf18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('pais', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuario', 'pais')
    # ### end Alembic commands ###