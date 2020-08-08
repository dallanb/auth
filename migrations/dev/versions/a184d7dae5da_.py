"""empty message

Revision ID: a184d7dae5da
Revises: 06dc2e3a7621
Create Date: 2020-08-07 23:24:35.093843

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a184d7dae5da'
down_revision = '06dc2e3a7621'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token_status',
    sa.Column('ctime', sa.BigInteger(), nullable=True),
    sa.Column('mtime', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.Enum('active', 'inactive', name='tokenstatusenum'), nullable=False),
    sa.PrimaryKeyConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_role',
    sa.Column('ctime', sa.BigInteger(), nullable=True),
    sa.Column('mtime', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.Enum('member', 'admin', 'root', name='userroleenum'), nullable=False),
    sa.PrimaryKeyConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_status',
    sa.Column('ctime', sa.BigInteger(), nullable=True),
    sa.Column('mtime', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.Enum('pending', 'active', 'inactive', 'blocked', 'deleted', name='userstatusenum'), nullable=False),
    sa.PrimaryKeyConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.create_table('token',
    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('ctime', sa.BigInteger(), nullable=True),
    sa.Column('mtime', sa.BigInteger(), nullable=True),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('kong_jwt_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
    sa.Column('user_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('status', sa.Enum('active', 'inactive', name='tokenstatusenum'), nullable=True),
    sa.ForeignKeyConstraint(['status'], ['token_status.name'], ),
    sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('token'),
    sa.UniqueConstraint('uuid')
    )
    op.drop_constraint('user_status_uuid_fkey', 'user', type_='foreignkey')
    op.drop_constraint('user_role_uuid_fkey', 'user', type_='foreignkey')
    op.drop_table('userstatus')
    op.drop_table('userrole')
    op.drop_table('usertoken')
    op.add_column('user', sa.Column('role', sa.Enum('member', 'admin', 'root', name='userroleenum'), nullable=True))
    op.add_column('user', sa.Column('status', sa.Enum('pending', 'active', 'inactive', 'blocked', 'deleted', name='userstatusenum'), nullable=True))
    op.create_foreign_key(None, 'user', 'user_status', ['status'], ['name'])
    op.create_foreign_key(None, 'user', 'user_role', ['role'], ['name'])
    op.drop_column('user', 'role_uuid')
    op.drop_column('user', 'status_uuid')
    op.drop_column('user', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.add_column('user', sa.Column('status_uuid', postgresql.UUID(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('role_uuid', postgresql.UUID(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.create_foreign_key('user_role_uuid_fkey', 'user', 'userrole', ['role_uuid'], ['uuid'])
    op.create_foreign_key('user_status_uuid_fkey', 'user', 'userstatus', ['status_uuid'], ['uuid'])
    op.drop_column('user', 'status')
    op.drop_column('user', 'role')
    op.create_table('usertoken',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('uuid', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('ctime', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('mtime', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    
    sa.Column('status', postgresql.ENUM('active', 'inactive', name='usertokenstatusenum'), autoincrement=False, nullable=False),
    sa.Column('kong_jwt_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('user_uuid', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'], name='usertoken_user_uuid_fkey'),
    sa.PrimaryKeyConstraint('id', name='usertoken_pkey'),
    sa.UniqueConstraint('token', name='usertoken_token_key'),
    sa.UniqueConstraint('uuid', name='usertoken_uuid_key')
    )
    op.create_table('userrole',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('uuid', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('ctime', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('mtime', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('name', postgresql.ENUM('member', 'admin', 'root', name='userroleenum'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='userrole_pkey'),
    sa.UniqueConstraint('uuid', name='userrole_uuid_key')
    )
    op.create_table('userstatus',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('uuid', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('ctime', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('mtime', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('name', postgresql.ENUM('pending', 'active', 'inactive', 'blocked', 'deleted', name='userstatusenum'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='userstatus_pkey'),
    sa.UniqueConstraint('uuid', name='userstatus_uuid_key')
    )
    op.drop_table('token')
    op.drop_table('user_status')
    op.drop_table('user_role')
    op.drop_table('token_status')
    # ### end Alembic commands ###
