from datetime import date

from .models import Finding
from .normalize import clean, is_weak_text, looks_like_url, normalize_key

REQUIRED = (
    "id", "issue", "affected_url", "evidence", "impact", "priority",
    "recommendation", "implementation_status",
)
IMPACTS = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
PRIORITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL", "1", "2", "3", "4"}
STATUSES = {"OPEN", "IN_PROGRESS", "BLOCKED", "READY_FOR_VERIFICATION", "VERIFIED", "WONT_FIX"}


def _parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def validate_findings(rows, today=None, strict=False):
    """Validate row completeness and consistency using a fixed reference date."""
    today = today or date.today()
    rows = list(rows)
    if not rows:
        raise ValueError("The report contains no findings; an empty report cannot pass validation.")

    findings, seen_ids, seen_pairs = [], set(), set()
    for n, raw in enumerate(rows, start=2):
        if not isinstance(raw, dict):
            raise ValueError(f"Finding at row {n} must be an object.")
        data = {str(k): clean(v) for k, v in raw.items()}
        f = Finding(n, data)
        fid = normalize_key(data.get("id"))
        if fid:
            if fid in seen_ids:
                f.issues.append("DUPLICATE_FINDING_ID")
            seen_ids.add(fid)

        pair = (normalize_key(data.get("issue")), normalize_key(data.get("affected_url")))
        if pair != ("", ""):
            if pair in seen_pairs:
                f.issues.append("DUPLICATE_FINDING")
            seen_pairs.add(pair)

        for field in REQUIRED:
            if not data.get(field):
                f.issues.append("MISSING_" + field.upper())

        url = data.get("affected_url", "")
        if url and not looks_like_url(url):
            f.issues.append("INVALID_AFFECTED_URL")

        if data.get("evidence") and is_weak_text(data["evidence"]):
            f.warnings.append("WEAK_EVIDENCE")
        if data.get("recommendation") and is_weak_text(data["recommendation"]):
            f.warnings.append("WEAK_RECOMMENDATION")

        impact = data.get("impact", "").upper()
        if impact and impact not in IMPACTS:
            f.issues.append("INVALID_IMPACT")
        priority = data.get("priority", "").upper()
        if priority and priority not in PRIORITIES:
            f.issues.append("INVALID_PRIORITY")

        status = data.get("implementation_status", "").upper()
        if status and status not in STATUSES:
            f.issues.append("INVALID_IMPLEMENTATION_STATUS")

        verification = data.get("verification", "")
        verification_date = data.get("verification_date", "")
        if status in {"READY_FOR_VERIFICATION", "VERIFIED"} and not verification:
            f.issues.append("MISSING_VERIFICATION")
        if status == "VERIFIED" and not verification_date:
            f.issues.append("MISSING_VERIFICATION_DATE")
        if verification_date:
            parsed_verification_date = _parse_date(verification_date)
            if parsed_verification_date is None:
                f.issues.append("INVALID_VERIFICATION_DATE")
            elif parsed_verification_date > today:
                f.issues.append("FUTURE_VERIFICATION_DATE")
            if status not in {"VERIFIED", "WONT_FIX"}:
                f.warnings.append("STATUS_VERIFICATION_CONFLICT")

        due = data.get("due_date", "")
        if due:
            due_date = _parse_date(due)
            if due_date is None:
                f.issues.append("INVALID_DUE_DATE")
            elif due_date < today and status not in {"VERIFIED", "WONT_FIX"}:
                f.warnings.append("OVERDUE_FINDING")

        if strict:
            f.issues.extend(f.warnings)
            f.warnings = []
        findings.append(f)
    return findings


def summary(findings):
    return {
        "total_findings": len(findings),
        "complete": sum(not f.issues and not f.warnings for f in findings),
        "incomplete": sum(bool(f.issues or f.warnings) for f in findings),
        "errors": sum(len(f.issues) for f in findings),
        "warnings": sum(len(f.warnings) for f in findings),
    }
