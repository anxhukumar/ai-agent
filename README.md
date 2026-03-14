# AI Agent Playground

A Python project that demonstrates a CLI AI agent and a sample calculator app.

## What's included

- `main.py`: Runs the AI agent loop using the Gemini API and local file/function tools.
- `functions/`: Helper functions for listing files, reading files, writing files, and running Python scripts.
- `calculator/`: A standalone calculator example with its own CLI and unit tests.

## Quick start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your Gemini API key:
   ```bash
   export GEMINI_API_KEY="your_api_key"
   ```
3. Run the agent:
   ```bash
   python3 main.py "List files in this project"
   ```

## Run tests

```bash
python3 -m unittest calculator/tests.py
```
