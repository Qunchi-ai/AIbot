import re

def valid_phone(text: str) -> bool:
    pattern = r"^\+?\d{7,15}$"
    return bool(re.match(pattern, text))
