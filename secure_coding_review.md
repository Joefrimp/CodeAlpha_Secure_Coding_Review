# Secure Coding Review Report

**Project:** CodeAlpha Cyber Security Internship - Task 3

**Application:** `vulnerable_app.py` (Flask Application)

**Review Date:** April 28, 2026

****

## 1. Summary

This report details the findings of a secure coding review performed on a Python Flask application (`vulnerable_app.py`). The review utilized the static analysis tool Bandit to identify potential security vulnerabilities. The analysis revealed critical issues related to SQL Injection and the insecure configuration of the Flask application.

## 2. Findings

### 2.1. SQL Injection Vulnerabilities (CWE-89)

**Description:** The application constructs SQL queries by directly concatenating user-supplied input without proper sanitization or parameterization. This practice makes the application vulnerable to SQL injection attacks, where an attacker can manipulate the SQL query to gain unauthorized access to data, modify data, or bypass authentication.

**Severity:** Medium**Confidence:** Low (as reported by Bandit, but in practice, these are high-risk vulnerabilities)

**Occurrences:**

| File | Line Number | Code Snippet |
| --- | --- | --- |
| `vulnerable_app.py` | 48 | `query = f"SELECT * FROM users WHERE username = \'{username}\' AND password = \'{password}\'"` |
| `vulnerable_app.py` | 67 | `search_query = f"SELECT username FROM users WHERE username LIKE \'%{query}%\'"` |

**Remediation:**

To prevent SQL injection, always use parameterized queries or prepared statements. Most database libraries provide mechanisms for this. For `sqlite3` in Python, this involves passing parameters as a tuple to the `execute` method, rather than embedding them directly into the query string.

**Example of Remediation (for login function):**

```python
conn = sqlite3.connect(database)
cursor = conn.cursor()
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
user = cursor.fetchone()
conn.close()
```

### 2.2. Flask Debug Mode Enabled (CWE-94)

**Description:** The Flask application is configured to run with `debug=True` in a production-like environment. The Werkzeug debugger, which is enabled when debug mode is active, allows the execution of arbitrary code, posing a severe security risk. This can lead to remote code execution (RCE) if an attacker gains access to the debugger PIN.

**Severity:** High**Confidence:** Medium

**Occurrence:**

| File | Line Number | Code Snippet |
| --- | --- | --- |
| `vulnerable_app.py` | 80 | `app.run(debug=True, port=5000)` |

**Remediation:**

Debug mode should **never** be enabled in a production environment. It is intended for development purposes only. For deployment, ensure `debug=False` or remove the `debug` parameter entirely, as Flask defaults to `False` in a production setting.

**Example of Remediation:**

```python
if __name__ == '__main__':
    init_db()
    # Ensure debug=False or remove the parameter for production
    app.run(debug=False, port=5000)
```

## 3. Conclusion

The `vulnerable_app.py` application contains significant security flaws that must be addressed before deployment. The SQL injection vulnerabilities could lead to data breaches and unauthorized access, while the enabled debug mode presents a critical remote code execution risk. Implementing the recommended remediation steps is crucial for securing the application.

## 4. References

- [CWE-89: Improper Neutralization of Special Elements used in an SQL Command (‘SQL Injection’)](https://cwe.mitre.org/data/definitions/89.html)

- [CWE-94: Improper Control of Generation of Code (‘Code Injection’)](https://cwe.mitre.org/data/definitions/94.html)

- [Bandit B608: Hardcoded SQL expressions](https://bandit.readthedocs.io/en/1.9.4/plugins/b608_hardcoded_sql_expressions.html)

- [Bandit B201: Flask debug mode enabled](https://bandit.readthedocs.io/en/1.9.4/plugins/b201_flask_debug_true.html)