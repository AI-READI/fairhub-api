import model


class DatasetVersions:
    def __init__(
        self,
        lastPublished: model.DatasetVersion,
        lastModified: model.DatasetVersion,
        name: str,
        id: int,
    ):
        self.latestVersion = lastModified.id
        self.publishedVersion = lastPublished.id
        self.lastModified = lastModified.modified
        self.lastPublished = lastPublished.modified
        self.name = name
        self.id = id

    def to_dict(self):
        return {
            "latestVersion": self.latestVersion,
            "publishedVersion": self.publishedVersion,
            "lastModified": self.lastModified,
            "lastPublished": self.lastPublished,
            "name": self.name,
            "id": self.id,
        }

    def from_data(data):
        datasetVersions = DatasetVersions()
        datasetVersions.id = data["id"]
        datasetVersions.latestVersion = data["latestVersion"]
        datasetVersions.lastModified = data["lastModified"]
        datasetVersions.lastPublished = data["lastPublished"]
        datasetVersions.name = data["name"]
        datasetVersions.publishedVersion = data["publishedVersion"]
        return datasetVersions
