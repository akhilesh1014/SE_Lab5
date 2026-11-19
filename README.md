# Lab 5 — Static Code Analysis

The [recruitment tracker](recruitment_tracker.py) stores applicants in SQLite, shortlists them by position and salary budget, updates interview status, and exports a CSV report. The lab uses Pylint, Bandit, and Flake8 to identify issues in the starter implementation and verify the fixes.

## Run the demo and analysis

```sh
python -m pip install -r requirements-dev.txt
python recruitment_tracker.py
python -m pylint recruitment_tracker.py
python -m bandit -r recruitment_tracker.py
python -m flake8 recruitment_tracker.py
```

The demo prints `['Nina']` and `2 in interview` and writes `applicants_report.csv` in the current directory.

## Results

| Tool | Result | Reports |
| --- | --- | --- |
| Pylint | Improved from 4.47/10 to 10.00/10 | [Before](pylint_report_before.txt) · [After](pylint_report_after.txt) |
| Bandit | No issues reported after fixes | [Before](bandit_report_before.txt) · [After](bandit_report_after.txt) |
| Flake8 | No violations reported after fixes | [Before](flake8_report_before.txt) · [After](flake8_report_after.txt) |

See the [issue log](issues.md) for the findings and fixes and the [reflection](reflection.md) for the lab discussion.
