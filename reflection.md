# Static analysis reflection

## 1. How do Flake8, Pylint, and Bandit differ?

Flake8 found formatting and unused-variable problems. Pylint found naming,
documentation, resource-management, and control-flow problems. Bandit found
security-sensitive constructs in database queries, budget evaluation, and
error handling. Running all three gave more coverage across code quality,
style, and security. Running the demo separately verified the expected output.

## 2. Which findings mattered most?

The database insert built SQL from applicant data and the shortlist ran the
salary-budget string as Python. Parameter binding and a restricted arithmetic
parser addressed those risks. The status update also hid database exceptions.
A caller could believe a failed update had succeeded, so it now receives
the database error and the transaction rolls back.

## 3. What trade-offs did the fixes involve?

The sample uses an arithmetic expression for the salary budget. The parser
keeps addition, subtraction, multiplication, division, and parentheses,
which cover the demonstration and common budget calculations. Unsupported
expressions fail with a validation error. The new names use snake_case and
aliases preserve calls made with the starter's public names.

## 4. Where could these tools run in the development process?

Developers can run the checks locally before committing and rerun them on
each pull request. A CI job can require Flake8 and Bandit to exit cleanly,
enforce a Pylint score above 9.5, and publish the tool output. A separate
test job should verify the application behavior.
