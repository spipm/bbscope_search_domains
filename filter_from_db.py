import sqlite3
import sys

from lib.filters import *
from config import TMP_DIR

options = {
  'ip':         'SELECT target from targets where is_ip = 1',
  'wildcard':   'SELECT target from targets where is_wildcard = 1',
  'url':        'SELECT target from targets where is_wildcard != 1 and is_ip != 1'
}

if len(sys.argv) < 2 or sys.argv[1] not in options:
  print("Usage: python3 filter_from_db.py <type: %s>" % ','.join(x for x in options))
  exit(0)

entrytype = sys.argv[1]

conn = sqlite3.connect(f"{TMP_DIR}/targets.db")
cursor = conn.cursor()

query = options[entrytype]
res = cursor.execute(query)

for record in res:
    record = record[0]
    record = record.strip()
    
    # filter out complicated to brute force (dns) records
    if record.count('*') > 1:
       continue
    if '*' in record and '*.' not in record:
       continue

    # Skip descriptive entries
    if '(' in record or ' ' in record or ',' in record:
      continue
    
    print(record)

conn.commit()
conn.close()
