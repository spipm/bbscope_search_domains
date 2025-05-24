import sqlite3
import sys

from lib.filters import *
from config import TMP_DIR

if len(sys.argv) < 3:
  print("Usage: python3 filter_targets.py <file> <platform>")
  exit(0)

fin       = sys.argv[1]
platform  = sys.argv[2]

with open(fin) as f:
    lines = [line.strip() for line in f]

conn = sqlite3.connect(f"{TMP_DIR}/targets.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target TEXT,
    platform TEXT,
    is_ip INTEGER,
    is_wildcard INTEGER
)
""")

for line in lines:

  if is_ip(line):
    cursor.execute("""
          INSERT INTO targets (target, platform, is_ip, is_wildcard)
          VALUES              (?, ?, ?, ?)
    """,  [line, platform, 1, is_wildcard(line)])
    continue

  line = sanitize_value(line)
  if should_deny(line):
    continue
  
  if not is_wildcard(line) and not is_valid_domain(line):
    continue

  cursor.execute("""
        INSERT INTO targets (target, platform, is_ip, is_wildcard)
        VALUES              (?, ?, ?, ?)
  """,  [line, platform, 0, is_wildcard(line)])


conn.commit()
conn.close()