"""init-database

Revision ID: 63d8835bbaaf
Revises:
Create Date: 2026-01-04 22:52:18.481275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '63d8835bbaaf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('published_dataset',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('study_id', sa.String(), nullable=False),
    sa.Column('dataset_id', sa.String(), nullable=False),
    sa.Column('version_id', sa.String(), nullable=False),
    sa.Column('doi', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('version_title', sa.String(), nullable=False),
    sa.Column('study_title', sa.String(), nullable=False),
    sa.Column('published_metadata', sa.JSON(), nullable=False),
    sa.Column('files', sa.JSON(), nullable=False),
    sa.Column('data', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('title', sa.String(length=300), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('short_description', sa.String(length=300), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('updated_on', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('email_address', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hash', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('email_verified', sa.BOOLEAN(), nullable=True),
    sa.Column('password_reset_token', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email_address'),
    sa.UniqueConstraint('username')
    )
    op.create_table('dataset',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('updated_on', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('email_verification',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invited_study_contributor',
    sa.Column('email_address', sa.String(), nullable=False),
    sa.Column('permission', sa.String(), nullable=False),
    sa.Column('invited_on', sa.BigInteger(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('email_address', 'study_id')
    )
    op.create_table('notification',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('target', sa.String(), nullable=True),
    sa.Column('read', sa.BOOLEAN(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participant',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('age', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('updated_on', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('session',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('expires_at', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_arm',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('label', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('intervention_list', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_central_contact',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('degree', sa.String(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('identifier_scheme', sa.String(), nullable=False),
    sa.Column('identifier_scheme_uri', sa.String(), nullable=False),
    sa.Column('affiliation', sa.String(), nullable=False),
    sa.Column('affiliation_identifier', sa.String(), nullable=False),
    sa.Column('affiliation_identifier_scheme', sa.String(), nullable=False),
    sa.Column('affiliation_identifier_scheme_uri', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('phone_ext', sa.String(), nullable=False),
    sa.Column('email_address', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_collaborators',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('scheme', sa.String(), nullable=False),
    sa.Column('scheme_uri', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_conditions',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('classification_code', sa.String(), nullable=False),
    sa.Column('scheme', sa.String(), nullable=False),
    sa.Column('scheme_uri', sa.String(), nullable=False),
    sa.Column('condition_uri', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_contributor',
    sa.Column('permission', sa.String(), nullable=False),
    sa.Column('user_id', sa.CHAR(length=36), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'study_id')
    )
    op.create_table('study_description',
    sa.Column('brief_summary', sa.String(), nullable=False),
    sa.Column('detailed_description', sa.String(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('study_id')
    )
    op.create_table('study_design',
    sa.Column('design_allocation', sa.String(), nullable=True),
    sa.Column('study_type', sa.String(), nullable=True),
    sa.Column('design_intervention_model', sa.String(), nullable=True),
    sa.Column('design_intervention_model_description', sa.String(), nullable=False),
    sa.Column('design_primary_purpose', sa.String(), nullable=True),
    sa.Column('design_masking', sa.String(), nullable=True),
    sa.Column('design_masking_description', sa.String(), nullable=True),
    sa.Column('design_who_masked_list', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('phase_list', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('enrollment_count', sa.Integer(), nullable=True),
    sa.Column('enrollment_type', sa.String(), nullable=True),
    sa.Column('number_arms', sa.Integer(), nullable=True),
    sa.Column('design_observational_model_list', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('design_time_perspective_list', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('bio_spec_retention', sa.String(), nullable=True),
    sa.Column('bio_spec_description', sa.String(), nullable=True),
    sa.Column('target_duration', sa.String(), nullable=True),
    sa.Column('is_patient_registry', sa.String(), nullable=True),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('study_id')
    )
    op.create_table('study_eligibility',
    sa.Column('sex', sa.String(), nullable=True),
    sa.Column('gender_based', sa.String(), nullable=True),
    sa.Column('gender_description', sa.String(), nullable=False),
    sa.Column('minimum_age_value', sa.Integer(), nullable=True),
    sa.Column('maximum_age_value', sa.Integer(), nullable=True),
    sa.Column('minimum_age_unit', sa.String(), nullable=True),
    sa.Column('maximum_age_unit', sa.String(), nullable=True),
    sa.Column('healthy_volunteers', sa.String(), nullable=True),
    sa.Column('inclusion_criteria', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('exclusion_criteria', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('study_population', sa.String(), nullable=False),
    sa.Column('sampling_method', sa.String(), nullable=True),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('study_id')
    )
    op.create_table('study_identification',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('identifier_type', sa.String(), nullable=True),
    sa.Column('identifier_domain', sa.String(), nullable=False),
    sa.Column('identifier_link', sa.String(), nullable=False),
    sa.Column('secondary', sa.BOOLEAN(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_intervention',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('other_name_list', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_keywords',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('classification_code', sa.String(), nullable=False),
    sa.Column('scheme', sa.String(), nullable=False),
    sa.Column('scheme_uri', sa.String(), nullable=False),
    sa.Column('keyword_uri', sa.String(), nullable=False),
    sa.Column('created_at', sa.String(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_location',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('facility', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('zip', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_other',
    sa.Column('size', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('study_id')
    )
    op.create_table('study_overall_official',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('degree', sa.String(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('identifier_scheme', sa.String(), nullable=False),
    sa.Column('identifier_scheme_uri', sa.String(), nullable=False),
    sa.Column('affiliation', sa.String(), nullable=False),
    sa.Column('affiliation_identifier', sa.String(), nullable=False),
    sa.Column('affiliation_identifier_scheme', sa.String(), nullable=False),
    sa.Column('affiliation_identifier_scheme_uri', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_oversight',
    sa.Column('fda_regulated_drug', sa.String(), nullable=True),
    sa.Column('fda_regulated_device', sa.String(), nullable=True),
    sa.Column('human_subject_review_status', sa.String(), nullable=True),
    sa.Column('has_dmc', sa.String(), nullable=True),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('study_id')
    )
    op.create_table('study_redcap',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('api_pid', sa.BigInteger(), nullable=True),
    sa.Column('api_url', sa.String(), nullable=True),
    sa.Column('api_key', sa.String(), nullable=True),
    sa.Column('api_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('updated_on', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_sponsors',
    sa.Column('responsible_party_type', sa.String(), nullable=True),
    sa.Column('responsible_party_investigator_first_name', sa.String(), nullable=False),
    sa.Column('responsible_party_investigator_last_name', sa.String(), nullable=False),
    sa.Column('responsible_party_investigator_title', sa.String(), nullable=False),
    sa.Column('responsible_party_investigator_identifier_value', sa.String(), nullable=False),
    sa.Column('responsible_party_investigator_identifier_scheme', sa.String(), nullable=False),
    sa.Column('responsible_party_investigator_identifier_scheme_uri', sa.String(), nullable=False),
    sa.Column('responsible_party_investigator_affiliation_name', sa.String(), nullable=False),
    sa.Column('responsible_party_investigator_affiliation_identifier_value', sa.String(), nullable=False),
    sa.Column('responsible_party_investigator_affiliation_identifier_scheme', sa.String(), nullable=False),
    sa.Column('responsible_party_investigator_affiliation_identifier_scheme_uri', sa.String(), nullable=False),
    sa.Column('lead_sponsor_name', sa.String(), nullable=False),
    sa.Column('lead_sponsor_identifier', sa.String(), nullable=False),
    sa.Column('lead_sponsor_identifier_scheme', sa.String(), nullable=False),
    sa.Column('lead_sponsor_identifier_scheme_uri', sa.String(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('study_id')
    )
    op.create_table('study_status',
    sa.Column('overall_status', sa.String(), nullable=True),
    sa.Column('why_stopped', sa.String(), nullable=False),
    sa.Column('start_date', sa.String(), nullable=True),
    sa.Column('start_date_type', sa.String(), nullable=True),
    sa.Column('completion_date', sa.String(), nullable=True),
    sa.Column('completion_date_type', sa.String(), nullable=True),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('study_id')
    )
    op.create_table('token_blacklist',
    sa.Column('jti', sa.CHAR(length=36), nullable=False),
    sa.Column('exp', sa.String(), nullable=False),
    sa.Column('user_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('jti')
    )
    op.create_table('user_details',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('institution', sa.String(), nullable=True),
    sa.Column('orcid', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('profile_image', sa.String(), nullable=True),
    sa.Column('timezone', sa.String(), nullable=True),
    sa.Column('user_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dataset_access',
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('url_last_checked', sa.BigInteger(), nullable=True),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('dataset_id')
    )
    op.create_table('dataset_alternate_identifier',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dataset_consent',
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('noncommercial', sa.BOOLEAN(), nullable=False),
    sa.Column('geog_restrict', sa.BOOLEAN(), nullable=False),
    sa.Column('research_type', sa.BOOLEAN(), nullable=False),
    sa.Column('genetic_only', sa.BOOLEAN(), nullable=False),
    sa.Column('no_methods', sa.BOOLEAN(), nullable=False),
    sa.Column('details', sa.String(), nullable=False),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('dataset_id')
    )
    op.create_table('dataset_contributor',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('family_name', sa.String(), nullable=True),
    sa.Column('given_name', sa.String(), nullable=False),
    sa.Column('name_type', sa.String(), nullable=True),
    sa.Column('name_identifier', sa.String(), nullable=False),
    sa.Column('name_identifier_scheme', sa.String(), nullable=False),
    sa.Column('name_identifier_scheme_uri', sa.String(), nullable=False),
    sa.Column('creator', sa.BOOLEAN(), nullable=False),
    sa.Column('contributor_type', sa.String(), nullable=True),
    sa.Column('affiliations', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dataset_date',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('date', sa.BigInteger(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('information', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dataset_de_ident_level',
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('direct', sa.BOOLEAN(), nullable=False),
    sa.Column('hipaa', sa.BOOLEAN(), nullable=False),
    sa.Column('dates', sa.BOOLEAN(), nullable=False),
    sa.Column('nonarr', sa.BOOLEAN(), nullable=False),
    sa.Column('k_anon', sa.BOOLEAN(), nullable=False),
    sa.Column('details', sa.String(), nullable=False),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('dataset_id')
    )
    op.create_table('dataset_description',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dataset_funder',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('identifier_type', sa.String(), nullable=True),
    sa.Column('identifier_scheme_uri', sa.String(), nullable=False),
    sa.Column('award_number', sa.String(), nullable=False),
    sa.Column('award_uri', sa.String(), nullable=False),
    sa.Column('award_title', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dataset_healthsheet',
    sa.Column('motivation', sa.JSON(), nullable=False),
    sa.Column('composition', sa.JSON(), nullable=False),
    sa.Column('collection', sa.JSON(), nullable=False),
    sa.Column('preprocessing', sa.JSON(), nullable=False),
    sa.Column('uses', sa.JSON(), nullable=False),
    sa.Column('distribution', sa.JSON(), nullable=False),
    sa.Column('maintenance', sa.JSON(), nullable=False),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('dataset_id')
    )
    op.create_table('dataset_managing_organization',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('identifier_scheme', sa.String(), nullable=False),
    sa.Column('identifier_scheme_uri', sa.String(), nullable=False),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('dataset_id')
    )
    op.create_table('dataset_other',
    sa.Column('resource_type', sa.String(), nullable=False),
    sa.Column('language', sa.String(), nullable=True),
    sa.Column('size', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('format', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('standards_followed', sa.String(), nullable=False),
    sa.Column('acknowledgement', sa.String(), nullable=False),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('dataset_id')
    )
    op.create_table('dataset_related_identifier',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('identifier_type', sa.String(), nullable=True),
    sa.Column('relation_type', sa.String(), nullable=True),
    sa.Column('related_metadata_scheme', sa.String(), nullable=False),
    sa.Column('scheme_uri', sa.String(), nullable=False),
    sa.Column('scheme_type', sa.String(), nullable=False),
    sa.Column('resource_type', sa.String(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dataset_rights',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('rights', sa.String(), nullable=False),
    sa.Column('uri', sa.String(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('identifier_scheme', sa.String(), nullable=False),
    sa.Column('identifier_scheme_uri', sa.String(), nullable=False),
    sa.Column('license_text', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dataset_subject',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('subject', sa.String(), nullable=False),
    sa.Column('scheme', sa.String(), nullable=False),
    sa.Column('scheme_uri', sa.String(), nullable=False),
    sa.Column('value_uri', sa.String(), nullable=False),
    sa.Column('classification_code', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dataset_title',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('dataset_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_dashboard',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('modules', sa.JSON(), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.Column('redcap_pid', sa.BigInteger(), nullable=True),
    sa.Column('reports', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('updated_on', sa.BigInteger(), nullable=False),
    sa.Column('study_id', sa.CHAR(length=36), nullable=False),
    sa.Column('redcap_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['redcap_id'], ['study_redcap.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_location_contact_list',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('identifier_scheme', sa.String(), nullable=False),
    sa.Column('zip', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('phone_ext', sa.String(), nullable=False),
    sa.Column('email_address', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('study_location_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['study_location_id'], ['study_location.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.execute(sa.text("CREATE SEQUENCE version_identifier_seq"))

    op.create_table('version',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('published', sa.BOOLEAN(), nullable=False),
    sa.Column('changelog', sa.String(), nullable=False),
    sa.Column('updated_on', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('published_on', sa.BigInteger(), nullable=False),
    sa.Column('identifier', sa.Integer(), server_default=sa.text("nextval('version_identifier_seq')"), nullable=False),
    sa.Column('doi', sa.String(), nullable=True),
    sa.Column('dataset_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('doi'),
    sa.UniqueConstraint('identifier')
    )
    op.create_table('version_participants',
    sa.Column('dataset_version_id', sa.CHAR(length=36), nullable=False),
    sa.Column('participant_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['dataset_version_id'], ['version.id'], ),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
    sa.PrimaryKeyConstraint('dataset_version_id', 'participant_id')
    )
    op.create_table('version_readme',
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('version_id', sa.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['version_id'], ['version.id'], ),
    sa.PrimaryKeyConstraint('version_id')
    )
    op.drop_table('_prisma_migrations')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('_prisma_migrations',
    sa.Column('id', sa.VARCHAR(length=36), autoincrement=False, nullable=False),
    sa.Column('checksum', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('finished_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('migration_name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('logs', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('rolled_back_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('started_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('applied_steps_count', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='_prisma_migrations_pkey')
    )
    op.drop_table('version_readme')
    op.drop_table('version_participants')
    op.drop_table('version')
    op.drop_table('study_location_contact_list')
    op.drop_table('study_dashboard')
    op.drop_table('dataset_title')
    op.drop_table('dataset_subject')
    op.drop_table('dataset_rights')
    op.drop_table('dataset_related_identifier')
    op.drop_table('dataset_other')
    op.drop_table('dataset_managing_organization')
    op.drop_table('dataset_healthsheet')
    op.drop_table('dataset_funder')
    op.drop_table('dataset_description')
    op.drop_table('dataset_de_ident_level')
    op.drop_table('dataset_date')
    op.drop_table('dataset_contributor')
    op.drop_table('dataset_consent')
    op.drop_table('dataset_alternate_identifier')
    op.drop_table('dataset_access')
    op.drop_table('user_details')
    op.drop_table('token_blacklist')
    op.drop_table('study_status')
    op.drop_table('study_sponsors')
    op.drop_table('study_redcap')
    op.drop_table('study_oversight')
    op.drop_table('study_overall_official')
    op.drop_table('study_other')
    op.drop_table('study_location')
    op.drop_table('study_keywords')
    op.drop_table('study_intervention')
    op.drop_table('study_identification')
    op.drop_table('study_eligibility')
    op.drop_table('study_design')
    op.drop_table('study_description')
    op.drop_table('study_contributor')
    op.drop_table('study_conditions')
    op.drop_table('study_collaborators')
    op.drop_table('study_central_contact')
    op.drop_table('study_arm')
    op.drop_table('session')
    op.drop_table('participant')
    op.drop_table('notification')
    op.drop_table('invited_study_contributor')
    op.drop_table('email_verification')
    op.drop_table('dataset')
    op.drop_table('user')
    op.drop_table('study')
    op.drop_table('published_dataset')
    # ### end Alembic commands ###
