import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import dns.resolver

resolvers = [
    "1.1.1.1",
    "1.0.0.1",
    "94.140.14.14",
    "76.76.2.0",
    "9.9.9.9",
    "208.67.222.222",
    "84.116.46.23",
    "84.116.46.22",
]
batch_size = 100
resolve_sleep = 0.2
resolve_proc_num = len(resolvers)

def resolve_domain(domain):
    resolver_ip = random.choice(resolvers)
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [resolver_ip]
    resolver.lifetime = 1

    try:
        answer = resolver.resolve(domain, 'A')
        time.sleep(resolve_sleep)
        if answer:
            print(domain, flush=True)
    except Exception:
        pass

def process_batch(domains):
    with ThreadPoolExecutor(max_workers=resolve_proc_num) as executor:
        executor.map(resolve_domain, domains)

batch = []
for line in sys.stdin:
    domain = line.strip()
    if not domain:
        continue
    batch.append(domain)
    if len(batch) >= batch_size:
        process_batch(batch)
        batch = []
if batch:
    process_batch(batch)

