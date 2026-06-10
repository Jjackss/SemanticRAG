# QUICKSTART: Getting Started Guide

## Step 1: Installation (5 minutes)

### Windows
```bash
git clone <repo-url>
cd SemanticRAG_v2
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### macOS / Linux
```bash
git clone <repo-url>
cd SemanticRAG_v2
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 2: Configuration (3 minutes)

### Prepare environment variables
```bash
cp .env.example .env
```

### Edit .env - Required Fields:

```ini
# Select your model
LLM_MODEL=mistral-large-latest

# Add your API Key
MISTRAL_API_KEY=your_key_here_from_https://console.mistral.ai
```

**Verify configuration:**
```bash
python scripts/check_api.py
```

You should see: OK

## Step 3: Prepare Manuals (2 minutes)

### Options:

**A) Use reference manuals (demonstration)**
```bash
# Already included
python scripts/build.py \
  --manual-id reference_8070 \
  --mode resume-compatible
```

**B) Add your own manuals**
```bash
# 1. Convert your PDF to text (.txt or .pdf)
# 2. Place in data/input/
# 3. Run:
python scripts/build.py \
  --source-chunks data/input/your_manual.txt \
  --manual-id my_manual \
  --mode resume-compatible
```

### Expected format:
The file should be plain text with related paragraphs. Example `my_manual.txt`:
```
Chapter 1: Introduction
The CNC 8070 system is...

Chapter 2: Installation
To install the system...
```

## Step 4: Run Build (5-30 minutes)

```bash
python scripts/build.py --manual-id my_manual --mode resume-compatible
```

### Real-time monitoring:
```bash
tail -f logs/semantic_rag.log
```

### Expected output:
```
OK Ingestion: 45 chunks extracted
OK Extraction: 1,230 triples generated
OK Canonicalization: 89 entity clusters resolved
OK Enrichment: 340 additional links created
OK Build complete: abox_linked.ttl ready
```

## Step 5: Query Results

### Option A: Interactive tool
```bash
python scripts/query.py

# Inside:
> SELECT ?entity ?label WHERE {
    ?entity rdf:type ?type .
    ?entity rdfs:label ?label .
  }
```

### Option B: Inspect generated files
```bash
# View final RDF graph
cat data/processed/abox_linked.ttl

# View build report
cat data/processed/build_report.json
```

## Step 6 (Optional): Publish to GraphDB

### Configure GraphDB

**Option 1: Local GraphDB with Docker**
```bash
docker run -d -p 7200:7200 khronus/graphdb:latest
```

**Option 2: Remote GraphDB**
```bash
# In .env, configure:
GRAPHDB_ENDPOINT=http://your-instance:7200
GRAPHDB_USERNAME=admin
GRAPHDB_PASSWORD=password
```

### Publish
```bash
python scripts/publish.py --enable-graphdb
```

Verify at: http://localhost:7200/sparql

## Common Use Cases

### Case 1: Add multiple manuals

```bash
# Create list file
cat > manuals_list.txt << EOF
data/input/manual1.txt|manual_1
data/input/manual2.txt|manual_2
data/input/manual3.txt|manual_3
EOF

# Process all
python scripts/build_batch.py --manuals-file manuals_list.txt
```

### Case 2: Resume interrupted build

```bash
# If the process was interrupted:
python scripts/build.py \
  --manual-id my_manual \
  --mode resume-compatible  # Reuse previous outputs
```

### Case 3: Clean and rebuild everything

```bash
python scripts/build.py \
  --manual-id my_manual \
  --mode force-all \
  --skip-cache
```

### Case 4: Evaluate quality

```bash
# If you have a golden dataset (QA pairs):
python scripts/evaluate.py \
  --qa-file data/golden_sets/my_qa_test.json \
  --output eval_report.json
```

## Common Issues

### "ModuleNotFoundError: No module named 'config'"
```bash
# Solution: Make sure you're in the root directory
cd SemanticRAG_v2
python scripts/build.py ...
```

### "API Key not found"
```bash
# Verify that .env exists
ls -la .env

# Verify content
grep MISTRAL_API_KEY .env
```

### "Connection refused" (GraphDB)
```bash
# Start GraphDB first
docker run -d -p 7200:7200 khronus/graphdb:latest
```

### Slow build
```bash
# In .env, reduce parallelism
BATCH_SIZE=2  # Default is 4
```

## Output Structure

After running `build.py`, you will see in `data/processed/`:

```
data/processed/
├── my_manual_abox_input.json           # Raw extraction (LLM)
├── my_manual_abox_generation_manifest.json  # Metadata
├── my_manual_merged.ttl                # Graph without consolidation
├── ontology_aligned.ttl                # T-Box (schema)
├── abox_canonical.ttl                  # Deduplicated data
├── abox_enriched.ttl                   # With enrichment
├── abox_linked.ttl                     # FINAL GRAPH
├── multilingual_lexicon.json           # Terms ES/EN
├── build_report.json                   # Statistics and metrics
└── canonicalization_report.json        # Deduplication details
```

**Important files:**
- `abox_linked.ttl` - Your final Knowledge Graph
- `build_report.json` - Metrics (entities, relations, etc.)
- `multilingual_lexicon.json` - Terms for search

## Next Steps

- **Full documentation**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Advanced configuration**: [docs/CONFIGURATION.md](docs/CONFIGURATION.md)
- **Troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

**Need help?** Check [FAQ](docs/FAQ.md) or open an issue.
