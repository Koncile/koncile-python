from koncile_sdk.clients.auth import AuthClient
from koncile_sdk.clients.files import FilesClient
from koncile_sdk.clients.tasks import TasksClient
from koncile_sdk.clients.folders import FoldersClient
from koncile_sdk.clients.templates import TemplatesClient
from koncile_sdk.clients.fields import FieldsClient
from koncile_sdk.clients.instructions import InstructionsClient
from koncile_sdk.clients.documents import DocumentsClient
from koncile_sdk.exceptions import ValidationError
from koncile_sdk.versions import API_URL_VERSIONS


class KoncileAPIClient:
    """
    The main client for interacting with the Koncile API.

    This client serves as an aggregator for various sub-clients, providing a unified interface
    to access different API functionalities such as authentication, file management, task
    operations, folder management, template handling, field configuration, instruction
    management, and document operations.

    Attributes:
        auth (AuthClient): Client for authentication-related operations.
        files (FilesClient): Client for file-related operations.
        tasks (TasksClient): Client for task-related operations.
        folders (FoldersClient): Client for folder-related operations.
        templates (TemplatesClient): Client for template-related operations.
        fields (FieldsClient): Client for field-related operations.
        instructions (InstructionsClient): Client for instruction-related operations.
        documents (DocumentsClient): Client for document-related operations.
    """

    def __init__(self, api_key: str, base_url: str = API_URL_VERSIONS["v1"]):
        """
        Initialize the KoncileAPIClient with the provided API key and base URL.

        This constructor initializes all sub-clients, passing the `base_url` and `api_key` to each.
        It also validates the provided API key to ensure that it is valid and authorized for use.

        Args:
            api_key (str): The API key used for authenticating requests.
            base_url (str, optional): The base URL for the API endpoints. Defaults to `API_URL_VERSIONS['v1']`.

        Raises:
            ValidationError: If the API key validation fails.
        """
        self.auth = AuthClient(base_url, api_key)
        self.files = FilesClient(base_url, api_key)
        self.tasks = TasksClient(base_url, api_key)
        self.folders = FoldersClient(base_url, api_key)
        self.templates = TemplatesClient(base_url, api_key)
        self.fields = FieldsClient(base_url, api_key)
        self.instructions = InstructionsClient(base_url, api_key)
        self.documents = DocumentsClient(base_url, api_key)

        if not self.auth.validate_api_key():
            raise ValidationError("Invalid API key or Base url provided")

    def update_api_key(self, api_key: str):
        """
        Update the API key for all sub-clients.

        This method allows the user to update the API key after the client has been initialized.
        It propagates the new API key to all sub-clients to ensure consistent authentication.

        Args:
            api_key (str): The new API key to be used for authenticating requests.

        Raises:
            ValidationError: If updating the API key fails for any sub-client.
        """
        self.auth.update_api_key(api_key)
        self.files.update_api_key(api_key)
        self.tasks.update_api_key(api_key)
        self.folders.update_api_key(api_key)
        self.templates.update_api_key(api_key)
        self.fields.update_api_key(api_key)
        self.instructions.update_api_key(api_key)
        self.documents.update_api_key(api_key)

        if not self.auth.validate_api_key():
            raise ValidationError("Invalid API key provided after update.")

    def update_base_url(self, base_url: str):
        """
        Update the base URL for all sub-clients.

        This method allows the user to change the base URL after the client has been initialized.
        It propagates the new base URL to all sub-clients to ensure that subsequent requests
        are directed to the correct API endpoints.

        Args:
            base_url (str): The new base URL for the API endpoints.

        Raises:
            ValidationError: If updating the base URL fails for any sub-client.
        """
        self.auth.update_base_url(base_url)
        self.files.update_base_url(base_url)
        self.tasks.update_base_url(base_url)
        self.folders.update_base_url(base_url)
        self.templates.update_base_url(base_url)
        self.fields.update_base_url(base_url)
        self.instructions.update_base_url(base_url)
        self.documents.update_base_url(base_url)

        if not self.auth.validate_api_key():
            raise ValidationError(
                "API key validation failed after updating base URL.")
