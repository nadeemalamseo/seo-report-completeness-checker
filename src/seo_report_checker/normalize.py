import re
from urllib.parse import urlparse

def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()

def normalize_key(value: object) -> str:
    return clean(value).casefold()

def looks_like_url(value: str) -> bool:
    try:
        p = urlparse(value)
        return p.scheme in {"http", "https"} and bool(p.netloc)
    except ValueError:
        return False

def is_weak_text(value: str) -> bool:
    text = clean(value).casefold()
    if not text:
        return False
    generic = {"needs improvement","seo issue found","poor optimization","should be fixed","improve seo","fix this issue","optimize page","review problem"}
    return text in generic or len(text) < 8
