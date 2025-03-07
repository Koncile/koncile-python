from typing import Any, Dict

from koncile_sdk.clients.base import BaseClient
from koncile_sdk.exceptions import RestrictedInstructionType

# Allowed instruction types
TYPES = ["general fields", "line fields"]


def transform_instruction_type(response_type):
    """
    Transform the API response instruction type to a user-friendly format.

    This function maps internal API response types to more understandable
    category names.

    Args:
        response_type (str): The instruction type received from the API response.

    Returns:
        str: A user-friendly instruction type.
    """
    match response_type:
        case "text":
            return "General fields"
        case "line":
            return "Line fields"
        case _:
            return response_type


class InstructionsClient(BaseClient):
    """
    Client for managing instruction-related operations with the API.

    Inherits from `BaseClient` to utilize common request handling methods.
    Provides functionalities such as creating, retrieving, updating, and deleting instructions.
    """

    def create(
        self,
        content: str,
        template_id: int,
        type: str,
    ) -> Dict[str, Any]:
        """
        Create a new instruction within a specified template.

        Sends a POST request to the `/create_instruction/` endpoint with the provided
        instruction details.

        Args:
            content (str): The content of the new instruction.
            template_id (int): The ID of the template to which the instruction belongs.
            type (str): The type of the instruction. Must be either "General fields" or "Line fields".

        Returns:
            Dict[str, Any]: A dictionary containing the details of the created instruction.

        Raises:
            RestrictedInstructionType: If the `instruction_type` is not one of the allowed types.
            APIError: If the API request fails or returns an error response.
        """
        if type.lower() not in TYPES:
            raise RestrictedInstructionType(
                'Instruction type shoud be "General fields" or "Line fields".'
            )
        body = {
            "content": content,
            "template_id": template_id,
            "type": type,
        }
        response = self._post("/create_instruction/", json_data=body)
        response["type"] = transform_instruction_type(response["type"])
        return response

    def get(self, instruction_id: int) -> Dict[str, Any]:
        """
        Retrieve the details of a specific instruction by its ID.

        Sends a GET request to the `/fetch_instruction/` endpoint with the provided
        instruction ID as a query parameter.

        Args:
            instruction_id (int): The unique identifier of the instruction to retrieve.

        Returns:
            Dict[str, Any]: A dictionary containing the details of the retrieved instruction.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        params = {"instruction_id": instruction_id}
        response = self._get("/fetch_instruction/", params)
        response["instruction_type"] = transform_instruction_type(
            response["type"])
        del response["type"]
        return response

    def update(
        self,
        instruction_id: int,
        content: str = None,
        type: str = None,
    ) -> Dict[str, Any]:
        """
        Update the details of an existing instruction.

        Sends a PUT request to the `/update_instruction/` endpoint with the updated
        instruction information.

        Args:
            instruction_id (int): The unique identifier of the instruction to update.
            content (str): The new content for the instruction.
            instruction_type (str): The new type of the instruction. Must be either "General fields" or "Line fields".

        Returns:
            Dict[str, Any]: A dictionary containing the updated details of the instruction.

        Raises:
            RestrictedInstructionType: If the `instruction_type` is not one of the allowed types.
            APIError: If the API request fails or returns an error response.
        """
        if type and type.lower() not in TYPES:
            raise RestrictedInstructionType(
                'Instruction type shoud be "General fields" or "Line fields".'
            )
        params = {
            "instruction_id": instruction_id,
        }
        body = {
            "content": content,
            "type": type,
        }
        response = self._put("/update_instruction/",
                             params=params, json_data=body)
        response["type"] = transform_instruction_type(
            response["type"])
        return response

    def delete(self, instruction_id: int):
        """
        Delete a specific instruction by its ID.

        Sends a DELETE request to the `/delete_instruction/` endpoint with the provided
        instruction ID as a query parameter.

        Args:
            instruction_id (int): The unique identifier of the instruction to delete.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        params = {"instruction_id": instruction_id}
        self._delete("/delete_instruction/", params)
