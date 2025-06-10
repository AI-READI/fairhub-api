from .file import FileStructure

import typing


class FolderStructure():  # type: ignore
    files: typing.List[typing.Union["FileStructure", "FolderStructure"]]
    def __init__(self, name, content_length, updated_on, is_directory, files):
        self.name = name
        self.content_length = content_length
        self.updated_on = updated_on
        self.is_directory = is_directory
        self.files = files

    def to_dict(self):
        return {
            "name": self.name,
            "content_length": self.content_length,
            "updated_on": self.updated_on.isoformat() if self.updated_on else None,
            "is_directory": self.is_directory,
            "files": [i.to_dict() for i in self.files]
        }