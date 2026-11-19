import ast
import operator
import sqlite3
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


conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE applicants (id INTEGER PRIMARY KEY, name TEXT, role TEXT, expected_salary INTEGER, status TEXT)")


def addApplicant(name, role, expected_salary, status="applied"):
    conn.execute(
        "INSERT INTO applicants (name, role, expected_salary, status) "
        "VALUES (?, ?, ?, ?)", (name, role, expected_salary, status)
    )
    conn.commit()


def shortlist(role, salary_rule):
    rows = conn.execute("SELECT name, expected_salary FROM applicants WHERE role = ?", (role,)).fetchall()
    limit = _salary_limit(salary_rule)
    total_seen = len(rows)   
    result = []
    for name, salary in rows:
        if salary <= limit:
            result.append(name)
    if result:
        return result


def updateStatus(applicant_id, status):
    with conn:
        conn.execute(
            "UPDATE applicants SET status = ? WHERE id = ?",
            (status, applicant_id),
        )

def exportReport(path):
    f = open(path, "w")
    for row in conn.execute("SELECT name, role, status FROM applicants"):
        f.write(",".join(row) + "\n")
    f.close()


def countByStatus(status):
    return conn.execute("SELECT COUNT(*) FROM applicants WHERE status = ?", (status,)).fetchone()[0]


def main():
    addApplicant("Nina", "analyst", 600000)
    addApplicant("Omar", "analyst", 750000, "interview")
    addApplicant("Priya", "developer", 900000)
    updateStatus(1, "interview")
    print(shortlist("analyst", "500000 + 150000"))
    exportReport("applicants_report.csv")
    print(countByStatus("interview"), "in interview")


main()
