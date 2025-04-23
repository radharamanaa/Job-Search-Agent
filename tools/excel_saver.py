from typing import Optional, List
import csv
from pathlib import Path
from datetime import datetime

from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

class JobData(BaseModel):
    job_title: str
    job_url: str
    country: Optional[str]
    city: Optional[str]
    relevancy_score: float
    recruiter_emails: Optional[str]
    description:str

def save_jobs_to_csv(jobs: List[JobData], output_dir: str = "output") -> str:
    """
    Save a list of job listings to a CSV file with timestamp-based naming.

    Args:
        class JobData(BaseModel):
            job_title: str
            job_url: str
            country: Optional[str]
            city: Optional[str]
            relevancy_score: float
            recruiter_emails: Optional[str]
            description:str
        jobs (List[JobData]): List of JobData objects containing job information
        output_dir (str): Directory path where the CSV file will be saved (default: "output")

    Returns:
        str: Path to the saved CSV file

    """
    if not jobs:
        raise ValueError("Jobs list cannot be empty")

    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"job_listings_{timestamp}.csv"
    file_path = output_path / filename

    # Define CSV headers based on JobData model
    headers = ['job_title', 'job_url', 'country', 'city',
              'relevancy_score', 'recruiter_emails']

    # Write data to CSV
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for job in jobs:
            single_job = job.model_dump()
            writer.writerow(single_job)

    return str(file_path)
