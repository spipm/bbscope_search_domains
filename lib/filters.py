import re
import ipaddress

denylist = [
  'NO_IN_SCOPE_TABLE',
  'yoursubdomain',
  'username',
  'your-own-1password-account'
  'play.google.com',
  'apps.apple.com',
  'itunes.apple.com',
  'marketplace.atlassian.com',
  'github.com',
  'addons',
  '{', '}',
  'www.sophos.com',
   "qds-i.net",
   "_dmarc",
   "opera",
   "--",
   "akamaitechnologies",
   "fiservapps",
   "fiservapis",
   "autodiscover",
   "clarivate",
   "compumark",
   "omnipaytest",
   "fiservmobileapps"
  ]

# Values to replace with ''
replacelist = [
  'http://',
  'https://'
]

# validates a.b or a.b.c, not http://
def is_valid_domain(s):
  pattern = r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
  return re.match(pattern, s) is not None

# if it is an ip or cidr
def is_ip(line):
  try:
    line = ipaddress.ip_network(line, strict=False)
    return True
  except ValueError as e:
    return False

def is_wildcard(line):
  if '*' in line:
    return True
  return False

def should_deny(line):
  if 'your' and 'domain' in line:
    return True
  for d in denylist:
    if d in line:
      return True
  return False

# Replace values like http:// and https:// with ''
# Also remove any http url paths
def sanitize_value(line):
  line = line.strip()

  for replace_value in replacelist:
    if replace_value in line:
      line = line.replace(replace_value, '')
  
  if '/' in line:
    line = line.split('/')[0]

  return line

