from datetime import date
from .models import Finding
from .normalize import clean, is_weak_text, looks_like_url, normalize_key

REQUIRED = ("issue","affected_url","evidence","impact","priority","recommendation","implementation_status")
IMPACTS = {"LOW","MEDIUM","HIGH","CRITICAL"}
PRIORITIES = {"LOW","MEDIUM","HIGH","CRITICAL","1","2","3","4"}
STATUSES = {"OPEN","IN_PROGRESS","BLOCKED","READY_FOR_VERIFICATION","VERIFIED","WONT_FIX"}

def validate_findings(rows, today=None, strict=False):
    today = today or date.today()
    findings, seen_ids, seen_pairs = [], set(), set()
    for n, raw in enumerate(rows, start=2):
        data = {str(k): clean(v) for k, v in raw.items()}
        f = Finding(n, data)
        fid = normalize_key(data.get("id"))
        if fid:
            if fid in seen_ids: f.issues.append("DUPLICATE_FINDING_ID")
            seen_ids.add(fid)
        pair = (normalize_key(data.get("issue")), normalize_key(data.get("affected_url")))
        if pair != ("",""):
            if pair in seen_pairs: f.issues.append("DUPLICATE_FINDING")
            seen_pairs.add(pair)
        for field in REQUIRED:
            if not data.get(field): f.issues.append("MISSING_" + field.upper())
        if data.get("affected_url") and not looks_like_url(data["affected_url"]):
            f.issues.append("INVALID_AFFECTED_URL")
        if data.get("evidence") and is_weak_text(data["evidence"]): f.warnings.append("WEAK_EVIDENCE")
        if data.get("recommendation") and is_weak_text(data["recommendation"]): f.warnings.append("WEAK_RECOMMENDATION")
        impact = data.get("impact","").upper()
        if impact and impact not in IMPACTS: f.issues.append("INVALID_IMPACT")
        priority = data.get("priority","").upper()
        if priority and priority not in PRIORITIES: f.issues.append("INVALID_PRIORITY")
        status = data.get("implementation_status","").upper()
        if status and status not in STATUSES: f.issues.append("INVALID_IMPLEMENTATION_STATUS")
        verification = data.get("verification")
        if status in {"READY_FOR_VERIFICATION","VERIFIED"} and not verification:
            f.issues.append("MISSING_VERIFICATION")
        if status == "VERIFIED" and verification:
            pass
        if status == "OPEN" and data.get("verification_date"):
            f.warnings.append("STATUS_VERIFICATION_CONFLICT")
        due = data.get("due_date")
        if due:
            try:
                due_date = date.fromisoformat(due)
                if due_date < today and status not in {"VERIFIED","WONT_FIX"}: f.warnings.append("OVERDUE_FINDING")
            except ValueError:
                f.issues.append("INVALID_DUE_DATE")
        if strict:
            f.issues.extend(f.warnings); f.warnings = []
        findings.append(f)
    return findings

def summary(findings):
    return {"total_findings":len(findings),"complete":sum(not f.issues and not f.warnings for f in findings),"incomplete":sum(bool(f.issues or f.warnings) for f in findings),"errors":sum(len(f.issues) for f in findings),"warnings":sum(len(f.warnings) for f in findings)}
