from datetime import date
from seo_report_checker.validators import validate_findings

def base():
    return {"id":"F-1","issue":"Missing title","affected_url":"https://example.com/a","evidence":"Title element is absent from the page.","impact":"HIGH","priority":"HIGH","recommendation":"Add a unique descriptive title element.","implementation_status":"OPEN","verification":""}

def test_complete(): assert not validate_findings([base()],date(2026,9,29))[0].issues
def test_missing_fields():
    row=base(); row["evidence"]=""; row["recommendation"]=""
    codes=validate_findings([row],date(2026,9,29))[0].issues
    assert "MISSING_EVIDENCE" in codes and "MISSING_RECOMMENDATION" in codes
def test_invalid_values():
    row=base(); row["priority"]="URGENT"; row["implementation_status"]="DONE"
    codes=validate_findings([row])[0].issues
    assert "INVALID_PRIORITY" in codes and "INVALID_IMPLEMENTATION_STATUS" in codes
def test_verified_requires_verification():
    row=base(); row["implementation_status"]="VERIFIED"
    assert "VERIFIED_WITHOUT_EVIDENCE" in validate_findings([row])[0].issues
def test_duplicate():
    row=base(); findings=validate_findings([row,dict(row)])
    assert "DUPLICATE_FINDING" in findings[1].issues and "DUPLICATE_FINDING_ID" in findings[1].issues
def test_overdue():
    row=base(); row["due_date"]="2026-09-01"
    assert "OVERDUE_FINDING" in validate_findings([row],date(2026,9,29))[0].warnings
def test_invalid_date():
    row=base(); row["due_date"]="not-a-date"
    assert "INVALID_DUE_DATE" in validate_findings([row])[0].issues
