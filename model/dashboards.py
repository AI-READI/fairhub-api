from __main__ import cache

from typing import Optional
from pydantic import EmailStr
from redis_om import HashModel

class StudyDashboard(HashModel):

    gender              : str
    sex                 : str
    race                : str
    ethnicity           : str
    ancestry            : str
    phenotype           : str
    a1c                 : str
    recruitment_status  : str
    consent_status      : str
    survey_status       : str
    communication_status: str
    device_status_es    : str
    device_status_cgm   : str
    device_status_amw   : str
    device_status_all   : str
    intervention_status : str
