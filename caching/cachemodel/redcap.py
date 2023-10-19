from redis_om import JsonModel


class REDCapProjectCacheModel(JsonModel):
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
