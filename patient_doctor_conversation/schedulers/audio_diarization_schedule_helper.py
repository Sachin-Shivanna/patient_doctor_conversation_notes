import os

def getAllFiles():
    directory = 'audioFile'  # Ensure this is the correct path to your directory
    accounts_data = {}  # This will map account IDs to their file dictionaries

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        parts = root.split(os.sep)
        # Ensure we're at the right depth (accountID/patientID)
        if len(parts) >= 3 and files:  # Make sure we have files to process
            accountID = parts[-2]  # Assuming accountID is the second to last part
            print(f"Processing account: {accountID}")  # Debugging print
            # Initialize the dictionary for this account if not already present
            if accountID not in accounts_data:
                accounts_data[accountID] = {}
            # Add file information
            for file in files:
                file_path = os.path.join(root, file)
                print(f"Adding file to account {accountID}: {file_path}")  # Debugging print
                # Add a new key-value pair for each file to the account's dictionary
                accounts_data[accountID][file_path] = file

    # Convert the accounts' dictionaries into a list
    return list(accounts_data.values())