# Assignment Submission Portal

A simple Flask web app where students submit their name, registration number,
assignment title and a submission URL. Every push is tested automatically by CI,
and the test report is saved on the instructor's computer as `test-report.json`.

## Requirements
- Python 3.10+
- Git

## Setup
```bash
python -m venv venv
venv\Scripts\activate      
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
The 3 tests check: a valid submission is saved and listed, a missing
registration number is rejected, and an invalid URL is rejected and not saved.

## Start the report receiver
```bash
python receiver.py
```
The receiver listens on http://localhost:8000. When it gets a POST request with
a JSON body, it saves the body as `test-report.json` in the project folder.
Keep it running while CI runs.

## CI pipeline
The workflow `.github/workflows/ci.yml` runs on every push:
1. Installs dependencies.
2. Runs the tests with `pytest` and writes real results to `pytest-raw.json`.
3. Runs `send_report.py`, which builds the report (repository, branch, commit SHA,
   run ID, timestamp, each test result and failure message, totals and overall
   status) and POSTs it to the receiver.

The report step uses `if: always()`, so the report is delivered for both passing
and failing runs. The job runs on a self-hosted runner on the instructor's
computer, so `localhost:8000` reaches the receiver.

### Self-hosted runner setup
Repo -> Settings -> Actions -> Runners -> New self-hosted runner (Windows),
then run `./run.cmd` in the runner folder.

## Demo
1. Push working code: the run is green and the report shows `passed`.
2. Introduce a defect in URL validation and push: the run is red and the report shows `failed`.
3. Fix the defect and push: the run is green again.