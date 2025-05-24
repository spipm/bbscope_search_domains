#!/bin/bash

source .env
mkdir -p $TMP_DIR

echo "[+] Verwijderen van oude resultaten"
rm -f ${TMP_DIR}/*
rm -f $OUTPUT_FILE

echo "[+] Domains + download van arkadiyt (Github)"
curl -s https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/refs/heads/main/data/domains.txt > "${TMP_DIR}/domains"
echo "" >> "${TMP_DIR}/domains"

echo "[+] DB + Downloaden van bbscope (h1, it, bc)"
# Hackerone
./bins/bbscope h1 -b -t $H1_TOKEN -u spipm -c cidr >  "${TMP_DIR}/h1_bb_targets"
./bins/bbscope h1 -b -t $H1_TOKEN -u spipm -c url  >> "${TMP_DIR}/h1_bb_targets"
python3 add_targets_to_db.py "${TMP_DIR}/h1_bb_targets" h1

# Intigriti
./bins/bbscope it -b -t $IT_TOKEN -c cidr  >  "${TMP_DIR}/it_bb_targets"
./bins/bbscope it -b -t $IT_TOKEN -c url   >> "${TMP_DIR}/it_bb_targets"
python3 add_targets_to_db.py "${TMP_DIR}/it_bb_targets" it

# Bugcrowd throws cidrs in with urls and has a separate api section, which are also urls
# Bugcrowd causes a lot of noise
# ./bins/bbscope bc -b -c url -E "${BC_EMAIL}" -t $BC_TOKEN >  "${TMP_DIR}/bc_bb_targets"
# ./bins/bbscope bc -b -c api -E "${BC_EMAIL}" -t $BC_TOKEN >> "${TMP_DIR}/bc_bb_targets"
# python3 add_targets_to_db.py "${TMP_DIR}/bc_bb_targets" bc

echo "[+] Domains + Dump van domeinen uit URL's in database"
python3 filter_from_db.py url >> "${TMP_DIR}/domains"

echo "[+] Domains + Hostnames resolven van IP's met dnsx"
for range in $(python3 filter_from_db.py ip); do echo "$range" | ./bins/dnsx -silent -resp-only -ptr >> "${TMP_DIR}/domains"; done

echo "[+] DB + Toevoegen van wildcards van arkadiyt (Github)"
curl -s https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/refs/heads/main/data/domains.txt > "${TMP_DIR}/wildcards_extern"
echo "" >> "${TMP_DIR}/wildcards_extern"
python3 add_targets_to_db.py "${TMP_DIR}/wildcards_extern" arkadiyt

echo "[+] DB + Custom RD domains/wildcards"
python3 add_targets_to_db.py custom_rd_domains.txt custom

echo "[+] Sorteren van unieke wildcards"
python3 filter_from_db.py wildcard | awk '{FS="*";print $2}' | grep -v opera | grep -v 'qds-i' | sort -u > "${TMP_DIR}/uniq_wildcards.txt"

echo "[+] Domains + Subdomeinen uit wildcards met subfinder"
cat "${TMP_DIR}/uniq_wildcards.txt" | ./bins/subfinder -silent >> "${TMP_DIR}/domains"

echo "[+] Domains > Unieke domeinen filteren"
cat "${TMP_DIR}/domains" | python3 filter_bogus_domains.py | sort -u > "${TMP_DIR}/domains_uniq.txt"

echo "[+] Domains > Filteren van resolvable domeinen"
cat "${TMP_DIR}/domains_uniq.txt" | python3 filter_resolvable.py > "${OUTPUT_FILE}"

NUM_DOMAINS=$(wc -l < "${OUTPUT_FILE}")
echo "[✓] Klaar! ${NUM_DOMAINS} resolvable bug bounty domeinen in ${OUTPUT_FILE}"
