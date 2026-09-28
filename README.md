# SEO Report Completeness Checker

Validate SEO audit reports for complete evidence, actionable recommendations, implementation status, and verification fields.

## What it does

This deterministic, local-first CLI checks an existing SEO audit report rather than crawling a website.

It answers:

> Is each audit finding structurally complete enough to be acted on, tracked, and verified?

It does **not** determine whether an SEO recommendation is correct or whether it will improve rankings.

## Workflow

```
Existing SEO audit
       |
       v
CSV / JSON report
       |
       v
Completeness checker
       |
       v
Missing / inconsistent fields
       |
       v
Action-ready report
```

## Install

Python 3.10+:

```bash
python -m pip install -e .
```

For development:

```bash
python -m pip install -e ".[test]"
```

## Usage

```bash
seo-report-check examples/complete-report.csv
seo-report-check examples/incomplete-report.csv --json
seo-report-check examples/incomplete-report.csv --strict --today 2026-09-29
```

Exit codes:

- `0` — no completeness findings
- `1` — findings or warnings were detected
- `2` — invalid input

## Required fields

`id`, `issue`, `affected_url`, `evidence`, `impact`, `priority`, `recommendation`, `implementation_status`.

`verification` is conditionally required when `implementation_status` is `READY_FOR_VERIFICATION` or `VERIFIED`.

Optional fields include `category`, `owner`, `due_date`, `implementation_notes`, `verification_date`, and `source`.

## Checks

The checker detects missing required fields, malformed URLs, unsupported impact/priority/status values, duplicate IDs/findings, weak generic evidence or recommendations, verification/status inconsistencies, invalid due dates, and overdue actions.

Warnings can be promoted to failures with `--strict`.

## Scope and limitations

This project evaluates **report completeness and internal consistency**. It does not crawl websites, call search-engine APIs, verify live HTTP responses, assess whether a recommendation is strategically correct, predict rankings or traffic, or guarantee indexing or search visibility.

Weak evidence/recommendation checks are deterministic heuristics, not expert or AI judgments.

## MarketLatch

For a broader SEO reporting workflow, see the [MarketLatch SEO Report Template](https://marketlatch.com/seo-report-template/?utm_source=github&utm_medium=referral&utm_campaign=github_seo_report_completeness_checker).

## Project links

- [Project landing page](https://nadeemalamseo.github.io/seo-report-completeness-checker/)
- [v0.1.0 release](https://github.com/nadeemalamseo/seo-report-completeness-checker/releases/tag/v0.1.0)
- [Download v0.1.0 ZIP](https://github.com/nadeemalamseo/seo-report-completeness-checker/archive/refs/tags/v0.1.0.zip)

## License

This repository is licensed under the MIT License. See [LICENSE](LICENSE).
