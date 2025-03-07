from koncile_sdk.clients.base import BaseClient
from koncile_sdk.exceptions import ValidationError


class AuthClient(BaseClient):
    """
    Client for handling authentication-related operations with the API.

    Inherits from `BaseClient` to utilize common request handling methods.
    Provides functionalities such as validating the API key.
    """

    def validate_api_key(self) -> bool:
        """
        Validate the current API key against the authentication endpoint.

        This method checks whether both the `api_key` and `base_url` are set.
        If they are, it proceeds to validate the API key by making a request
        to the authentication check endpoint. Returns `True` if the API key
        is valid, otherwise returns `False`.

        Returns:
            bool: `True` if the API key is valid and the validation request succeeds;
                  `False` otherwise.
        """
        if self.api_key and self.base_url:
            return self._validate_api_key_request()
        return False

    def _validate_api_key_request(self) -> bool:
        """
        Perform an API request to verify the validity of the API key.

        Sends a POST request to the `/check_api_key/` endpoint to check if the
        provided API key is valid. Assumes that the API responds with a JSON
        object containing a `success` key indicating the validation result.

        Returns:
            bool: `True` if the API key is valid (`"success": True` in response);
                  `False` otherwise.
        """
        try:
            response = self._post("/check_api_key/")
            return response.get(
                "success", False
            )  # Assuming API responds with {"valid": true/false}
        except ValidationError:
            return False
