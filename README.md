# Koncile Python SDK

The official Python SDK for [Koncile](https://koncile.ai), providing a seamless interface to interact with the Koncile API.

## Features

- Authentication and API key management
- File operations (upload, download, manage)
- Task management and status tracking
- Folder organization
- Template handling
- Field configuration
- Instruction management
- Document operations

## Installation

You can install the Koncile SDK using pip:

```bash
pip install koncile
```

For development installation, we recommend using a virtual environment (optional but recommended to avoid dependency conflicts):

```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate

# Install the package
pip install koncile
```

## Quick Start

```python
import time
from typing import List
from koncile_sdk.client import KoncileAPIClient
from koncile_sdk.clients.tasks import TaskStatus

# Initialize the client
client = KoncileAPIClient(
    api_key="your_api_key"
)

# Upload multiple files and get task IDs
files = [
    "./invoices/invoice1.pdf",
    "./invoices/invoice2.pdf"
]

upload_response = client.files.upload(
    folder_id="folder_id",
    template_id="template_id",
    file_paths=files
)

# Get task IDs from the upload response
task_ids: List[str] = upload_response['task_ids']

# Poll for task completion
completed_tasks = []
while len(task_ids) != len(completed_tasks):
    for i, task_id in enumerate(task_ids):
        if i not in completed_tasks:
            response = client.tasks.fetch_tasks_results(task_id)
            
            # Check if task is complete
            if response["status"] != TaskStatus.IN_PROGRESS.value:
                completed_tasks.append(i)
                
                if response["status"] == TaskStatus.DONE.value:
                    print(f"Task {task_id} completed successfully")
                    print("Results:", response["results"])
                elif response["status"] == TaskStatus.FAILED.value:
                    print(f"Task {task_id} failed")
                elif response["status"] == TaskStatus.DUPLICATE.value:
                    print(f"Task {task_id} detected as duplicate")
    
    if len(task_ids) != len(completed_tasks):
        time.sleep(1)  # Wait before next polling iteration
```

## Documentation

For detailed API documentation and guides, visit [docs.koncile.ai](https://docs.koncile.ai).

## Support

For support inquiries, please contact support@koncile.ai.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

© 2025 Koncile. All rights reserved.
