# Running Lab 5

```sh
python -m pip install -r requirements-dev.txt
python recruitment_tracker.py
python -m pylint recruitment_tracker.py
python -m bandit -r recruitment_tracker.py
python -m flake8 recruitment_tracker.py
```

See [issues.md](issues.md) and [reflection.md](reflection.md). Files ending in `_before.txt` record the starter analysis. Files ending in
`_after.txt` record the cleaned application. A blank Flake8 report
means Flake8 found no violations.
