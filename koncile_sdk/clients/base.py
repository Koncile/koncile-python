import json
import requests
import warnings
import re

from typing import List, Optional, Dict, Any, Tuple

from koncile_sdk.exceptions import (
    APIError,
    FolderNotFound,
    FreeTierLimitReached,
    AuthenticationError,
    InstructionNotFound,
    ObjectNotFound,
    FieldNotFound,
    TaskNotFound,
    TemplateNotFound,
    ValidationError,
    UploadLimitReached,
)


# Dictionary of words to replace (case-insensitive)
SDK_REPLACEMENT = {
    "config": "folder",
    "class": "template",
    "parameter": "field",
}

# Create a regex pattern that matches all words in the dictionary (case-insensitive)
pattern = re.compile(
    r"\b(" + "|".join(map(re.escape, SDK_REPLACEMENT.keys())) + r")\b",
    re.IGNORECASE,
)


def preserve_case(match):
    """
    Preserve the case of the matched word based on the replacement.

    This function ensures that the replacement word maintains the case format
    of the matched text. It handles uppercase, capitalized, lowercase, and mixed cases.

    Args:
        match (re.Match): The regex match object containing the matched text.

    Returns:
        str: The replacement word with preserved case.
    """
    matched_text = match.group(0)
    replacement = SDK_REPLACEMENT[
        matched_text.lower()
    ]  # Get replacement word from dict (lowercased key)

    if matched_text.isupper():
        return replacement.upper()
    elif matched_text[0].isupper():
        return replacement.capitalize()
    elif matched_text.islower():
        return replacement.lower()
    else:
        # Handle mixed case (e.g., "ExAmPle" → "DeMo")
        return "".join(
            rep.upper() if orig.isupper() else rep.lower()
            for orig, rep in zip(matched_text, replacement)
        )


class BaseClient:
    """
    BaseClient provides a universal handler for making API requests.

    It supports various HTTP methods, handles authentication, and manages
    request sessions with appropriate headers.

    Attributes:
        base_url (str): The base URL for the API.
        api_key (str): The API key for authentication.
        session (requests.Session): The session object for making HTTP requests.
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the BaseClient with a base URL and API key.

        Sets up the HTTP session with authorization headers if an API key is provided.
        Issues warnings if the base URL or API key are missing.

        Args:
            base_url (str): The base URL for the API.
            api_key (str): The API key for authentication.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()

        if not base_url:
            warnings.warn(
                "No base api url provided. You will not be able to process requests."
            )

        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        else:
            warnings.warn(
                "No API key provided. You will not be able to process requests."
            )

    def update_api_key(self, api_key: str):
        """
        Update the API key used for authentication.

        This method updates the API key and refreshes the authorization header
        in the session.

        Args:
            api_key (str): The new API key.
        """
        self.api_key = api_key
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        else:
            self.session.headers.pop("Authorization", None)

    def update_base_url(self, base_url: str):
        """
        Update the base URL for the API.

        Args:
            base_url (str): The new base URL.
        """
        self.base_url = base_url

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        files: Optional[List[Tuple[str, Tuple[str, Any, str]]]] = None,
    ) -> Dict[str, Any]:
        """
        Universal request handler supporting various HTTP methods and data types:
        - JSON requests
        - File uploads (multipart/form-data)
        - Query parameters

        This method constructs and sends an HTTP request based on the provided
        parameters, handles the response, and returns the parsed JSON data.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE).
            endpoint (str): API endpoint.
            params (Optional[Dict[str, Any]]): URL query parameters (e.g., {"user_id": 1}).
            json_data (Optional[Dict[str, Any]]): JSON body for API requests.
            files (Optional[List[Tuple[str, Tuple[str, Any, str]]]]): List of tuples for file uploads.

        Returns:
            Dict[str, Any]: Parsed JSON response from the API.

        Raises:
            APIError: If the API response contains an error.

        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # Headers
        headers = {
            "Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

        # Use JSON for normal requests, but exclude it when uploading files
        if files:
            data = None  # multipart/form-data does not use json
            # headers["Content-Type"] = "multipart/form-data"
        else:
            data = json_data
            headers["Content-Type"] = "application/json"

        response = self.session.request(
            method, url, params=params, json=data, files=files, headers=headers
        )
        self._handle_response_status(response)  # Extracted status handling

        return response.json()

    def _handle_response_status(self, response: requests.Response):
        """
        Handle API response errors and raise appropriate exceptions.

        This method checks the HTTP status code of the response and raises
        custom exceptions based on the error type.

        Args:
            response (requests.Response): The HTTP response object.

        Raises:
            AuthenticationError: If the response status is 401 (Unauthorized).
            ValidationError: If the response status is 403 (Forbidden).
            FreeTierLimitReached: If the response status is 402 (Payment Required).
            FolderNotFound: If a folder-related error occurs.
            TemplateNotFound: If a template-related error occurs.
            FieldNotFound: If a field-related error occurs.
            InstructionNotFound: If an instruction-related error occurs.
            TaskNotFound: If a task-related error occurs.
            ObjectNotFound: If an object-related error occurs.
            UploadLimitReached: If the upload limit is reached.
            APIError: For all other API errors.
        """
        status_code = response.status_code

        # Handling errors that don't need details from response
        if status_code == 401:
            raise AuthenticationError("Unauthorized")

        if status_code == 403:
            raise ValidationError("Could not validate credentials")

        if status_code == 402:
            raise FreeTierLimitReached(
                "You do not have enough credits to proceed the request. Upgrade your account."
            )

        if status_code >= 400:
            # Handling errors that need details from response
            try:
                error_data = response.json()
                detail = error_data.get("detail", "Unknown error")

                # Perform the replacement
                if isinstance(detail, list):
                    # If it's a list of strings, join them
                    detail = " | ".join(str(item) for item in detail)
                else:
                    # For anything else, just convert to string
                    detail = str(detail)
                # Handle 404 Not Found errors with specific messages
                if status_code == 404:
                    detail_lower = detail.lower()
                    if "folder not found" in detail_lower:
                        raise FolderNotFound("Folder not found")
                    if "template not found" in detail_lower:
                        raise TemplateNotFound("Template not found")
                    if "field not found" in detail_lower:
                        raise FieldNotFound("Field not found")
                    if "instruction not found" in detail_lower:
                        raise InstructionNotFound("Instruction not found")
                    if "task not found" in detail_lower:
                        raise TaskNotFound("Task not found")
                    raise ObjectNotFound(f'Object not found: "{detail}"')

                # Handle specific error messages
                if detail == "Maximum number of page upload reached":
                    raise UploadLimitReached(
                        "You’ve reached your upload pages limit. Please upgrade the subscription or reach out to our team to upload more pages"
                    )
            except json.JSONDecodeError:
                # Fallback to raw text if JSON decoding fails
                detail = response.text

            # Raise a general APIError with the status code and detail
            raise APIError(f"API Error {status_code}: {detail}", status_code)

    def _get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform a universal GET request.

        Supports query parameters.

        Args:
            endpoint (str): API endpoint.
            params (Optional[Dict[str, Any]]): URL query parameters.

        Returns:
            Dict[str, Any]: Parsed JSON response.
        """
        return self._request(method="GET", endpoint=endpoint, params=params)

    def _post(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        files: Optional[List[Tuple[str, Tuple[str, Any, str]]]] = None,
    ) -> Dict[str, Any]:
        """
        Perform a universal POST request.

        Supports query parameters, JSON data, and file uploads.

        Args:
            endpoint (str): API endpoint.
            params (Optional[Dict[str, Any]]): URL query parameters.
            json_data (Optional[Dict[str, Any]]): JSON body for the request.
            files (Optional[List[Tuple[str, Tuple[str, Any, str]]]]): Files to upload.

        Returns:
            Dict[str, Any]: Parsed JSON response.
        """
        return self._request(
            method="POST",
            endpoint=endpoint,
            params=params,
            json_data=json_data,
            files=files,
        )

    def _put(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Perform a universal PUT request.

        Supports query parameters and JSON data.

        Args:
            endpoint (str): API endpoint.
            params (Optional[Dict[str, Any]]): URL query parameters.
            json_data (Optional[Dict[str, Any]]): JSON body for the request.

        Returns:
            Dict[str, Any]: Parsed JSON response.
        """
        return self._request(
            method="PUT", endpoint=endpoint, params=params, json_data=json_data
        )

    def _delete(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform a universal DELETE request.

        Supports query parameters.

        Args:
            endpoint (str): API endpoint.
            params (Optional[Dict[str, Any]]): URL query parameters.

        Returns:
            Dict[str, Any]: Parsed JSON response.
        """
        return self._request(method="DELETE", endpoint=endpoint, params=params)
