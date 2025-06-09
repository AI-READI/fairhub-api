"""APIs for study files"""

import importlib
import os

from azure.storage.filedatalake import FileSystemClient
import model
from flask_restx import Namespace, Resource, reqparse
from flask import Response

api = Namespace("File", description="File operations", path="/")

class FileException(Exception):
    pass

@api.route("/study/<study_id>/files")
class Files(Resource):
    """Files for a study"""

    parser = reqparse.RequestParser()
    parser.add_argument("path", type=str, required=False, location="args")
    @api.doc(description="Return a list of all files for a study")
    @api.param("path", "The folder path on the file system")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self, study_id):  # pylint: disable=unused-argument
        """Return a list of all files for a study"""
        # todo: anticipating that each study will have a folder in the storage account
        # with the same name as the study id.

        # Determine the appropriate configuration module based on the testing context
        if os.environ.get("FLASK_ENV") == "testing":
            config_module_name = "pytest_config"
        else:
            config_module_name = "config"

        config_module = importlib.import_module(config_module_name)
        if os.environ.get("FLASK_ENV") == "testing":
            # If testing, use the 'TestConfig' class for accessing 'secret'
            config = config_module.TestConfig
        else:
            # If not testing, directly use the 'config' module
            config = config_module

        def get_file_tree():
            container = config.CONTAINER
            file_system_client = FileSystemClient.from_connection_string(
                config.AZURE_STORAGE_CONNECTION_STRING,
                file_system_name=container,
            )
            source: str = "AI-READI/test-files"
            return recurse_file_tree(file_system_client, source)

        def recurse_file_tree(file_system_client: FileSystemClient, source: str):
            source_client = file_system_client.get_directory_client(source)
            if not source_client.exists():
                raise FileException("source directory does not exist!")
            props = source_client.get_directory_properties()
            updated_on = props['last_modified']
            size = 0
            path_name = os.path.basename(source)
            return model.FolderStructure(
                path_name,
                size,
                updated_on,
                True,
                [
                    (
                        recurse_file_tree(file_system_client, child_path.name)
                        if child_path.is_directory
                        else model.FileStructure(
                            os.path.basename(child_path.name),
                            child_path.content_length,
                            child_path.last_modified,
                            False
                        )
                    )
                    for child_path in file_system_client.get_paths(source, recursive=False)
                ],
            )
        get_file_tree()
        return get_file_tree().to_dict(), 200
