# Input schema

Required fields: `id`, `issue`, `affected_url`, `evidence`, `impact`, `priority`, `recommendation`, `implementation_status`.

Optional fields: `verification`, `category`, `owner`, `due_date`, `implementation_notes`, `verification_date`, `source`.

Verification is required when `implementation_status` is `READY_FOR_VERIFICATION` or `VERIFIED`.

Impact values: LOW, MEDIUM, HIGH, CRITICAL.

Priority values: LOW, MEDIUM, HIGH, CRITICAL, or 1-4.

Implementation statuses: OPEN, IN_PROGRESS, BLOCKED, READY_FOR_VERIFICATION, VERIFIED, WONT_FIX.
