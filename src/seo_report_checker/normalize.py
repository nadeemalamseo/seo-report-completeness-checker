import ipaddress
import re
from urllib.parse import urlsplit


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_key(value: object) -> str:
    return clean(value).casefold()


def looks_like_url(value: str) -> bool:
    """Check URL syntax without making a network request or judging reachability."""
    if not value or value != value.strip() or any(ch.isspace() or ord(ch) < 32 for ch in value):
        return False
    try:
        parsed = urlsplit(value)
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
            return False
        if parsed.username is not None or parsed.password is not None:
            return False
        host = parsed.hostname
        if not host:
            return False
        # Accessing .port validates malformed and out-of-range port values.
        port = parsed.port
        if port is not None and not 1 <= port <= 65535:
            return False
        try:
            ipaddress.ip_address(host)
            return True
        except ValueError:
            pass
        if host.endswith("."):
            host = host[:-1]
        ascii_host = host.encode("idna").decode("ascii")
        if len(ascii_host) > 253 or not ascii_host:
            return False
        labels = ascii_host.split(".")
        if any(not label or len(label) > 63 for label in labels):
            return False
        if any(not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?", label) for label in labels):
            return False
        # A dotted numeric host that failed IP parsing is not a valid hostname.
        if re.fullmatch(r"[0-9.]+", ascii_host):
            return False
        return True
    except (UnicodeError, ValueError):
        return False


def is_weak_text(value: str) -> bool:
    text = clean(value).casefold()
    if not text:
        return False
    generic = {
        "needs improvement", "seo issue found", "poor optimization",
        "should be fixed", "improve seo", "fix this issue",
        "optimize page", "review problem",
    }
    return text in generic or len(text) < 8
