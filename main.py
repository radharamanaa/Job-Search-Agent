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
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("httpx").setLevel(logging.DEBUG)  # For HTTP request/response logging
logging.getLogger("openai").setLevel(logging.DEBUG)
load_dotenv()

prompt = """
You are an enthusiastic job researcher who loves to find jobs which exactly match profile of the user.
You will be given a resume and you have to find matching jobs for him across the whole world depending on his question.
By default you will search for 5 jobs.

You will use the tools effectively, by asking queries to the search tools.
###IF you are not able to use a tool error out fast, without executing anything
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
        print(f"save_found_jobs called with title: {title}, url: {url}")
        print(f"Current session state before adding job: {agent.session_state}")

        single_job = SingleJob(title=title, description=description, url=url)
        job_data = single_job.model_dump()

        agent.session_state["jobs_list"].append(job_data)
        print(f"Job added successfully. Current session state: {agent.session_state}")

        return f"Job '{title}' added successfully. The job list now is {agent.session_state['jobs_list']}"
    except Exception as e:
        error_msg = f"Error in save_found_jobs: {str(e)}"
        print(error_msg)
        return error_msg




def call_agent_and_return_state(resume:str, user_prompt: str):
    final_prompt = f"""
    Please find the resume below
    {resume}
    PLease find the question of the user below
    {user_prompt}
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
                     1. Use the search tools (tavily_search or google_search) to find relevant job postings.
                     2. Focus on recent job postings from the last week only.
                     3. For EACH job you find, you MUST use the save_found_jobs tool to save it.
                     4. The save_found_jobs tool requires three parameters:
                        - title: The job title
                        - description: A brief description of the job
                        - url: The URL where the job was found
                     5. You MUST call save_found_jobs at least once before completing your task.
                     6. Do not end your search until you have found and saved at least one job.

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

resume = """
I am into Java, ReactJS, Typescript, SQL, MYSQL, NOSQL, MongoDB and an AWS Certified Developer with 8+ years of experience and currently a Technical Architect.
I am also into Python and AI development including RAG pipeline and Agentic RAG. """

user_prompt = """

Please search remote jobs for me, strictly who are looking for complete remote. Give me pages where i can apply for jobs directly.
If possible give me pages of the company itself.

Please scrape the webpages as needed and give me the urls which i can directly click apply or contact the recruiter directly.

I am searching for jobs in the dach region in Europe, if possible find companies which sponsor the visa.
Give direct company pages where i can apply. Or linkedin i dont want any other site.

Please find only 1 job for me. Find jobs which are very close to my experience and seniority. I am ok with Senior Team lead also"""
# state = call_agent_and_return_state(resume, user_prompt=user_prompt)
# print(state)
