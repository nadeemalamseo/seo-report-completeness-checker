# Limitations

This project checks report completeness, not SEO correctness.

It does not crawl websites, call Google or other APIs, verify live HTTP responses, resolve DNS, follow redirects, decide whether an SEO recommendation is effective, predict rankings or traffic, guarantee indexing or search visibility, or use an LLM to judge evidence quality.

URL validation checks syntax only and cannot establish reachability, ownership, canonicalization, HTTP status, or whether a URL is the correct affected page.

WEAK_EVIDENCE and WEAK_RECOMMENDATION are deterministic heuristics, not expert judgments. A report can pass the checker while containing inaccurate evidence or poor SEO advice. A non-empty report is required; a successful exit code means only that the implemented completeness checks found no issues or warnings.