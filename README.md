# SEO Report Completeness Checker

Validate SEO audit reports for complete evidence, actionable recommendations, implementation status, and verification records.

## What it does

This deterministic, local-first CLI checks an existing SEO audit report rather than crawling a website. It asks whether each finding is documented well enough to be assigned, implemented, tracked, and verified. It does **not** determine whether an SEO recommendation is correct or whether it will improve rankings.

## Install

Python 3.10+:

    python -m pip install -e .
    python -m pip install -e ".[test]"

## Usage

    seo-report-check examples/complete-report.csv
    seo-report-check examples/incomplete-report.csv --json
    seo-report-check examples/incomplete-report.csv --strict --today 2026-11-27
    seo-report-check path/to/report.json

Only .csv and .json input files are accepted. Empty reports are rejected rather than treated as successful audits.

Exit codes: 0 = no completeness issues or warnings; 1 = findings have issues or warnings; 2 = invalid input or report format.

## Required fields

Every finding requires: id, issue, affected_url, evidence, impact, priority, recommendation, implementation_status.

Verification evidence is required for READY_FOR_VERIFICATION and VERIFIED. VERIFIED findings also require an ISO verification_date that is not in the future relative to the selected reference date.

Impact values: LOW, MEDIUM, HIGH, CRITICAL. Priority values: LOW, MEDIUM, HIGH, CRITICAL, or 1–4. Numeric priority ordering is not inferred; teams should document their convention. Status values: OPEN, IN_PROGRESS, BLOCKED, READY_FOR_VERIFICATION, VERIFIED, WONT_FIX.

See docs/input-schema.md for accepted values and CSV/JSON structure.

## Checks

The checker detects missing required fields, malformed URLs, unsupported impact/priority/status values, duplicate IDs/findings, weak generic evidence or recommendations, verification/status inconsistencies, invalid dates, future verification dates, and overdue actions. Warnings can be promoted to errors with --strict.

## Scope and limitations

This project evaluates **report completeness and internal consistency**. It does not crawl websites, call search-engine APIs, verify live HTTP responses, assess whether a recommendation is strategically correct, predict rankings or traffic, or guarantee indexing or search visibility.

URL validation is syntactic only. A syntactically valid URL may still be unreachable, redirect, return an error, or point to the wrong page. Weak evidence/recommendation checks are deterministic heuristics, not expert or AI judgments.

## MarketLatch

For a broader SEO reporting workflow, see the [MarketLatch SEO Report Template](https://marketlatch.com/seo-report-template/?utm_source=github&utm_medium=referral&utm_campaign=github_seo_report_completeness_checker).

## Project links

- [Project landing page](https://nadeemalamseo.github.io/seo-report-completeness-checker/)
- [Latest source ZIP](https://github.com/nadeemalamseo/seo-report-completeness-checker/archive/refs/heads/main.zip)
- [Historical v0.1.0 release](https://github.com/nadeemalamseo/seo-report-completeness-checker/releases/tag/v0.1.0)

## License

This repository is licensed under the MIT License. See LICENSE.