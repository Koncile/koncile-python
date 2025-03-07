import enum
from typing import Any, Dict, Optional

from koncile_sdk.clients.base import BaseClient
from koncile_sdk.exceptions import RestrictedFieldType

# Allowed fields types
TYPES = ["general fields", "line fields"]


class FieldFormat(enum.Enum):
    """
    Enumeration of possible field formats.

    Attributes:
        text (str): Represents a text format.
        number (str): Represents a numerical format.
        date (str): Represents a date format.
        currency (str): Represents a currency format.
        price (str): Represents a price format.
        boolean (str): Represents a boolean format.
        empty (str): Represents an empty format.
        multiple_choice (str): Represents a multiple-choice format.
        unit (str): Represents a unit format.
    """

    text = "text"
    number = "number"
    date = "date"
    currency = "currency"
    price = "price"
    boolean = "boolean"
    empty = "empty"
    multiple_choice = "multiple_choice"
    unit = "unit"


def transform_field_type(response_type):
    """
    Transform the API response field type to a user-friendly format.

    This function maps internal API response types to more understandable
    category names.

    Args:
        response_type (str): The field type received from the API response.

    Returns:
        str: A user-friendly field type.
    """
    match response_type:
        case "text":
            return "General fields"
        case "line":
            return "Line fields"
        case _:
            return response_type


class FieldsClient(BaseClient):
    """
    Client for managing field-related operations with the API.

    Inherits from `BaseClient` to utilize common request handling methods.
    Provides functionalities such as creating, retrieving, updating, and deleting fields.
    """

    def create(
        self,
        name: str,
        template_id: int,
        type: str,
        desc: Optional[str] = None,
        format: Optional[str] = FieldFormat.text.value,
        position: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Create a new field within a specified template.

        Sends a POST request to the `/create_field/` endpoint with the provided
        field details.

        Args:
            name (str): The name of the new field.
            template_id (int): The ID of the template to which the field belongs.
            field_type (str): The type of the field. Must be either "General fields" or "Line fields".
            desc (Optional[str], optional): A description of the field. Defaults to None.
            format (Optional[str], optional): The format of the field. Defaults to `FieldFormat.text.value`.
            position (Optional[int], optional): The position of the field within the template. Defaults to None.

        Returns:
            Dict[str, Any]: A dictionary containing the details of the created field.

        Raises:
            RestrictedFieldType: If the `field_type` is not one of the allowed types.
            APIError: If the API request fails or returns an error response.
        """
        if type.lower() not in TYPES:
            raise RestrictedFieldType(
                'Field type shoud be "General fields" or "Line fields".'
            )
        body = {
            "name": name,
            "template_id": template_id,
            "type": type,
            "desc": desc,
            "format": format,
            "position": position
        }
        response = self._post("/create_field/", json_data=body)
        response["type"] = transform_field_type(response["type"])
        return response

    def get(self, field_id: int) -> Dict[str, Any]:
        """
        Retrieve the details of a specific field by its ID.

        Sends a GET request to the `/fetch_field/` endpoint with the provided
        field ID as a query field.

        Args:
            field_id (int): The unique identifier of the field to retrieve.

        Returns:
            Dict[str, Any]: A dictionary containing the details of the retrieved field.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        params = {"field_id": field_id}
        response = self._get("/fetch_field/", params)
        response["type"] = transform_field_type(response["type"])
        return response

    def update(
        self,
        field_id: int,
        name: Optional[str] = None,
        type: Optional[str] = None,
        desc: Optional[str] = None,
        position: Optional[int] = None,
        format: Optional[str] = FieldFormat.text.value,
    ) -> Dict[str, Any]:
        """
        Update the details of an existing field.

        Sends a PUT request to the `/update_field/` endpoint with the updated
        field information.

        Args:
            field_id (int): The unique identifier of the field to update.
            name (str): The new name for the field.
            field_type (str): The new type of the field. Must be either "General fields" or "Line fields".
            description (Optional[str], optional): The new description for the field. Defaults to None.
            format (Optional[str], optional): The new format of the field. Defaults to `FieldFormat.text.value`.

        Returns:
            Dict[str, Any]: A dictionary containing the updated details of the field.

        Raises:
            RestrictedFieldType: If the `field_type` is not one of the allowed types.
            APIError: If the API request fails or returns an error response.
        """
        if type and type.lower() not in TYPES:
            raise RestrictedFieldType(
                'Field type shoud be "General fields" or "Line fields".'
            )
        params = {
            "field_id": field_id,
        }
        body = {
            "name": name,
            "type": type,
            "desc" : desc,
            "format": format,
            "position": position
        }
        response = self._put("/update_field/",
                             params=params, json_data=body)
        response["type"] = transform_field_type(response["type"])
        return response

    def delete(self, field_id: int):
        """
        Delete a specific field by its ID.

        Sends a DELETE request to the `/delete_field/` endpoint with the provided
        field ID as a query field.

        Args:
            field_id (int): The unique identifier of the field to delete.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        params = {"field_id": field_id}
        self._delete("/delete_field/", params)
