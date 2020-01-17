"""empty message

Revision ID: 63a32ab6673d
Revises: 
Create Date: 2020-01-17 23:47:16.531407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63a32ab6673d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('education',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('email_domain', sa.Text(), nullable=True),
    sa.Column('url', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employment_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('perk',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('listed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('listed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('submission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('salary', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('years_experience', sa.Integer(), nullable=True),
    sa.Column('years_with_current_employer', sa.Integer(), nullable=True),
    sa.Column('number_of_employers', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('confirmation_code', sa.String(length=255), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tech',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('listed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('submission_to_education',
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('education_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['education_id'], ['education.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('submission_id', 'education_id')
    )
    op.create_table('submission_to_employment_type',
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('employment_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['employment_type_id'], ['employment_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('submission_id', 'employment_type_id')
    )
    op.create_table('submission_to_location',
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('submission_id', 'location_id')
    )
    op.create_table('submission_to_perk',
    sa.Column('value', sa.Numeric(), nullable=True),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('perk_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['perk_id'], ['perk.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('submission_id', 'perk_id')
    )
    op.create_table('submission_to_role',
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('submission_id', 'role_id')
    )
    op.create_table('submission_to_tech',
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('tech_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tech_id'], ['tech.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('submission_id', 'tech_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('submission_to_tech')
    op.drop_table('submission_to_role')
    op.drop_table('submission_to_perk')
    op.drop_table('submission_to_location')
    op.drop_table('submission_to_employment_type')
    op.drop_table('submission_to_education')
    op.drop_table('tech')
    op.drop_table('submission')
    op.drop_table('role')
    op.drop_table('perk')
    op.drop_table('location')
    op.drop_table('employment_type')
    op.drop_table('employer')
    op.drop_table('education')
    # ### end Alembic commands ###
