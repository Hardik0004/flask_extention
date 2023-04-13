"""v 0 1 user and article and save it

Revision ID: 6ab248fc04f0
Revises: 
Create Date: 2023-04-10 18:14:56.412985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ab248fc04f0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_info',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('user_name', sa.String(length=128), nullable=False),
    sa.Column('email_id', sa.String(length=128), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('modified_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('article',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.Column('article_link', sa.String(length=1028), nullable=False),
    sa.Column('image_link', sa.String(length=1028), nullable=False),
    sa.Column('website_name', sa.String(length=1028), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('modified_on', sa.DateTime(), nullable=True),
    sa.Column('share', sa.Integer(), autoincrement=True, nullable=True),
    sa.Column('watch', sa.Integer(), autoincrement=True, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('saved_article',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('article_id', sa.String(length=36), nullable=True),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('modified_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_info.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('saved_article')
    op.drop_table('article')
    op.drop_table('user_info')
    # ### end Alembic commands ###
