# Static analysis findings

Line numbers refer to the assigned starter script. The tool reports are grouped by run.

| Issue | Type | Starter line(s) | Description | Fix |
| --- | --- | ---: | --- | --- |
| Bandit B608 | Security, medium | 8 | Applicant data was interpolated into an SQL statement. Ordinary names containing apostrophes could break the insert. | Bind the four values with SQLite placeholders. |
| Bandit B307 / Pylint W0123 | Security, medium | 14 | The salary budget was evaluated as a Python expression. | Parse a bounded arithmetic expression and evaluate only numeric constants and approved operators. |
| Bandit B110 / Pylint W0718 | Error handling, low Bandit severity | 24–29 | The status update could silently swallow a database error. | Use a transaction context and let callers see exceptions. |
| Pylint R1710 | Correctness | 12–21 | An empty shortlist implicitly returned None. | Always return a list. |
| Pylint W0612 / Flake8 F841 | Maintainability | 15 | The row count was assigned and unused. | Remove the assignment. |
| Pylint W1514 and R1732 | Resource handling | 31–36 | The export used the platform encoding and could leave a file open if a write failed. | Use a context manager, UTF-8, and the CSV writer for quoting. |
| Pylint C0103 and C0116 | Naming and documentation | 7, 12, 24, 31, 38, 42 | Several function names used camelCase and functions lacked docstrings. | Use documented snake_case entry points and preserve the original names as compatibility aliases. |
| Flake8 E501, E302, W291 | Style | 4, 8, 15, 31 and others | Long lines, spacing between functions, and trailing whitespace reduced readability. | Reformat queries and functions and remove trailing whitespace. |

The demo should print `['Nina']` and `2 in interview`. The CSV should contain
Nina and Omar in interview and Priya as applied.
