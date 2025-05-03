import streamlit as st
from main import call_agent_and_return_state
import pandas as pd
from resume_parser import parse_resume

def search_jobs():
    # This function will be called when the button is clicked
    resume = st.session_state.resume_text
    instructions = st.session_state.instructions

    # Show loading spinner while processing
    with st.spinner('Searching for jobs...'):
        try:
            # Get the state from your agent
            st.write("Calling the job search agent... This may take a few minutes.")
            state = call_agent_and_return_state(resume, instructions)

            # Debug information
            # st.write(f"Agent session state received: {state}")

            # Check if jobs_list exists and has items
            if "jobs_list" not in state or not state["jobs_list"]:
                st.warning("No jobs were saved by the agent. The jobs_list is empty.")
                st.write("This could be because:")
                st.write("1. The agent couldn't find any matching jobs")
                st.write("2. The agent encountered an error when trying to save jobs")
                st.write("3. The agent didn't properly use the save_found_jobs tool")
                return

            # Create dictionary with only required fields
            jobs_data = {
                'title': [],
                'description': [],
                'url': []
            }

            # Populate the dictionary with job data from state
            for job in state["jobs_list"]:
                jobs_data['title'].append(job["title"])
                jobs_data['description'].append(job["description"])
                jobs_data['url'].append(job["url"])

            # Create dataframe
            df = pd.DataFrame(jobs_data)

            # Show total number of jobs found
            st.write(f"Found {len(df)} jobs matching your criteria")

            # Display the dataframe with styling
            st.dataframe(
                df,
                column_config={
                    "title": st.column_config.TextColumn(
                        "Job Title",
                        width="medium",
                    ),
                    "description": st.column_config.TextColumn(
                        "Description",
                        width="large",
                    ),
                    "url": st.column_config.LinkColumn(
                        "Apply Link",
                        width="small",
                    )
                },
                hide_index=True,
                use_container_width=False,
                width=1200
            )

            # Add download button for CSV
            if not df.empty:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download Jobs Data",
                    csv,
                    "jobs_data.csv",
                    "text/csv",
                    key='download-csv'
                )

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()

            st.error(f"An error occurred while searching for jobs: {str(e)}")

            with st.expander("Error Details"):
                st.code(error_details)

            st.write("Possible solutions:")
            st.write("1. Check that all API keys are correctly set in your .env file")
            st.write("2. Make sure your search instructions are clear and specific")
            st.write("3. Try again with a different search query")
            return

        if 'df' in locals() and df.empty:
            st.warning("No jobs found matching your criteria. Try adjusting your search parameters.")

    st.write(f"Done!")

def main():
    # Set page configuration
    st.set_page_config(page_title="Search Jobs", layout="wide")

    # Title and Header
    st.title("Search Jobs")

    if 'button_disabled' not in st.session_state:
        st.session_state.button_disabled = False

    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = ""

    # Create a form-like container
    with st.container():
        # File uploader for resume
        st.subheader("Upload Your Resume")
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

        if uploaded_file is not None:
            # Parse the resume
            resume_text = parse_resume(uploaded_file)
            st.session_state.resume_text = resume_text

            # Show a preview of the parsed text
            with st.expander("Resume Preview"):
                st.text_area("Parsed Content", value=resume_text, height=200, disabled=True)

        # Alternative manual input option
        st.subheader("Or Enter Resume Text Manually")
        manual_resume = st.text_area("Resume Text",
                                    value=st.session_state.resume_text,
                                    placeholder="Please paste your Resume here if not uploading a file",
                                    key="manual_resume",
                                    height=200)

        if manual_resume != st.session_state.resume_text and manual_resume.strip():
            st.session_state.resume_text = manual_resume

        st.text_area("Instructions",
                    placeholder="Please enter in plain words what kinds of jobs you want to search. You can optionally tell the location, seniority and if remote!",
                    key="instructions",
                    height=200)
        st.write('Please be very specific in your job search instructions. Please mention the location, job criteria, experience you are looking for!')

        # Search button
        if st.button("Search Jobs",
                     type="primary",
                     disabled=st.session_state.button_disabled or not st.session_state.resume_text,
                     key="search_button"):
            search_jobs()

if __name__ == "__main__":
    main()