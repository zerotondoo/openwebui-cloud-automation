# OpenWebUI Automation

A Python-based automation script for streamlined interaction with OpenWebUI, specifically designed for processing meeting transcripts.

## Features

- Native macOS file picker for .txt files
- Configurable default directories and OpenWebUI URL
- Model selection with quick-access to default and last used models
- Automatic chat initialization with transcript upload
- Comprehensive error handling and logging

## Requirements

- Python 3.8+
- macOS
- Running OpenWebUI instance

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit `config.yaml` to customize:
- Default transcript folder location
- OpenWebUI URL
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
4. Open the chat in your default browser

## Error Handling

All errors are:
- Displayed in user-friendly dialog boxes
- Logged to `./logs/automation.log`
- Handled gracefully with appropriate recovery options

## Project Structure

```
openwebui-automation/
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
```
