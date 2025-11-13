import re

def valid_phone(phone):
    return bool(re.fullmatch(r"(\+?\d[\d\s\-]{7,})", phone))
