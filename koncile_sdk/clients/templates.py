import enum
from typing import Any, Dict, Optional

from koncile_sdk.clients.base import BaseClient


class TemplateType(enum.Enum):
    """
    Enumeration of possible template types.
    """

    regular = "regular"
    invoice = "invoice"
    price_grid = "grid"


class TemplatesClient(BaseClient):
    """
    Client for managing template-related operations with the API.

    Inherits from `BaseClient` to utilize common request handling methods.
    Provides functionalities such as creating, retrieving, updating, and deleting templates.
    """

    def create(
        self,
        name: str,
        folder_id: int,
        desc: str = None,
        template_id: Optional[int] = None,
        type: TemplateType = TemplateType.regular,
    ) -> Dict[str, Any]:
        """
        Create a new template in the specified folder.

        Sends a POST request to the `/create_template/` endpoint with the provided
        template details. Optionally associates the new template with an existing
        template ID.

        Args:
            name (str): The name of the new template.
            desc (str): A description of the new template.
            folder_id (int): The ID of the folder where the template will be stored.
            template_id (Optional[int], optional): The ID of an existing template to associate with. Defaults to None.
            template_type (TemplateType, optional): The type of the template. Defaults to `TemplateType.regular`.

        Returns:
            Dict[str, Any]: A dictionary containing the details of the created template with updated keys.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        params = {}
        if template_id:
            params["template_id"] = template_id
        body = {
            "name": name,
            "desc": desc,
            "folder_id": folder_id,
            "type": type,
        }
        response = self._post("/create_template/", json_data=body)
        return response

    def get(self, template_id: int) -> Dict[str, Any]:
        """
        Retrieve the details of a specific template by its ID.

        Sends a GET request to the `/fetch_template/` endpoint with the provided
        template ID as a query parameter.

        Args:
            id (int): The unique identifier of the template to retrieve.

        Returns:
            Dict[str, Any]: A dictionary containing the details of the retrieved template with updated keys.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        params = {"template_id": template_id}
        response = self._get("/fetch_template/", params)
        return response

    def update(
        self,
        template_id: int,
        name: str = None,
        desc: str = None,
        type: TemplateType = None,
    ) -> Dict[str, Any]:
        """
        Update the details of an existing template.

        Sends a PUT request to the `/update_template/` endpoint with the updated
        template information.

        Args:
            id (int): The unique identifier of the template to update.
            name (str): The new name for the template.
            desc (str): The new description for the template.
            template_type (TemplateType, optional): The new type of the template. Defaults to `TemplateType.regular`.

        Returns:
            Dict[str, Any]: A dictionary containing the updated details of the template with updated keys.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        params = {"template_id": template_id}
        body = {
            "name": name,
            "desc": desc,
            "type": type
        }
        response = self._put("/update_template/", params, body)
        return response

    def delete(self, template_id: int):
        """
        Delete a specific template by its ID.

        Sends a DELETE request to the `/delete_template/` endpoint with the provided
        template ID as a query parameter.

        Args:
            id (int): The unique identifier of the template to delete.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        params = {"template_id": template_id}
        self._delete("/delete_template/", params)
