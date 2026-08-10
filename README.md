# docx_template_filler

A Streamlit web app that fills placeholders in `.docx` templates using values from an `.xlsx` spreadsheet or from user input.

## How It Works

1. Upload a `.docx` template containing `\$PLACEHOLDER` tokens
2. Upload an `.xlsx` file with two columns: placeholder names (without the \$) (col 1) and replacement values (col 2)
2a. Alternatively enter placeholder tokens (without the \$) and target values by hand.
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
