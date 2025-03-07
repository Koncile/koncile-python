import os
import mimetypes

from typing import Any, Dict, List, Optional, Set
from koncile_sdk.clients.base import BaseClient
from koncile_sdk.exceptions import APIError, RestrictedFileType

# Allowed file types
ALLOWED_MIME_TYPES = {
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
    "application/vnd.ms-excel",  # .xls
    "application/vnd.ms-excel.sheet.binary.macroEnabled.12",  # .xlsb
    "application/pdf",  # .pdf
    "image/jpeg",  # .jpeg, .jpg
    "image/png",  # .png
}


class FilesClient(BaseClient):
    """
    Client for handling file-related operations with the API.

    Inherits from `BaseClient` to utilize common request handling methods.
    Provides functionalities such as uploading files and retrieving allowed MIME types.
    """

    def allowed_mime_types(self) -> Set[str]:
        """
        Retrieve the set of allowed MIME types for file uploads.

        Returns:
            Set[str]: A set containing the allowed MIME types.
        """
        return ALLOWED_MIME_TYPES

    def upload(
        self,
        file_paths: List[str],
        user_id: Optional[int] = None,
        folder_id: Optional[int] = None,
        template_id: Optional[int] = None,
        doc_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Upload multiple files to the API.

        This method validates the provided file paths, ensures that each file is of an allowed
        MIME type, and uploads them to the `/upload_file/` endpoint with the specified parameters.

        Args:
            file_paths (List[str]): A list of file system paths to the files to be uploaded.
            user_id (Optional[int], optional): The ID of the user uploading the files. Defaults to None.
            folder_id (Optional[int], optional): The configuration ID associated with the upload. Defaults to None.
            template_id (Optional[int], optional): The class ID associated with the upload. Defaults to None.
            doc_id (Optional[int], optional): The document ID associated with the upload. Defaults to None.

        Returns:
            Dict[str, Any]: A dictionary containing the API's response to the upload request.

        Raises:
            APIError: If neither `user_id` nor `folder_id` is provided, if no files are selected,
                      if a file does not exist, or if a file's MIME type is not allowed.
            RestrictedFileType: If a file's MIME type is not within the allowed MIME types.
        """
        # Ensure that either user_id or folder_id is provided
        if not user_id and not folder_id:
            raise APIError("Please select a user or a configuration.")

        # Ensure that at least one file is provided for upload
        if not file_paths:
            raise APIError("Please select files to upload.")

        files = []

        for file_path in file_paths:
            if not os.path.exists(file_path):
                raise APIError(f"File not found: {file_path}")

            # Extract only the file name
            file_name = os.path.basename(file_path)
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                mime_type = "application/octet-stream"  # Default if unknown

            # Validate file type
            if mime_type not in ALLOWED_MIME_TYPES:
                raise RestrictedFileType(
                    f"File type not allowed: {file_name} ({mime_type})"
                )

            files.append(
                ("files", (file_name, open(file_path, "rb"), mime_type)))

        params = {}
        if doc_id:
            params["doc_id"] = doc_id
        if template_id:
            params["template_id"] = template_id
        if folder_id:
            params["folder_id"] = folder_id
        if user_id:
            params["user_id"] = user_id

        try:
            response = self._post(
                "/upload_file/",
                params=params,
                files=files,
            )
        finally:
            # Ensure all opened file handles are closed to prevent memory leaks
            for _, file_tuple in files:
                file_tuple[1].close()

        return response
