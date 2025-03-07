from typing import Any, Dict, Optional

from koncile_sdk.clients.base import BaseClient


class FoldersClient(BaseClient):
    """
    Client for managing folder-related operations with the API.

    Inherits from `BaseClient` to utilize common request handling methods.
    Provides functionalities such as creating, retrieving, updating, and deleting folders.
    """

    def create(self, name: str, desc: str = None) -> Dict[str, Any]:
        """
        Create a new folder with the specified name and description.

        Sends a POST request to the `/create_folder/` endpoint with the provided
        folder details.

        Args:
            name (str): The name of the new folder.
            desc (str): A description of the new folder.

        Returns:
            Dict[str, Any]: A dictionary containing the details of the created folder.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        body = {
            "name": name,
            "desc": desc,
        }
        response = self._post("/create_folder/", json_data=body)
        return response

    def get(self, folder_id: int) -> Dict[str, Any]:
        """
        Retrieve the details of a specific folder by its ID.

        Sends a GET request to the `/fetch_folder/` endpoint with the provided
        folder ID as a query parameter.

        Args:
            id (int): The unique identifier of the folder to retrieve.

        Returns:
            Dict[str, Any]: A dictionary containing the details of the retrieved folder.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        params = {"folder_id": folder_id}
        response = self._get("/fetch_folder/", params)
        return response

    def update(self, folder_id: int, name: str = None, desc: str = None) -> Dict[str, Any]:
        """
        Update the details of an existing folder.

        Sends a PUT request to the `/update_folder/` endpoint with the updated
        folder information.

        Args:
            id (int): The unique identifier of the folder to update.
            name (str): The new name for the folder.
            desc (str): The new description for the folder.

        Returns:
            Dict[str, Any]: A dictionary containing the updated details of the folder.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        params = {"folder_id": folder_id}
        body = {
            "name": name,
            "desc": desc,
        }
        print(body)
        print(params)
        response = self._put("/update_folder/", params, body)
        return response

    def delete(self, folder_id: int, override: Optional[bool] = False):
        """
        Delete a specific folder by its ID.

        Sends a DELETE request to the `/delete_folder/` endpoint with the provided
        folder ID as a query parameter. The `override` parameter determines whether
        to force the deletion of the folder even if it contains sub-items.

        **Caution**: Setting `override=True` will permanently delete the folder and all
        its contents. Ensure that you have backed up any important data before proceeding.

        Args:
            id (int): The unique identifier of the folder to delete.
            override (Optional[bool], optional): If set to `True`, forces the deletion of the folder
                even if it contains sub-items. Defaults to `False`.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        params = {"folder_id": folder_id, "override": override}
        self._delete("/delete_folder/", params)
