# docx_template_filler

A Streamlit web app that fills placeholders in `.docx` templates using values entered directly in the app.

## How It Works

1. Upload a `.docx` template containing `\$PLACEHOLDER` tokens
2. The app scans the document and shows a text input for each placeholder it finds; fill in a value for each and click "Fill All"
2a. Alternatively, expand "Replace a single placeholder manually" to replace one token at a time by hand.
3. Download the filled document with all formatting preserved

## Setup

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

## Run

```bash
.venv\Scripts\streamlit run main.py
```
