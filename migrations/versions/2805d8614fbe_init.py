"""init

Revision ID: 2805d8614fbe
Revises:
Create Date: 2023-01-22 19:53:43.663982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2805d8614fbe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exercises',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('number_approaches', sa.Integer(), nullable=True),
    sa.Column('number_repetitions', sa.String(), nullable=True),
    sa.Column('day', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('programs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('program_exercises',
    sa.Column('program_id', sa.Integer(), nullable=True),
    sa.Column('exercises_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exercises_id'], ['exercises.id'], ),
    sa.ForeignKeyConstraint(['program_id'], ['programs.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('program_exercises')
    op.drop_table('programs')
    op.drop_table('exercises')
    op.drop_table('category')
    # ### end Alembic commands ###
