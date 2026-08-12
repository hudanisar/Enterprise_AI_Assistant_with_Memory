import re
SENSITIVE = re.compile(r"(api[_ -]?key|password|token|secret|credit card)", re.I)
PATTERNS = [("preference", re.compile(r"(?:remember that )?i (?:prefer|like|love) (.+)", re.I)), ("project", re.compile(r"i(?:'m| am) working on (.+)", re.I)), ("instruction", re.compile(r"(?:always|please) (.+)", re.I))]
def extract_memories(text: str):
    if SENSITIVE.search(text): return []
    for kind, pattern in PATTERNS:
        match = pattern.search(text)
        if match:
            value = match.group(1).strip(" .")
            if len(value) > 2: return [(kind, f"User {kind}s {value}." if kind == "preference" else f"User is working on {value}." if kind == "project" else value)]
    return []

