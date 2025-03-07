import enum
from typing import Any, Dict
from koncile_sdk.clients.base import BaseClient


class TaskStatus(enum.Enum):
    """
    Enumeration of possible statuses for a task.

    Attributes:
        IN_PROGRESS (str): Indicates that the task is currently in progress.
        DONE (str): Indicates that the task has been completed successfully.
        FAILED (str): Indicates that the task has failed.
        DUPLICATE (str): Indicates that the duplicate file was uploaded.
    """

    IN_PROGRESS = "IN PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"
    DUPLICATE = "DUPLICATE"


class TasksClient(BaseClient):
    """
    Client for interacting with task-related API endpoints.

    Inherits from BaseClient to utilize common request handling methods.
    Provides methods specific to task operations such as fetching task results.
    """

    def fetch_tasks_results(self, task_id: str) -> Dict[str, Any]:
        """
        Fetch the results of a specific task by its ID.

        Sends a GET request to the `/fetch_tasks_results/` endpoint with the provided task ID
        as a query parameter and returns the parsed JSON response.

        Args:
            task_id (str): The unique identifier of the task whose results are to be fetched.

        Returns:
            Dict[str, Any]: A dictionary containing the task results.

        Raises:
            APIError: If the API request fails or returns an error response.
        """
        # Define the query parameters with the provided task ID
        params = {"task_id": task_id}

        # Send a GET request to the specified endpoint with the query parameters
        response = self._get("/fetch_tasks_results/", params=params)

        # Return the JSON response from the API
        return response
