# Assignment Submission Portal

A simple Flask web app where students submit their name, registration number,
assignment title and a submission URL. Every push is tested automatically by CI.

## Requirements
- Python 3.10+
- Git

## Setup
```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Run the application
```bash
python app.py
```
Open http://127.0.0.1:5000

## Run the tests
```bash
pytest -v
```

## Start the report receiver
_(to be added)_

## CI pipeline
_(to be added)_