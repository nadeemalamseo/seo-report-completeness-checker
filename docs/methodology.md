# Methodology

The checker validates report structure and internal field consistency. It does not crawl URLs or determine whether an SEO recommendation is correct.

## Input handling

CSV headers are trimmed and matched case-insensitively. Empty headers, duplicate headers, rows with more values than columns, and header-only CSV files are rejected. JSON may be a top-level array or an object containing a findings or rows array. Duplicate JSON object keys, empty reports, non-object finding rows, and nested object/array field values are rejected to avoid ambiguous interpretation.

## Required fields and values

Every finding requires id, issue, affected_url, evidence, impact, priority, recommendation, and implementation_status.

Impact values: LOW, MEDIUM, HIGH, CRITICAL. Priority values: LOW, MEDIUM, HIGH, CRITICAL, or 1–4. Numeric priority ordering is not inferred by the checker; teams should document their own convention. Status values: OPEN, IN_PROGRESS, BLOCKED, READY_FOR_VERIFICATION, VERIFIED, WONT_FIX.

## URL syntax

Affected URLs must use HTTP or HTTPS, contain a valid hostname or IP literal, have no embedded user credentials or whitespace, and use a valid port when specified. This is syntax validation only. The checker does not resolve DNS, make HTTP requests, follow redirects, or establish that the URL is publicly reachable.

## Verification and dates

Verification evidence is required for READY_FOR_VERIFICATION and VERIFIED findings. VERIFIED findings also require an ISO-8601 calendar date in verification_date; future verification dates are rejected. A verification date on a status other than VERIFIED or WONT_FIX produces a status conflict warning. Due dates use ISO-8601 calendar dates. Overdue findings are warnings unless strict mode is enabled, and VERIFIED/WONT_FIX findings are not marked overdue.

## Duplicate and weak-content checks

Duplicate IDs and duplicate normalized issue/URL pairs are reported. Text normalization collapses whitespace and compares duplicate keys case-insensitively. Generic evidence and recommendation phrases are flagged by a small deterministic heuristic; this does not assess factual accuracy, sufficiency, or strategic quality.

## Strict mode and reproducibility

The checker is deterministic for the same input and reference date. Supply --today YYYY-MM-DD to make due-date and future-verification checks reproducible. --strict promotes warnings to errors. Exit code 0 means no completeness issues or warnings were found in the supplied non-empty report; it does not mean the SEO audit itself is correct.