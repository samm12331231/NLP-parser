# NLP Parser

A small natural language parser built with **NLTK** and a simple **Flask** web UI.

## What it does

- Parses a sentence using a context-free grammar (CFG)
- Produces one or more parse trees
- Extracts noun phrase (NP) chunks from parsed trees
- Supports both command-line and browser-based usage

## Project files

- `parser.py` — core grammar, sentence preprocessing, parsing, and NP chunk extraction (CLI runnable)
- `app.py` — Flask interface for entering text and viewing parse output
- `templates/index.html` — web page template
- `sentences/` — sample input sentence files
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.9+ (recommended)
- pip

Dependencies:

- `Flask>=3.0.3,<4.0`
- `Werkzeug>=3.0.3,<4.0`
- `nltk==3.9.1`

## Setup

```bash
pip install -r requirements.txt
```

## Usage

### 1) Run from command line

```bash
python parser.py
```

or with a sample file:

```bash
python parser.py sentences/1.txt
```

### 2) Run web app

```bash
python app.py
```

Then open:

`http://localhost:10000`

## Notes

- Input text is lowercased and tokenized, with non-alphabetic characters stripped from each token.
- If a sentence cannot be parsed by the defined grammar, no parse tree is returned.
- Flask debug mode is off by default and can be enabled with `FLASK_DEBUG=1`.
