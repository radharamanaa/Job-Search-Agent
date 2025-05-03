# Job Search and Matcher Agent 🤖

An intelligent job search assistant that matches your resume with relevant job opportunities using AI. This tool helps streamline your job search process by analyzing your resume and preferences to find the most suitable positions.

## Features ✨

- **Resume Analysis**: Upload or paste your resume and get matched with relevant jobs
- **Custom Search Preferences**: Specify location, seniority level, and remote work preferences
- **Real-time Job Matching**: Instantly search and match jobs based on your profile
- **Interactive Results**: View matched jobs in an easy-to-read format
- **Export Functionality**: Download your job matches as CSV
- **Smart Filtering**: AI-powered relevancy matching between your skills and job requirements

## Prerequisites 📋

Before you begin, ensure you have the following:

- **Python 3.12** or higher
- **uv** (Python package manager)
- **API Keys** for the following services:
  - OpenAI API key (for GPT-4o)
  - Tavily API key (for web search)
  - Google API key and Custom Search Engine ID (for Google search)
  - (Optional) Anthropic API key (if using Claude models)

## Installation 🚀

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/JobSearchAndMatcherAgent.git
cd JobSearchAndMatcherAgent
```

### 2. Create a virtual environment with UV

```bash
# Install UV if you don't have it already
# See https://github.com/astral-sh/uv for installation instructions

# Create and activate virtual environment with UV
uv venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies with UV

```bash
uv sync

```

### 4. Set up environment variables

Create a `.env` file in the root directory with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_google_cse_id
ANTHROPIC_API_KEY=your_anthropic_api_key  # Optional
```

## Getting API Keys 🔑

### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API keys section
4. Create a new secret key

### Tavily API Key

1. Visit [Tavily AI](https://tavily.com/)
2. Sign up for an account
3. Navigate to the API section
4. Generate a new API key

### Google API Key and Custom Search Engine ID

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Custom Search API
4. Create credentials to get your API key
5. Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
6. Create a new search engine
7. Get your Search Engine ID (cx)

## Usage 💻

### Running the Streamlit UI

```bash
streamlit run ui.py
```

This will start the web interface at `http://localhost:8501` where you can:

1. Upload your resume (PDF, DOCX, or TXT format) or paste it directly
2. Enter your job search preferences
3. Click "Search Jobs" to find matching opportunities
4. View and download the results

### Example Job Search Instructions

For best results, be specific in your job search instructions. For example:

```
Please search for remote Senior Java Developer remote positions.
I'm looking for roles that involve Spring Boot and microservices.
I prefer companies that offer visa sponsorship.
I am looking to directly get the company pages on which the job is listed
```

## Project Structure 📁

- `ui.py` - Streamlit user interface
- `main.py` - Core agent implementation
- `resume_parser.py` - Handles resume parsing from different file formats
- `tools/` - Directory containing search and utility tools:
  - `tavilysearchtool.py` - Tavily search integration
  - `googlesearchtool.py` - Google search integration
  - `web_scraper.py` - Web content extraction
  - `excel_saver_plain.py` - CSV export functionality

## Troubleshooting 🔧

### Common Issues

1. **API Key Errors**:

   - Ensure all API keys are correctly set in your `.env` file
   - Check for any spaces or extra characters in your API keys

2. **Resume Parsing Issues**:

   - Try different file formats if one doesn't work
   - Use the manual input option if automatic parsing fails

3. **No Jobs Found**:

   - Make your search instructions more specific
   - Try different keywords or locations

4. **Installation Problems**:
   - Ensure you're using Python 3.12 or higher
   - Try reinstalling dependencies with `uv sync`
   - If UV is not working properly, check the [UV documentation](https://github.com/astral-sh/uv) for troubleshooting

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- [Agno](https://github.com/agno-ai/agno) - Agent framework
- [Streamlit](https://streamlit.io/) - For the web interface
- [LangChain](https://github.com/langchain-ai/langchain) - For search tools
- [Tavily](https://tavily.com/) - For web search capabilities
- [OpenAI](https://openai.com/) - For GPT-4o model
