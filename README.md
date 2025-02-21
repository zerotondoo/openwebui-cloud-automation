# OpenWebUI Cloud Automation

A Python-based automation script for streamlined interaction with OpenWebUI's cloud service, specifically designed for processing meeting transcripts using OpenAI-compatible API endpoints.

## Features

- Native macOS file picker for .txt files
- Configurable default directories and OpenWebUI URL
- Model selection with quick-access to default and last used models
- Automatic chat initialization with transcript upload
- Comprehensive error handling and logging
- Secure API key authentication
- OpenAI-compatible API endpoints

## Requirements

- Python 3.8+
- macOS
- Access to an OpenWebUI server with API key

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Set up your OpenWebUI API key:
   ```bash
   export OPENWEBUI_API_KEY=your_api_key_here
   ```

2. Edit `config.yaml` to customize:
   - Default transcript folder location
   - OpenWebUI server URL
   - Default model preferences
   - Logging settings

## Usage

Run the script:
```bash
python src/main.py
```

The script will:
1. Open a file picker for selecting a transcript
2. Present available models for selection
3. Initialize a new chat with the selected model
4. Upload the transcript to your OpenWebUI server
5. Open the chat in your default browser

## Error Handling

All errors are:
- Displayed in user-friendly dialog boxes
- Logged to `./logs/automation.log`
- Handled gracefully with appropriate recovery options

## Security

This version uses secure API key authentication and can safely connect to internet-accessible OpenWebUI servers. The API key is stored as an environment variable for enhanced security.

## Project Structure

```
openwebui-cloud-automation/
├── config.yaml          # Configuration settings
├── requirements.txt     # Python dependencies
├── src/
│   ├── main.py         # Main script
│   ├── config_manager.py
│   ├── file_picker.py
│   ├── model_selector.py
│   ├── webui_client.py
│   └── utils/
│       ├── logger.py
│       └── error_handler.py
└── logs/
    └── automation.log
