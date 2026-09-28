import argparse
from datetime import date
from pathlib import Path
from .csv_reader import read_csv
from .json_reader import read_json
from .report import render_json, render_text
from .validators import validate_findings

def main():
    parser=argparse.ArgumentParser(description="Validate the completeness of an SEO audit report.")
    parser.add_argument("file"); parser.add_argument("--json",action="store_true"); parser.add_argument("--strict",action="store_true"); parser.add_argument("--today")
    args=parser.parse_args()
    try:
        rows=read_json(args.file) if Path(args.file).suffix.lower()==".json" else read_csv(args.file)
        today=date.fromisoformat(args.today) if args.today else date.today()
        findings=validate_findings(rows,today=today,strict=args.strict)
    except (OSError,ValueError,UnicodeError) as exc:
        parser.error(str(exc)); return 2
    print(render_json(findings) if args.json else render_text(findings))
    return 1 if any(f.issues or f.warnings for f in findings) else 0

if __name__=="__main__": raise SystemExit(main())
