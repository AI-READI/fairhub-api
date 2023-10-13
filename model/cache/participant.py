from redis_om import HashModel


class ParticipantCache(HashModel):
    studyid: str
    dm__i: str
    dm__d: str
