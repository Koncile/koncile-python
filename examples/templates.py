from koncile_sdk.client import KoncileAPIClient

def main():
    # Initialize the client
    client = KoncileAPIClient(
        api_key="your_api_key"
    )
    print("Successfully authenticated")

    try:
        # Create a folder for templates
        folder = client.folders.create(
            name="Invoice Templates",
            description="Collection of invoice processing templates"
        )
        print(f"Created folder: {folder['name']} (ID: {folder['id']})")

        # Create a new template
        template = client.templates.create(
            name="Standard Invoice Template",
            description="Template for processing standard invoices",
            folder_id=folder["id"]
        )
        print(f"Created template: {template['name']} (ID: {template['id']})")

        # Get template details
        template_details = client.templates.get(template["id"])
        print("\nTemplate details:")
        print(f"- Name: {template_details['name']}")
        print(f"- Description: {template_details['description']}")
        print(f"- ID: {template_details['id']}")

        # List all templates in the folder
        templates = client.templates.list(folder_id=folder["id"])
        print("\nAll templates in folder:")
        for t in templates:
            print(f"- {t['name']} (ID: {t['id']})")

        # Update template
        updated_template = client.templates.update(
            template["id"],
            name="Enhanced Invoice Template",
            description="Template for processing invoices with enhanced field detection"
        )
        print(f"\nUpdated template: {updated_template['name']}")

    except Exception as e:
        print(f"Error: {str(e)}")

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
