from agno.agent import Agent
from agno.debug import enable_debug_mode
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from uuid import uuid4
from tools import save_to_csv, extract_content, tavily_search, google_search

enable_debug_mode()
import logging

# Configure logging to capture DEBUG-level messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s'
)
logging.getLogger("httpx").setLevel(logging.DEBUG)  # For HTTP request/response logging
logging.getLogger("openai").setLevel(logging.DEBUG)

# Create a logger for this module
logger = logging.getLogger(__name__)
load_dotenv()

prompt = """
You are an expert job researcher and career advisor who specializes in finding jobs that perfectly match a candidate's profile.
You have exceptional skills in:
1. Resume analysis and extracting key qualifications, skills, and experience
2. Formulating effective boolean search queries to find relevant job postings
3. Evaluating job descriptions to determine the best matches for a candidate

You will be given a resume and specific job search preferences. Your task is to:
- Analyze the resume to identify key skills, experience, and qualifications
- Create targeted search queries using boolean operators when appropriate
- Find and evaluate job postings that match the candidate's profile
- Save the most relevant job opportunities
- By default, aim to find 5 high-quality job matches

Use the provided tools effectively, especially the search tools with well-crafted queries.
If you encounter any issues with a tool, report the error immediately without proceeding further.
"""


class SingleJob(BaseModel):
    title: str = Field(description="Title of the job")
    description: str = Field(description="Brief Description of the Job")
    url: str = Field(description="Url where the job was found")


def save_found_jobs(agent: Agent, title: str, description: str, url: str):
    """
        Saves a job to the agent's session state list and returns a confirmation message.

        This function appends a JobState item to the 'jobs_list' maintained in the agent's session state
        and provides feedback about the current state of the jobs list after the addition.

        Args:
            agent (Agent): The agent instance containing the session state.
            title: Title of the job
            description: Description of the Job
            url: Url where the job is found

        Returns:
            str: A message confirming the current state of the jobs list after adding the new item.

        Note:
            The function assumes that agent.session_state["jobs_list"] is already initialized
            as a list before this function is called.
        """
    try:
        logger.info(f"save_found_jobs called with title: {title}, url: {url}")
        logger.debug(f"Current session state before adding job: {agent.session_state}")

        single_job = SingleJob(title=title, description=description, url=url)
        job_data = single_job.model_dump()

        agent.session_state["jobs_list"].append(job_data)
        logger.info(f"Job added successfully. Job title: {title}")
        logger.debug(f"Current session state after adding job: {agent.session_state}")

        return f"Job '{title}' added successfully. The job list now is {agent.session_state['jobs_list']}"
    except Exception as e:
        error_msg = f"Error in save_found_jobs: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg




def call_agent_and_return_state(resume:str, user_prompt: str):
    final_prompt = f"""
    # CANDIDATE RESUME
    ```
    {resume}
    ```

    # JOB SEARCH REQUIREMENTS
    ```
    {user_prompt}
    ```

    Begin by analyzing the resume to extract key skills, experience, and qualifications.
    Then formulate effective search queries based on both the resume and job search requirements.
    Use boolean operators in your search queries when appropriate to find the most relevant results.
    """
    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        session_state={"jobs_list": []},
        delay_between_retries=5,
        session_id=str(uuid4()),
        add_state_in_messages=True,
        reasoning=True,
        description=prompt,
        instructions="""You will have to find jobs matching the user's resume and preferences.
                     IMPORTANT INSTRUCTIONS:

                     STEP 1: ANALYZE THE RESUME
                     - First, carefully analyze and summarize the resume to extract key information:
                       * Technical skills and programming languages
                       * Years of experience
                       * Education level and field
                       * Previous job titles and roles
                       * Industry expertise
                       * Certifications and qualifications
                     - Create a concise summary of the candidate's profile to guide your search

                     STEP 2: FORMULATE SEARCH QUERIES
                     - Based on the resume analysis and user's preferences, create effective search queries
                     - Use Google boolean search operators when appropriate, such as:
                       * Quotes for exact phrases: "java developer"
                       * OR for alternatives: java OR python
                       * Site-specific searches: site:linkedin.com
                       * Exclusions: -internship -junior
                       * Combinations: "senior developer" (java OR python) remote
                     - Prioritize search terms that match the candidate's strongest skills and experience

                     STEP 3: SEARCH FOR RELEVANT JOBS
                     - Use the search tools (tavily_search or google_search) to find relevant job postings
                     - Focus on recent job postings from the last week only
                     - Use extract_content tool to get detailed information from job posting pages
                     - Prioritize company career pages and LinkedIn over general job boards

                     STEP 4: SAVE MATCHING JOBS
                     - For EACH job you find, you MUST use the save_found_jobs tool to save it
                     - The save_found_jobs tool requires three parameters:
                       * title: The job title
                       * description: A brief description of the job
                       * url: The URL where the job was found
                     - You MUST call save_found_jobs at least once before completing your task
                     - Do not end your search until you have found and saved at least one job

                     Example of using the save_found_jobs tool:
                     save_found_jobs(
                         title="Senior Java Developer",
                         description="Remote position for an experienced Java developer with Spring Boot skills",
                         url="https://example.com/jobs/123"
                     )
                     """,
        tools=[save_found_jobs, extract_content, tavily_search, google_search],
        storage=SqliteStorage(table_name="agent_sessions", db_file="tmp/data.db"),
        show_tool_calls=True,
        markdown=True,
        debug_mode=True,
    )
    agent.run(final_prompt)
    return agent.session_state
