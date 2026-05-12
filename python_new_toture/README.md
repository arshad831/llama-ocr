# Python Tutor Bot

Python Tutor Bot is a beginner-friendly educational AI app built with Python, Gradio, and the OpenAI Python SDK.

It helps learners:

- Explain Python concepts
- Debug Python errors
- Take short quizzes
- Improve Python code

## Project Files

- `app.py` - Gradio app and OpenAI call
- `prompts.py` - reusable prompt templates
- `requirements.txt` - Python dependencies
- `.env.example` - example environment variables

## Local Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your OpenAI API key to `.env`:

```bash
OPENAI_API_KEY=your_real_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```

5. Run the app:

```bash
python app.py
```

## Hugging Face Spaces Deployment

1. Create a new Hugging Face Space.
2. Choose **Gradio** as the Space SDK.
3. Upload these project files to the Space:
   - `app.py`
   - `prompts.py`
   - `requirements.txt`
   - `README.md`
4. In the Space settings, add a secret:

```bash
OPENAI_API_KEY=your_real_openai_api_key
```

5. Optional: add this secret if you want to change the model:

```bash
OPENAI_MODEL=gpt-4o-mini
```

The `.env` file is for local development only and should not be committed or uploaded with your real API key.
