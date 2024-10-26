"""init

Revision ID: c9b05cfb62f3
Revises: 
Create Date: 2022-06-02 00:57:03.860048

"""
import datetime

from alembic import op
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'c9b05cfb62f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('site_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('modified_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('mobile', sa.String(length=10), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('registered_on', sa.DateTime(), nullable=True),
    sa.Column('user_type', sa.String(), nullable=False),
    sa.Column('public_id', sa.String(length=36), nullable=True),
    sa.Column('created_by', sa.String(length=36), nullable=True),
    sa.Column('modified_by', sa.String(length=36), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('middle_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['site_user.public_id'], ),
    sa.ForeignKeyConstraint(['modified_by'], ['site_user.public_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('mobile'),
    sa.UniqueConstraint('public_id')
    )
    # Insert default super admin with password admin@123
    op.execute(f"INSERT INTO site_user "
               f"(is_deleted, email, mobile, password_hash, registered_on, user_type, public_id) "
               f"VALUES "
               f"('0','sachin@demo.com', '9999911111', "
               f"'$2b$12$iXS8TFkM4Yn8AJK/.WtyfeBmVEVEbGyglaFbR01E3DCe3I/xeT5DC', "
               f"'{datetime.datetime.now()}', 'SUPER_ADMIN', 'aaa125e6-fec5-43ce-88eb-891739c3ca7e')")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('site_user')
    # ### end Alembic commands ###
