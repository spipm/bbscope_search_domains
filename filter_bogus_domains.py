import sys
from lib.filters import is_ip, is_valid_domain, is_wildcard, sanitize_value, should_deny

for line in sys.stdin:
   domain = line.strip()

   if is_ip(domain) or is_wildcard(domain):
      continue

   domain = sanitize_value(domain)
   if should_deny(domain) or not is_valid_domain(line):
      continue

   print(domain)

