from koncile_sdk.client import KoncileAPIClient

def main():
    # Initialize the client
    client = KoncileAPIClient(
        api_key="your_api_key"
    )
    print("Successfully authenticated")

    try:
        # Create a new folder
        folder = client.folders.create(
            name="Test Folder API",
            description="Test folder for API"
        )
        print(f"Created folder: {folder['name']} (ID: {folder['id']})")

        # Get folder details
        folder_details = client.folders.get(folder["id"])
        print(f"\nFolder details: {folder_details}")
        print(f"- Name: {folder_details['name']}")
        print(f"- Description: {folder_details['description']}")
        print(f"- ID: {folder_details['id']}")

        # List all folders
        folders = client.folders.list()
        print("\nAll folders:")
        for f in folders:
            print(f"- {f['name']} (ID: {f['id']})")

        # Update folder
        updated_folder = client.folders.update(
            folder["id"],
            name="Test Folder API Updated",
            description="Test folder for API Updated"
        )
        print(f"\nUpdated folder: {updated_folder['name']} (ID: {updated_folder['id']})")

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
