from koncile_sdk.client import KoncileAPIClient
from koncile_sdk.clients.fields import FieldFormat

def main():
    # Initialize the client
    client = KoncileAPIClient(
        api_key="your_api_key"
    )
    print("Successfully authenticated")

    try:
        # Create a folder and template
        folder = client.folders.create(
            name="Invoice Processing",
            description="Invoice processing configuration"
        )
        print(f"Created folder: {folder['name']} (ID: {folder['id']})")
        
        template = client.templates.create(
            name="Standard Invoice",
            description="Template for standard invoices",
            folder_id=folder["id"]
        )
        print(f"Created template: {template['name']} (ID: {template['id']})")

        # Create fields with different formats
        fields = []
        
        # Text field for invoice number
        invoice_number = client.fields.create(
            name="Invoice Number",
            description="Unique invoice identifier",
            template_id=template["id"],
            field_type="General fields",
            format=FieldFormat.text.value
        )
        fields.append(invoice_number)
        print(f"Created field: {invoice_number['name']}")

        # Date field for invoice date
        invoice_date = client.fields.create(
            name="Invoice Date",
            description="Date of invoice issuance",
            template_id=template["id"],
            field_type="General fields",
            format=FieldFormat.date.value
        )
        fields.append(invoice_date)
        print(f"Created field: {invoice_date['name']}")

        # Number field for total amount
        total_amount = client.fields.create(
            name="Total Amount",
            description="Total invoice amount",
            template_id=template["id"],
            field_type="Financial Details",
            format=FieldFormat.number.value
        )
        fields.append(total_amount)
        print(f"Created field: {total_amount['name']}")

        # Create instructions for field extraction
        instructions = []
        
        # Instruction for billing lines
        line_instruction = client.instructions.create(
            content="Ignore billing lines with a negative amount",
            template_id=template["id"],
            instruction_type="Line fields"
        )
        instructions.append(line_instruction)
        print(f"Created instruction for: Invoice Number")

        # List all fields in template
        print("\nAll fields in template:")
        template_fields = client.fields.list(template_id=template["id"])
        for field in template_fields:
            print(f"- {field['name']} ({field['field_type']})")

        # List all instructions in template
        print("\nAll instructions in template:")
        template_instructions = client.instructions.list(template_id=template["id"])
        for instruction in template_instructions:
            print(f"- {instruction['content']} ({instruction['instruction_type']})")

        # Update a field
        updated_field = client.fields.update(
            total_amount["id"],
            name="Total Amount (USD)",
            field_type="Financial Details",
            description="Total invoice amount in USD"
        )
        print(f"\nUpdated field: {updated_field['name']}")

        # Update an instruction
        updated_instruction = client.instructions.update(
            line_instruction["id"],
            content="Ignore billing lines with a negative amount and with a date before 2025-01-01",
            instruction_type="Line fields"
        )
        print(f"\nUpdated instruction: {updated_instruction['content']}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        # Clean up
        print("\nCleaning up...")
        try:
            for field in fields:
                client.fields.delete(field["id"])
            print("Deleted all fields")
        except Exception as e:
            print(f"Error deleting fields: {str(e)}")

        try:
            for instruction in instructions:
                client.instructions.delete(instruction["id"])
            print("Deleted all instructions")
        except Exception as e:
            print(f"Error deleting instructions: {str(e)}")

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
