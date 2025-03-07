import os
from koncile_sdk.client import KoncileAPIClient

def main():
    # Initialize the client
    client = KoncileAPIClient(
        api_key="your_api_key"
    )
    print("Successfully authenticated")

    try:
        # Create a folder for document management
        folder = client.folders.create(
            name="Document Archive",
            description="Archive of processed documents"
        )
        print(f"Created folder: {folder['name']} (ID: {folder['id']})")

        # Ensure downloads directory exists
        downloads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "downloads")
        os.makedirs(downloads_dir, exist_ok=True)

        # List all documents in the folder
        print("\nListing documents in folder:")
        documents = client.documents.list(folder_id=folder["id"])
        for doc in documents:
            print(f"- {doc['name']} (ID: {doc['id']})")

        # Get details of a specific document
        if documents:
            doc_id = documents[0]["id"]
            doc_details = client.documents.get(doc_id)
            print(f"\nDocument details for {doc_id}:")
            print(f"- Name: {doc_details['name']}")
            print(f"- Status: {doc_details['status']}")
            print(f"- Created: {doc_details['created_at']}")

            # Download document
            download_path = os.path.join(downloads_dir, doc_details['name'])
            client.documents.download(doc_id, download_path)
            print(f"Downloaded document to: {download_path}")

            # Delete document
            client.documents.delete(doc_id)
            print(f"Deleted document: {doc_details['name']}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        # Clean up
        print("\nCleaning up...")
        try:
            client.folders.delete(folder["id"])
            print(f"Deleted folder: {folder['name']}")
        except Exception as e:
            print(f"Error deleting folder: {str(e)}")
        print("Cleanup complete")

if __name__ == "__main__":
    main()
