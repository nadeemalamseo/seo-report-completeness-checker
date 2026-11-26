# Input schema

## Required fields

Every finding must contain:

- id
- issue
- affected_url
- evidence
- impact
- priority
- recommendation
- implementation_status

## Conditional and optional fields

- verification is required when status is READY_FOR_VERIFICATION or VERIFIED.
- verification_date is required when status is VERIFIED; it must be an ISO-8601 calendar date and cannot be in the future relative to the reference date.
- Optional fields: category, owner, due_date, implementation_notes, verification_date, source.

## Accepted values

- Impact: LOW, MEDIUM, HIGH, CRITICAL.
- Priority: LOW, MEDIUM, HIGH, CRITICAL, or 1–4. Numeric ordering is defined by the team using the report.
- Implementation status: OPEN, IN_PROGRESS, BLOCKED, READY_FOR_VERIFICATION, VERIFIED, WONT_FIX.

## CSV

Use one finding per row, a single header row, unique non-empty column names, and the required field names. Headers are trimmed and case-insensitive. Blank optional cells are allowed.

## JSON

Use a top-level array of finding objects, or an object with a findings or rows array. Each field value must be a scalar (string, number, boolean, or null). Duplicate object keys and empty arrays are rejected.