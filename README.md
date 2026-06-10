# SemanticRAG: Knowledge Graph Construction from Technical Manuals

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

**SemanticRAG** is a modular framework for constructing **operational and queryable Knowledge Graphs** from technical manuals. It automates ingestion, semantic extraction, consolidation, and publication of RDF graphs with multilingual support and automatic evaluation.

## Key Features

- **Automatic Ingestion**: Processes PDFs and technical documents into chunks
- **Semantic Extraction**: Automatically generates A-Box (data) and T-Box (schema)
- **Intelligent Consolidation**: Deduplication, enrichment, and entity resolution
- **Multilingual Support**: Automatic lexicalization in multiple languages
- **GraphDB Integration**: Direct integration with GraphDB (RDF4J)
- **Formal Evaluation**: Golden datasets and quality metrics
- **AAS Projection**: Deterministic projection to AAS models (Asset Administration Shell)

## Prerequisites

- **Python 3.10+**
- **Git**
- API keys for:
  - **Mistral AI** (primary) or **Qwen** (alternative)
  - **GraphDB** (optional, for publication)

## Quick Start (5 minutes)

### 1. Clone and Setup

```bash
git clone <repo-url>
cd SemanticRAG_v2
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your credentials
```

Required fields:
- `MISTRAL_API_KEY` - Your Mistral API key
- `LLM_MODEL` - Model to use: `mistral-large-latest` or `qwen-2.5-32b`
- `GRAPHDB_ENDPOINT` (optional) - Your GraphDB instance URL
- `GRAPHDB_USERNAME` (optional) - GraphDB credentials

### 3. Prepare Manuals

Place your processed documents in `data/input/`:

```bash
# Format: chunks file (raw text)
# Example structure:
data/input/
├── my_manual_chunks.txt
└── another_documentation.txt
```

### 4. Run Build

```bash
# Full Knowledge Graph build
python scripts/build.py --manual-id my_manual

# Or with resume mode (recommended)
python scripts/build.py --manual-id my_manual --mode resume-compatible
```

### 5. Query Results

```bash
# Interactive query tool
python scripts/query.py

# Publish to GraphDB (if configured)
python scripts/publish.py
```

## Documentation

| Document | Content |
|----------|---------|
| [QUICKSTART.md](QUICKSTART.md) | Detailed getting started guide |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Components and pipeline description |
| [DATA_PIPELINE.md](docs/DATA_PIPELINE.md) | Data flow details |
| [CONFIGURATION.md](docs/CONFIGURATION.md) | Advanced configuration options |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contributing guidelines |

## Project Structure

```
SemanticRAG_v2/
├── config/                  # Centralized configuration
│   ├── settings.py         # Global settings
│   ├── llm_config.py       # LLM model setup
│   └── graphdb_config.py   # GraphDB configuration
│
├── core/                    # Reusable code
│   ├── ingestion/          # Manual reading and processing
│   ├── extraction/         # RDF triple extraction
│   ├── retrieval/          # Retrieval and evaluation
│   ├── database/           # Persistence (local RDF and GraphDB)
│   └── aas_projection/     # AAS model projection
│
├── scripts/                 # Entry points
│   ├── build.py            # Main build script
│   ├── build_with_manual.py# Manual onboarding
│   ├── publish.py          # GraphDB publication
│   ├── query.py            # Interactive querying
│   └── check_api.py        # API usage verification
│
├── data/
│   ├── input/              # Place your manuals here
│   ├── processed/          # Generated artifacts
│   └── golden_sets/        # Validation datasets
│
└── reference_project/      # Reference project (Broaching CNC-8070)
    ├── config/             # Project-specific configuration
    └── data/               # Sample manuals and golden sets
```

## Core Concepts

### T-Box (Schema)
- **Terminological Box**: Defines concepts and relationships
- Automatically generated from manuals
- Consolidated in `ontology_aligned.ttl`

### A-Box (Data)
- **Assertional Box**: Specific extracted instances
- Main artifacts:
  - `abox_input.json` - Raw extraction
  - `abox_canonical.ttl` - After deduplication
  - `abox_enriched.ttl` - With automatic enrichment
  - `abox_linked.ttl` - Final operational graph

### Processing Pipeline
```
Manuals (PDF/TXT)
    ↓
Ingestion & Chunking
    ↓
A-Box Extraction (LLM)
    ↓
Merge & Consolidation
    ↓
Canonicalization (Deduplication)
    ↓
Enrichment (Linking)
    ↓
Validation & Evaluation
    ↓
Publication (GraphDB / RDF)
```

## Advanced Configuration

### Change LLM Model

```bash
# In .env:
LLM_MODEL=mistral-large-latest       # Mistral
# or
LLM_MODEL=qwen-2.5-32b                # Qwen
```

### Use Remote GraphDB

```bash
python scripts/publish.py \
  --graphdb-endpoint http://your-graphdb:7200 \
  --graphdb-username admin \
  --graphdb-password password
```

### Execution Modes

```bash
# resume-compatible: Reuse previous outputs (recommended)
python scripts/build.py --mode resume-compatible

# force-stale: Recalculate some steps
python scripts/build.py --mode force-stale

# force-all: Recalculate everything (slow)
python scripts/build.py --mode force-all
```

## Monitoring and Evaluation

```bash
# Evaluate against golden dataset
python scripts/evaluate.py \
  --qa-file data/golden_sets/my_qa_dataset.json

# Generate health report
python scripts/check_api.py  # API usage
```

## Troubleshooting

### "API Key not found"
Verify that `.env` exists and contains `MISTRAL_API_KEY`

### "GraphDB connection failed"
If using local GraphDB, start the server first:
```bash
docker run -d -p 7200:7200 khronus/graphdb:latest
```

### Slow build
Adjust `BATCH_SIZE` in `.env` (lower values = less parallelism)

See [full troubleshooting guide](docs/TROUBLESHOOTING.md) for more.

## Usage Examples

### Example 1: Add a new manual

```bash
# 1. Process your PDF to chunks (plain text)
# 2. Save in data/input/my_chunks.txt
# 3. Run:
python scripts/build_with_manual.py \
  --source-chunks data/input/my_chunks.txt \
  --manual-id my_new_manual
```

### Example 2: Interactive querying

```bash
python scripts/query.py

# Inside the REPL:
> SELECT ?label WHERE { ?s rdf:type ?type . ?s rdfs:label ?label . }
> SPARQL QUERY EXECUTED
> Results: 1200 entities
```

### Example 3: Evaluate against Golden Set

```bash
python scripts/evaluate.py \
  --qa-file data/golden_sets/QA_my_domain.json \
  --output eval_results.json
```

## Support

- **Documentation**: See `/docs`
- **Issues**: Open an issue in the repository
- **Questions**: Check the [FAQ](docs/FAQ.md)

## License

MIT License - See [LICENSE](LICENSE) for details.

## Acknowledgments

Based on research in Knowledge Graphs, Semantic Web, and LLM-driven extraction. Maintains compatibility with reference projects in specific domains.

---

**Ready to get started?** See [QUICKSTART.md](QUICKSTART.md)
