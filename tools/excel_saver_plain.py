import csv
import os

def save_to_csv(title: str, description: str, url: str, filename: str = "data.csv"):
    """
    Save title, description and url to a CSV file.
    Creates the file if it doesn't exist and appends new rows with every invocation.

    Args:
        title (str): Title of the entry
        description (str): Description text
        url (str): URL of the entry
        filename (str): Name of the CSV file (defaults to 'data.csv')
    :returns
        A string as "success" or "failed to Save"
    """
    # Define the fieldnames for the CSV
    fieldnames = ['title', 'description', 'url']

    # Check if file exists to determine if we need to write headers
    import datetime
    import time
    filename = filename[:filename.rfind(".")]
    filename+= str(datetime.datetime.now())[:10]+f"_{int(time.time())}" +".csv"
    file_exists = os.path.isfile(filename)

    # Open file in append mode ('a+')
    with open(filename, mode='a+', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write headers if file is being created for the first time
        if not file_exists:
            writer.writeheader()

        # Write the new row
        writer.writerow({
            'title': title,
            'description': description,
            'url': url
        })
    return "Success"