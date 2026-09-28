# Methodology

The checker validates report structure and internal field consistency. It does not crawl URLs or determine whether an SEO recommendation is correct.

A finding is complete when required fields are present, enumerated fields use supported values, the URL is syntactically valid, and status/verification relationships are consistent.

Warnings identify generic evidence or recommendations and overdue actions. `--strict` promotes warnings to failures.

The validator is deterministic: the same input and reference date produce the same result.
