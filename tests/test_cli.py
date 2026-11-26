import json

import pytest

from seo_report_checker.csv_reader import read_csv
from seo_report_checker.json_reader import read_json


def test_json_reader_and_output(tmp_path, monkeypatch, capsys):
    from seo_report_checker.cli import main

    p = tmp_path / "report.json"
    p.write_text(json.dumps([{
        "id": "F-1", "issue": "Missing title", "affected_url": "https://example.com/a",
        "evidence": "Title element is absent.", "impact": "HIGH", "priority": "HIGH",
        "recommendation": "Add a unique title.", "implementation_status": "OPEN", "verification": "",
    }]), encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["seo-report-check", str(p), "--json"])
    assert main() == 0
    assert "summary" in capsys.readouterr().out


def test_csv_rejects_duplicate_headers(tmp_path):
    p = tmp_path / "report.csv"
    p.write_text("id,issue,Issue\n1,a,b\n", encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate column"):
        read_csv(p)


def test_csv_rejects_empty_report(tmp_path):
    p = tmp_path / "report.csv"
    p.write_text("id,issue\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no finding rows"):
        read_csv(p)


def test_csv_rejects_extra_columns(tmp_path):
    p = tmp_path / "report.csv"
    p.write_text("id,issue\n1,a,extra\n", encoding="utf-8")
    with pytest.raises(ValueError, match="more values"):
        read_csv(p)


def test_csv_normalizes_header_whitespace_and_case(tmp_path):
    p = tmp_path / "report.csv"
    p.write_text(" ID , ISSUE \nF-1,Missing title\n", encoding="utf-8")
    assert read_csv(p) == [{"id": "F-1", "issue": "Missing title"}]


def test_json_rejects_duplicate_object_keys(tmp_path):
    p = tmp_path / "report.json"
    p.write_text('[{"id":"A","id":"B"}]', encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate object key"):
        read_json(p)


def test_json_rejects_empty_findings(tmp_path):
    p = tmp_path / "report.json"
    p.write_text('{"findings":[]}', encoding="utf-8")
    with pytest.raises(ValueError, match="no findings"):
        read_json(p)


def test_json_rejects_nested_field_values(tmp_path):
    p = tmp_path / "report.json"
    p.write_text('[{"id":"A","metadata":{"source":"x"}}]', encoding="utf-8")
    with pytest.raises(ValueError, match="must be a scalar"):
        read_json(p)
