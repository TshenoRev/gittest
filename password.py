import stdio

def is_good_password(s: str) -> str:
    if len(s) < 8:
        return 'Weak password'  # Too short
    if not any(c.isdigit() for c in s):
        return 'Weak password'  # No digit
    if not any(c.isupper() for c in s):
        return 'Weak password'  # No uppercase letter
    if not any(c.islower() for c in s):
        return 'Weak password'  # No lowercase letter
    if not any(not c.isalnum() for c in s):
        return 'Weak password'  # No non-alphanumeric character
    return 'Good password'  # All conditions met

# the following are my Test cases
test_passwords = [
    "Pass.0",      # Weak (too short)
    "Pass.wrd",    # Weak (no digit)
    "pass.w0rd",   # Weak (no uppercase letter)
    "PASS.W0RD",   # Weak (no lowercase letter)
    "Passw0rd",    # Weak (no non-alphanumeric letter)
    "Pass.w0rd"    # Good
]

for password in test_passwords:
    result = is_good_password(password)
    stdio.writeln(f"{password}: {result}")
