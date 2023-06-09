"""v 0.2 add category to article

Revision ID: 0cf1d41d3e5c
Revises: 6ab248fc04f0
Create Date: 2023-04-11 09:40:39.452343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cf1d41d3e5c'
down_revision = '6ab248fc04f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('category', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'category')
    # ### end Alembic commands ###
