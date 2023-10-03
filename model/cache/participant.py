from redis_om import HashModel


class ParticipantCache(HashModel):
    studyid: str
    data_management_complete: str
