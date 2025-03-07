import os
import time
from typing import List

from koncile_sdk.client import KoncileAPIClient
from koncile_sdk.clients.tasks import TaskStatus

def monitor_tasks(client: KoncileAPIClient, task_ids: List[str], polling_interval: int = 1):
    """
    Monitor the progress of multiple tasks with proper error handling.
    
    Args:
        client: KoncileAPIClient instance
        task_ids: List of task IDs to monitor
        polling_interval: Time in seconds between polling attempts
    """
    completed_tasks = []
    results = {}
    
    while len(task_ids) != len(completed_tasks):
        for i, task_id in enumerate(task_ids):
            if i not in completed_tasks:
                try:
                    response = client.tasks.fetch_tasks_results(task_id)
                    
                    if response["status"] != TaskStatus.IN_PROGRESS.value:
                        completed_tasks.append(i)
                        results[task_id] = response
                        
                        if response["status"] == TaskStatus.DONE.value:
                            print(f"✓ Task {task_id} completed successfully")
                        elif response["status"] == TaskStatus.FAILED.value:
                            print(f"✗ Task {task_id} failed: {response.get('error', 'Unknown error')}")
                        elif response["status"] == TaskStatus.DUPLICATE.value:
                            print(f"! Task {task_id} detected as duplicate")
                            
                except Exception as e:
                    print(f"Error checking task {task_id}: {str(e)}")
                    completed_tasks.append(i)
                    results[task_id] = {"status": "ERROR", "error": str(e)}
        
        if len(task_ids) != len(completed_tasks):
            time.sleep(polling_interval)
    
    return results

def main():
    # Initialize the client
    client = KoncileAPIClient(
        api_key="your_api_key"
    )
    print("Successfully authenticated")

    # Create a folder and template for file processing
    folder = client.folders.create(
        name="March 2025 Invoices",
        description="Invoices for March 2025"
    )
    print(f"Created folder: {folder['name']} (ID: {folder['id']})")
    
    template = client.templates.create(
        name="Standard Invoice Template",
        description="Template for processing standard invoices",
        folder_id=folder["id"]
    )
    print(f"Created template: {template['name']} (ID: {template['id']})")

    # Get the absolute path to the files directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files_dir = os.path.join(os.path.dirname(current_dir), "files")
    
    # Prepare list of files to process
    files = [
        os.path.join(files_dir, "invoice1.pdf"),
        os.path.join(files_dir, "invoice2.pdf"),
        os.path.join(files_dir, "invoice3.pdf")
    ]

    try:
        # Upload files and get task IDs
        print(f"\nUploading {len(files)} files...")
        upload_response = client.files.upload(
            folder_id=folder["id"],
            template_id=template["id"],
            file_paths=files
        )
        
        task_ids = upload_response['task_ids']
        print(f"Files uploaded successfully. Monitoring {len(task_ids)} tasks...")

        # Monitor tasks with proper error handling
        results = monitor_tasks(client, task_ids)

        # Process results
        print("\nProcessing Results:")
        for task_id, result in results.items():
            if result["status"] == TaskStatus.DONE.value:
                print(f"\nResults for task {task_id}:")
                for field, value in result["results"].items():
                    print(f"- {field}: {value}")

    except Exception as e:
        print(f"Error during file processing: {str(e)}")
    
    finally:
        # Clean up
        print("\nCleaning up...")
        try:
            client.templates.delete(template["id"])
            print(f"Deleted template: {template['name']}")
        except Exception as e:
            print(f"Error deleting template: {str(e)}")
            
        try:
            client.folders.delete(folder["id"])
            print(f"Deleted folder: {folder['name']}")
        except Exception as e:
            print(f"Error deleting folder: {str(e)}")
        
        print("Cleanup complete")

if __name__ == "__main__":
    main()
