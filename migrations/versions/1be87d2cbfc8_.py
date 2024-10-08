"""empty message

Revision ID: 1be87d2cbfc8
Revises: cb12722e63d2
Create Date: 2024-10-07 00:40:03.748810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1be87d2cbfc8'
down_revision = 'cb12722e63d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_planets_favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('planets_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planets_id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_planets_favorites')
    # ### end Alembic commands ###
