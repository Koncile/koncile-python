from koncile_sdk.clients.base import BaseClient


class DocumentsClient(BaseClient):
    """
    Client for managing document-related operations with the API.

    Inherits from `BaseClient` to utilize common request handling methods.
    Provides functionalities such as deleting documents.
    """

    def delete(self, id: int):
        """
        Delete a specific document by its ID.

        Sends a DELETE request to the `/delete_doc/` endpoint with the provided
        document ID as a query parameter.

        Args:
            id (int): The unique identifier of the document to delete.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        params = {"doc_id": id}
        self._delete("/delete_doc/", params)
