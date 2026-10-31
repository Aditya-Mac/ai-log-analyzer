# AI-Powered Log Analyzer

A Flask-based web application that analyzes application and server logs, identifies errors and warnings, and uses the Gemini API to generate root-cause analysis and troubleshooting recommendations.

## Features

- Upload `.log` or `.txt` files
- Count INFO, WARNING, and ERROR messages
- Extract warning and error details
- Generate rule-based recommendations
- Generate AI-powered root-cause analysis
- Determine issue severity
- Visualize log distribution using Chart.js
- Display results through a responsive Bootstrap dashboard
- Continue showing standard analysis if the AI service is unavailable

## Technologies Used

- Python
- Flask
- Google Gemini API
- HTML
- Bootstrap
- Jinja2
- Chart.js
- Git and GitHub

## Project Workflow

```text
Log File Upload
       |
       v
Flask Backend
       |
       v
Log Parser
       |
       +----> INFO, WARNING, and ERROR Counts
       |
       +----> Error and Warning Extraction
       |
       v
Gemini API
       |
       v
AI Root-Cause Analysis
       |
       v
Bootstrap Results Dashboard
```

## Project Structure

```text
ai-log-analyzer/
|
|-- app.py
|-- ai_analysis.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|
|-- templates/
|   |-- index.html
|   |-- result.html
|   `-- history.html
|
`-- uploads/
    `-- .gitkeep
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Aditya-Mac/ai-log-analyzer.git
cd ai-log-analyzer
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure the Gemini API key

Create a Gemini API key and store it as an environment variable.

#### Windows PowerShell

For the current terminal session:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

To save it persistently:

```powershell
setx GEMINI_API_KEY "your-api-key"
```

After using `setx`, close the terminal and open a new one.

Never add the real API key directly to the source code.

### 4. Run the application

```bash
python app.py
```

Open the following address in a browser:

```text
http://127.0.0.1:5000
```

## Example Log

```log
INFO Application Started
WARNING Memory Usage High
ERROR Database Connection Failed
ERROR Timeout While Calling API
```

The application will:

- Count each log severity
- Extract warnings and errors
- Generate a troubleshooting summary
- Send relevant log entries to Gemini
- Display AI-generated root-cause analysis and recommended actions

## Security

- The Gemini API key is read from the `GEMINI_API_KEY` environment variable.
- API keys and environment files are excluded through `.gitignore`.
- Uploaded log files are not committed to GitHub.
- File names are sanitized before files are saved.
- The application continues working with standard analysis if Gemini is unavailable.

## Current Limitations

- The application uses the Flask development server.
- AI response time depends on Gemini API availability.
- Very large log files may require additional filtering or chunking.
- Uploaded logs are processed locally and sent to the configured AI service for analysis.

## Future Improvements

- Add support for additional log formats
- Process large logs in smaller chunks
- Mask sensitive information before sending logs to AI
- Add asynchronous AI processing
- Add automated tests
- Containerize the application with Docker
- Deploy the application to a cloud platform

## Author

Aditya Macharla