import csv
def read_csv(path):
    with open(path,newline="",encoding="utf-8-sig") as fh: return list(csv.DictReader(fh))
