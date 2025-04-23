from agno.agent import Agent
from agno.memory.db.sqlite import SqliteMemoryDb
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import  load_dotenv
from tools import tavily_search, save_jobs_to_csv, save_to_csv
from agno.debug import enable_debug_mode
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

You will use the tools effectively, by changing your queries to the search tools.
###You have to store the data in CSV file by calling the tool
###IF you are not able to use a tool error out fast, without executing anything
"""
import time
time.time().is_integer()
memory_db = SqliteMemoryDb(
    table_name="agent_memory",
    db_file=f"agent_memory_{int(time.time())}.db"  # This will create a file named agent_memory.db in your working directory
)

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description=prompt,
    tools=[DuckDuckGoTools(), tavily_search, save_to_csv],
    memory=memory_db,
    enable_agentic_memory=True,
    show_tool_calls=True,
    markdown=True,
    debug_mode=True
)

user_prompt = """
I am into Java, ReactJS, Typescript, SQL, MYSQL, NOSQL, MongoDB and an AWS Certified Developer with 8+ years of experience and currently a Technical Architect.
I am also into Python and AI development including RAG pipeline and Agentic RAG. 

Please search remote jobs for me, strictly who are looking for complete remote. Give me pages of direct linkedin jobs which match my profile.
"""


if __name__ == "__main__":
    agent.print_response(user_prompt, stream=True)
