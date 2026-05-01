import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()

def truncate(text: str, max_chars: int = 1000) -> str:
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text