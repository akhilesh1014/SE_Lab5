"""Track job applicants and export an SQLite-backed recruitment report."""

import ast
import csv
import operator
import sqlite3
from contextlib import closing
from math import isfinite


BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _budget_value(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPERATORS:
        return BINARY_OPERATORS[type(node.op)](
            _budget_value(node.left), _budget_value(node.right)
        )
    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPERATORS:
        return UNARY_OPERATORS[type(node.op)](_budget_value(node.operand))
    raise ValueError("salary budget must use numbers and basic arithmetic")


def _salary_limit(salary_rule):
    if type(salary_rule) in (int, float):
        limit = salary_rule
    elif isinstance(salary_rule, str) and len(salary_rule) <= 128:
        try:
            expression = ast.parse(salary_rule.strip(), mode="eval")
            limit = _budget_value(expression.body)
        except (SyntaxError, ZeroDivisionError, OverflowError) as error:
            raise ValueError("invalid salary budget") from error
    else:
        raise ValueError("invalid salary budget")
    if limit < 0 or (isinstance(limit, float) and not isfinite(limit)):
        raise ValueError("salary budget must be finite and nonnegative")
    return limit


def _create_database():
    database = sqlite3.connect(":memory:")
    database.execute(
        "CREATE TABLE applicants ("
        "id INTEGER PRIMARY KEY, name TEXT, role TEXT, "
        "expected_salary INTEGER, status TEXT)"
    )
    return database


def add_applicant(name, role, expected_salary, status="applied"):
    """Record an applicant and their initial hiring status."""
    with conn:
        conn.execute(
            "INSERT INTO applicants (name, role, expected_salary, status) "
            "VALUES (?, ?, ?, ?)",
            (name, role, expected_salary, status),
        )


def shortlist(role, salary_rule):
    """Return applicants for the role within the inclusive salary budget."""
    limit = _salary_limit(salary_rule)
    rows = conn.execute(
        "SELECT name, expected_salary FROM applicants "
        "WHERE role = ? ORDER BY id",
        (role,),
    )
    return [name for name, salary in rows if salary <= limit]


def update_status(applicant_id, status):
    """Update the applicant's hiring status."""
    with conn:
        conn.execute(
            "UPDATE applicants SET status = ? WHERE id = ?",
            (status, applicant_id),
        )


def export_report(path):
    """Export applicant names, roles, and statuses as UTF-8 CSV."""
    rows = conn.execute(
        "SELECT name, role, status FROM applicants ORDER BY id"
    )
    with open(path, "w", encoding="utf-8", newline="") as report:
        csv.writer(report).writerows(rows)


def count_by_status(status):
    """Count applicants with the given hiring status."""
    return conn.execute(
        "SELECT COUNT(*) FROM applicants WHERE status = ?", (status,)
    ).fetchone()[0]


# Preserve the starter module's function names for existing callers.
# pylint: disable=invalid-name
addApplicant = add_applicant
updateStatus = update_status
exportReport = export_report
countByStatus = count_by_status
# pylint: enable=invalid-name

conn = _create_database()


def main():
    """Run the demonstration and write the sample report."""
    add_applicant("Nina", "analyst", 600000)
    add_applicant("Omar", "analyst", 750000, "interview")
    add_applicant("Priya", "developer", 900000)
    update_status(1, "interview")
    print(shortlist("analyst", "500000 + 150000"))
    export_report("applicants_report.csv")
    print(count_by_status("interview"), "in interview")


if __name__ == "__main__":
    with closing(conn):
        main()
