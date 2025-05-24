
### Usage

1. Create an .env file
```
TMP_DIR=./tmp
H1_TOKEN=
IT_TOKEN=
BC_TOKEN=
BC_EMAIL=
OUTPUT_FILE=resolvable_targets.txt
```
(fill in your tokens)

2. Check `search_domains.sh`, uncomment Bugcrowd lines if you want

3. Start a venv and install requirements

f4. Run ./search_domains.sh

### Warning

Filtering wildcards is a challenge, and this script might yield results that are out of scope.
