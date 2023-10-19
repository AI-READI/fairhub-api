from redis_om import JsonModel

class ParticipantCacheModel(JsonModel):
    studyid: str
    dm__i: str
    dm__d: str
