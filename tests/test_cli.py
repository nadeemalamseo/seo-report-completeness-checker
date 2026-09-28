import json
def test_json_reader_and_output(tmp_path,monkeypatch,capsys):
    from seo_report_checker.cli import main
    p=tmp_path/"report.json"
    p.write_text(json.dumps([{"id":"F-1","issue":"Missing title","affected_url":"https://example.com/a","evidence":"Title element is absent.","impact":"HIGH","priority":"HIGH","recommendation":"Add a unique title.","implementation_status":"OPEN","verification":""}]),encoding="utf-8")
    monkeypatch.setattr("sys.argv",["seo-report-check",str(p),"--json"])
    assert main()==0
    assert "summary" in capsys.readouterr().out
