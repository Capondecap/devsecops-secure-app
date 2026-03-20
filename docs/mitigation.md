# Security Mitigation Guide

## 1. Command Injection Mitigation

### Issue

- User input is passed directly into system commands

### Mitigation

- Use `subprocess.run()` with argument lists instead of shell execution
- Validate and sanitize input before use
- Restrict input to expected formats such as IPv4 or IPv6 addresses
- Avoid `os.popen` and other shell-based execution helpers

### Example Fix

```python
subprocess.run(["ping", "-c", "1", ip], capture_output=True)
```

## 2. SQL Injection Mitigation

### Issue

- SQL queries are constructed using string concatenation

### Mitigation

- Use parameterized queries for all database access
- Treat all external input as untrusted
- Never directly insert user input into SQL statements

### Example Fix

```python
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

## 3. Insecure Deserialization Mitigation

### Issue

- Application uses `pickle.loads()` on user-controlled input

### Mitigation

- Do not use `pickle` for untrusted data
- Use safer formats such as JSON
- Validate expected fields and data types before processing
- Enforce input structure with schema validation where possible

## 4. Container Security Best Practices

### Improvements

- Use minimal base images such as `python:slim`
- Avoid installing unnecessary tools in production images
- Run the application as a non-root user
- Remove unused packages and reduce image surface area

## 5. CI/CD Security Improvements

### Improvements

- Keep security gates enforced in the pipeline
- Add secrets scanning such as `gitleaks`
- Pin dependency versions and review updates regularly
- Fail builds on high and critical vulnerabilities
