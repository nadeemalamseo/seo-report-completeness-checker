import json
from .validators import summary

def payload(findings):
    return {"summary":summary(findings),"findings":[{"row":f.row_number,"id":f.finding_id,"status":"INCOMPLETE" if f.issues or f.warnings else "COMPLETE","issues":f.issues,"warnings":f.warnings} for f in findings]}

def render_text(findings):
    p=payload(findings); s=p["summary"]
    lines=["SEO REPORT COMPLETENESS CHECK","=============================","",f"Total findings: {s['total_findings']}",f"Complete: {s['complete']}",f"Incomplete: {s['incomplete']}",f"Errors: {s['errors']}",f"Warnings: {s['warnings']}"]
    for x in p["findings"]:
        if x["status"]=="INCOMPLETE":
            lines += ["",f"ROW-{x['row']} {x['id']}".strip(),"Status: INCOMPLETE"]
            if x["issues"]: lines.append("Problems: "+", ".join(x["issues"]))
            if x["warnings"]: lines.append("Warnings: "+", ".join(x["warnings"]))
    return "\n".join(lines)

def render_json(findings): return json.dumps(payload(findings),indent=2,sort_keys=True)
