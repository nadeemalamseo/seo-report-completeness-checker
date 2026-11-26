from datetime import date

import pytest

from seo_report_checker.validators import validate_findings


def base():
    return {
        "id": "F-1",
        "issue": "Missing title",
        "affected_url": "https://example.com/a",
        "evidence": "Title element is absent from the page.",
        "impact": "HIGH",
        "priority": "HIGH",
        "recommendation": "Add a unique descriptive title element.",
        "implementation_status": "OPEN",
        "verification": "",
    }


def test_complete():
    assert not validate_findings([base()], date(2026, 9, 29))[0].issues


def test_missing_fields():
    row = base()
    row["evidence"] = ""
    row["recommendation"] = ""
    codes = validate_findings([row], date(2026, 9, 29))[0].issues
    assert "MISSING_EVIDENCE" in codes
    assert "MISSING_RECOMMENDATION" in codes


def test_missing_id_is_reported():
    row = base()
    row["id"] = ""
    assert "MISSING_ID" in validate_findings([row])[0].issues


def test_invalid_values():
    row = base()
    row["priority"] = "URGENT"
    row["implementation_status"] = "DONE"
    codes = validate_findings([row])[0].issues
    assert "INVALID_PRIORITY" in codes
    assert "INVALID_IMPLEMENTATION_STATUS" in codes


def test_verified_requires_verification_evidence_and_date():
    row = base()
    row["implementation_status"] = "VERIFIED"
    codes = validate_findings([row])[0].issues
    assert "MISSING_VERIFICATION" in codes
    assert "MISSING_VERIFICATION_DATE" in codes


def test_verified_with_evidence_and_date_passes():
    row = base()
    row.update(
        implementation_status="VERIFIED",
        verification="Confirmed after recrawl.",
        verification_date="2026-09-28",
    )
    assert not validate_findings([row], date(2026, 9, 29))[0].issues


def test_ready_for_verification_requires_verification():
    row = base()
    row["implementation_status"] = "READY_FOR_VERIFICATION"
    assert "MISSING_VERIFICATION" in validate_findings([row])[0].issues


def test_duplicate():
    row = base()
    findings = validate_findings([row, dict(row)])
    assert "DUPLICATE_FINDING" in findings[1].issues
    assert "DUPLICATE_FINDING_ID" in findings[1].issues


def test_overdue():
    row = base()
    row["due_date"] = "2026-09-01"
    assert "OVERDUE_FINDING" in validate_findings([row], date(2026, 9, 29))[0].warnings


def test_invalid_due_date():
    row = base()
    row["due_date"] = "not-a-date"
    assert "INVALID_DUE_DATE" in validate_findings([row])[0].issues


def test_invalid_verification_date():
    row = base()
    row.update(implementation_status="VERIFIED", verification="Confirmed", verification_date="yesterday")
    assert "INVALID_VERIFICATION_DATE" in validate_findings([row])[0].issues


def test_future_verification_date():
    row = base()
    row.update(implementation_status="VERIFIED", verification="Confirmed", verification_date="2026-10-01")
    assert "FUTURE_VERIFICATION_DATE" in validate_findings([row], date(2026, 9, 29))[0].issues


def test_empty_report_is_rejected():
    with pytest.raises(ValueError, match="no findings"):
        validate_findings([])


def test_strict_promotes_warnings():
    row = base()
    row["evidence"] = "Needs improvement"
    finding = validate_findings([row], date(2026, 9, 29), strict=True)[0]
    assert "WEAK_EVIDENCE" in finding.issues
    assert not finding.warnings
