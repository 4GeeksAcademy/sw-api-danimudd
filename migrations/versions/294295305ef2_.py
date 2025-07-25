"""empty message

Revision ID: 294295305ef2
Revises: a5cffa318ac2
Create Date: 2025-07-19 18:31:16.872856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '294295305ef2'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('climate', sa.String(), nullable=False),
    sa.Column('population', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('starship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('cargo_space', sa.String(), nullable=False),
    sa.Column('speed', sa.Integer(), nullable=False),
    sa.Column('occupancy', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('hair_color', sa.String(), nullable=False),
    sa.Column('eye_color', sa.String(), nullable=False),
    sa.Column('species', sa.String(), nullable=False),
    sa.Column('origin_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['origin_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('class_type', sa.String(), nullable=False),
    sa.Column('weilder_id', sa.Integer(), nullable=False),
    sa.Column('power_source', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['weilder_id'], ['character.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weapon')
    op.drop_table('character')
    op.drop_table('starship')
    op.drop_table('planet')
    # ### end Alembic commands ###
