from __main__ import cache

from typing import Optional
from redis_om import HashModel


class ProjectCache(HashModel):
    project_id: str
    project_title: str
    creation_time: str
    production_time: str
    in_production: str
    project_language: str
    purpose: str
    purpose_other: str
    project_notes: str
    custom_record_label: str
    secondary_unique_field: str
    is_longitudinal: str
    has_repeating_instruments_or_events: str
    surveys_enabled: str
    scheduling_enabled: str
    record_autonumbering_enabled: str
    randomization_enabled: str
    ddp_enabled: str
    project_irb_number: str
    project_grant_number: str
    project_pi_firstname: str
    project_pi_lastname: str
    display_today_now_button: str
    missing_data_codes: str
    external_modules: str
    bypass_branching_erase_field_prompt: str


class DashboardCache(HashModel):
    name: str
    namespace: str
    endpoint: str


class StudyDashboardCache(DashboardCache):
    gender: str
    sex: str
    race: str
    ethnicity: str
    ancestry: str
    phenotype: str
    a1c: str
    recruitment_status: str
    consent_status: str
    survey_status: str
    communication_status: str
    device_status_es: str
    device_status_cgm: str
    device_status_amw: str
    device_status_all: str
    intervention_status: str
