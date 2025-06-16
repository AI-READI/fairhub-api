class FileStructure:  # type: ignore
    def __init__(self, name, content_length, updated_on, is_directory):
        self.name = name
        self.size = content_length
        self.updated_on = updated_on
        self.is_directory = is_directory

    def to_dict(self):
        return {
            "name": self.name,
            "content_length": self.size,
            "updated_on": self.updated_on.isoformat() if self.updated_on else None,
            "is_directory": self.is_directory,
        }
