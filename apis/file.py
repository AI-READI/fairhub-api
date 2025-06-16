"""APIs for study files"""

import importlib
import os
import typing

from azure.storage.filedatalake import FileSystemClient
from flask_restx import Namespace, Resource, reqparse

import model

api = Namespace("File", description="File operations", path="/")


class FileException(Exception):
    pass


@api.errorhandler(FileException)
def handle_file_exception(error):
    return {"message": str(error)}, 404


# @api.route("/study/<study_id>/files1")
# class Files(Resource):
#     """Files for a study"""
#
#     parser = reqparse.RequestParser()
#     parser.add_argument("path", type=str, required=False, location="args")
#     @api.doc(description="Return a list of all files for a study")
#     @api.param("path", "The folder path on the file system")
#     @api.response(200, "Success")
#     @api.response(400, "Validation Error")
#     def get(self, study_id):  # pylint: disable=unused-argument
#         """Return a list of all files for a study"""
#         # with the same name as the study id.
#
#         # Determine the appropriate configuration module based on the testing context
#         if os.environ.get("FLASK_ENV") == "testing":
#             config_module_name = "pytest_config"
#         else:
#             config_module_name = "config"
#
#         config_module = importlib.import_module(config_module_name)
#         if os.environ.get("FLASK_ENV") == "testing":
#             # If testing, use the 'TestConfig' class for accessing 'secret'
#             config = config_module.TestConfig
#         else:
#             # If not testing, directly use the 'config' module
#             config = config_module
#         if not config.AZURE_STORAGE_CONNECTION_STRING and not config.CONTAINER:
#             return "azure connection string is missing", 404
#         def get_file_tree():
#             container = config.CONTAINER
#             file_system_client = FileSystemClient.from_connection_string(
#                 config.AZURE_STORAGE_CONNECTION_STRING,
#                 file_system_name=container,
#             )
#             source: str = f"AI-READI/test-files/{study_id}"
#             return recurse_file_tree(file_system_client, source)
#
#         def recurse_file_tree(file_system_client: FileSystemClient, source: str):
#             source_client = file_system_client.get_directory_client(source)
#             if not source_client.exists():
#                 raise FileException("source directory does not exist!")
#             props = source_client.get_directory_properties()
#             updated_on = props['last_modified']
#             size = 0
#             path_name = os.path.basename(source)
#             return model.FolderStructure(
#                 path_name,
#                 size,
#                 updated_on,
#                 True,
#                 [
#                     (
#                         recurse_file_tree(file_system_client, child_path.name)
#                         if child_path.is_directory
#                         else model.FileStructure(
#                             os.path.basename(child_path.name),
#                             child_path.content_length,
#                             child_path.last_modified,
#                             False
#                         )
#                     )
#                     for child_path in file_system_client.get_paths(source, recursive=False)
#                 ],
#             )
#         return get_file_tree().to_dict(), 200


@api.route("/study/<study_id>/files")
class Files(Resource):
    """Files for a study"""

    parser = reqparse.RequestParser()
    parser.add_argument(
        "path",
        type=str,
        required=False,
        location="args",
        default="",
        help="The folder path to list. Defaults to the study root.",
    )

    @api.doc(
        description="Return a flat list of files and folders for a given path within a study."
    )
    @api.param("path", "The folder path on the file system to explore.")
    @api.response(200, "Success")
    @api.response(400, "Validation Error or Invalid Path")
    @api.response(404, "Path not found")
    def get(self, study_id):  # pylint: disable=unused-argument
        """Returns a flat list of files and folders for a given path"""
        study = model.Study.query.get(study_id)
        if not study:
            return "Study not found", 404

        args = self.parser.parse_args()
        relative_path = args.get("path", "")
        relative_path = relative_path.lstrip("/\\")

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

        if not config.AZURE_STORAGE_CONNECTION_STRING and not config.CONTAINER:
            return "azure connection string is missing", 404
        # --- Path Sanitization ---
        base_dir = os.path.normpath(f"AI-READI/test-files/{study_id}")
        full_path = os.path.normpath(os.path.join(base_dir, relative_path))
        if os.path.commonpath([base_dir, full_path]) != base_dir:
            return {"message": "Access denied: Invalid path provided."}, 400
        source_path = full_path.replace("\\", "/")

        # --- Azure Client and Directory Listing ---
        file_system_client = FileSystemClient.from_connection_string(
            config.AZURE_STORAGE_CONNECTION_STRING,
            file_system_name=config.CONTAINER,
        )

        directory_client = file_system_client.get_directory_client(source_path)

        # Check for existence and raise exception as requested
        if not directory_client.exists():
            raise FileException(f"Source directory does not exist: {source_path}")

        # The response is a simple list of items in the directory
        directory_contents = []

        for child_path in file_system_client.get_paths(
            path=source_path, recursive=False
        ):
            item: typing.Union[model.FolderStructure, model.FileStructure]

            if child_path.is_directory:
                item = model.FolderStructure(
                    name=os.path.basename(child_path.name),
                    content_length=0,
                    updated_on=child_path.last_modified,
                    is_directory=True,
                    files=[],
                )
            else:
                item = model.FileStructure(
                    name=os.path.basename(child_path.name),
                    content_length=child_path.content_length,
                    updated_on=child_path.last_modified,
                    is_directory=False,
                )

            directory_contents.append(item.to_dict())

        return directory_contents, 200
