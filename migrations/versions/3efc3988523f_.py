"""empty message

Revision ID: 3efc3988523f
Revises: f04efd28a7d9
Create Date: 2024-04-01 13:46:33.350289

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3efc3988523f'
down_revision = 'f04efd28a7d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_name', sa.String(length=250), nullable=False),
    sa.Column('biography', sa.String(length=5000), nullable=False),
    sa.Column('nationality', sa.String(length=250), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=250), nullable=False),
    sa.Column('author', sa.String(length=250), nullable=False),
    sa.Column('isbn', sa.String(length=250), nullable=False),
    sa.Column('genre', sa.String(length=250), nullable=True),
    sa.Column('publication_year', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.drop_table('author')
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.drop_index('title')

    op.drop_table('books')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=250), nullable=False),
    sa.Column('author', mysql.VARCHAR(length=250), nullable=False),
    sa.Column('isbn', mysql.VARCHAR(length=250), nullable=False),
    sa.Column('genre', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('publication_year', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('profile_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], name='books_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.create_index('title', ['title'], unique=True)

    op.create_table('author',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('author_name', mysql.VARCHAR(length=250), nullable=False),
    sa.Column('biography', mysql.VARCHAR(length=5000), nullable=False),
    sa.Column('nationality', mysql.VARCHAR(length=250), nullable=False),
    sa.Column('profile_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], name='author_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('Books')
    op.drop_table('Author')
    # ### end Alembic commands ###
