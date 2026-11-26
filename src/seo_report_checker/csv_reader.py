import csv


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh, strict=True)
        headers = reader.fieldnames
        if not headers:
            raise ValueError("CSV is empty or has no header row.")
        normalized = [str(header or "").strip().casefold() for header in headers]
        if any(not header for header in normalized):
            raise ValueError("CSV contains an empty column name.")
        if len(normalized) != len(set(normalized)):
            raise ValueError("CSV contains duplicate column headers.")
        reader.fieldnames = normalized
        rows = []
        for line_number, row in enumerate(reader, start=2):
            if None in row:
                raise ValueError(f"CSV row {line_number} has more values than the header.")
            rows.append(row)
        if not rows:
            raise ValueError("CSV contains a header but no finding rows.")
        return rows
