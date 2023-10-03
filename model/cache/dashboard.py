from redis_om import HashModel


class DashboardCache(HashModel):
    name: str
    varname: str
    namespace: str
    endpoint: str
