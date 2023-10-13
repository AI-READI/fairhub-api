from .version import Version


class DatasetVersions:
    def __init__(
        self,
        last_published: Version,
        last_modified: Version,
        id: str,  # pylint: disable = redefined-builtin
    ):
        self.latest_version = last_modified.id
        self.published_version = last_published.id
        self.last_modified = last_modified.modified
        self.last_published = last_published.modified
        self.id = id

    def to_dict(self):
        return {
            "latest_version": self.latest_version,
            "published_version": self.published_version,
            "last_modified": self.last_modified,
            "last_published": self.last_published,
            "id": self.id,
        }

    @staticmethod
    def from_data(data: dict):
        dataset_versions = DatasetVersions(
            id=data["id"],
            last_published=data["last_published"],
            last_modified=data["last_modified"],
        )
        dataset_versions.latest_version = data["latest_version"]
        dataset_versions.published_version = data["published_version"]
        return dataset_versions
