# SemanticRAG Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                 INPUT: Technical Manuals                    │
│                  (PDF, TXT, Markdown, etc.)                 │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────▼──────────────┐
         │  1. INGESTION & CHUNKING │
         │   (core/ingestion)       │
         └───────────┬──────────────┘
                     │
         ┌───────────▼──────────────────────┐
         │  2. SEMANTIC EXTRACTION (LLM)    │
         │   - T-Box (Schema/Ontology)      │
         │   - A-Box (Entities/Relations)   │
         │   (core/extraction)              │
         └───────────┬──────────────────────┘
                     │
         ┌───────────▼──────────────────────┐
         │  3. CONSOLIDATION                │
         │   - Deduplication (Entities)     │
         │   - Canonicalization             │
         │   - Link Resolution              │
         └───────────┬──────────────────────┘
                     │
         ┌───────────▼──────────────────────┐
         │  4. ENRICHMENT & VALIDATION      │
         │   - Multilinguality (EN)         │
         │   - AAS Projection               │
         │   - Quality Metrics              │
         │   (core/retrieval)               │
         └───────────┬──────────────────────┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
   RDF Local    GraphDB Remote   Golden Sets
   (RDF/TTL)    (Publication)     (Evaluation)
      └──────────────┬──────────────┘
                     │
         ┌───────────▼──────────────┐
         │      KNOWLEDGE GRAPH     │
         │   Ready for Retrieval    │
         │   and Application        │
         └──────────────────────────┘
```

## Core Components

### 1. **core/ingestion** - Document Ingestion
**Responsibility**: Reading and preparing manuals

```python
ingestion/
├── document_loader.py      # Load PDF, TXT, etc.
├── chunker.py              # Fragment into semantic chunks
├── density_analyzer.py     # Information density analysis
└── language_detector.py    # Language detection
```

**Input**: `data/input/*.txt` or `*.pdf`
**Output**: Structured chunks in JSON

### 2. **core/extraction** - Semantic Extraction
**Responsibility**: RDF generation (T-Box + A-Box) using LLM

```python
extraction/
├── abox_extractor.py       # Generate RDF triples for instances
├── abox_input_builder.py   # Prepare LLM input
├── abox_semantic_validator.py  # Validate RDF semantics
├── tbox_enrichment_auditor.py  # Audit schema
└── prompts/
    ├── abox_extraction_prompts.json
    └── tbox_generation_prompts.json
```

**Input**: Chunks + Prompts
**Output**: 
- `abox_input.json` - Raw extraction
- RDF triples in N-Triples format

### 3. **core/retrieval** - Retrieval and Evaluation
**Responsibility**: Queries, evaluation, and semantic search

```python
retrieval/
├── query_engine.py         # SPARQL engine
├── qa_evaluator.py         # Evaluation against golden sets
├── multilingual_normalizer.py  # EN normalization
├── synthesis_pipeline.py   # Answer synthesis
└── text_to_sparql.py       # Text to SPARQL conversion
```

**Input**: Knowledge Graph + Queries
**Output**: SPARQL results, evaluation metrics

### 4. **core/database** - Persistence
**Responsibility**: Storage and publication

```python
database/
├── local_rdf_store.py      # Local RDF storage (rdflib)
├── graphdb_publisher.py    # GraphDB publication
├── query_federation.py     # Federated queries
└── health_checker.py       # Graph health
```

**Input**: Consolidated graph
**Output**: Remote GraphDB / Local RDF

### 5. **core/aas_projection** - AAS (Asset Administration Shell)
**Responsibility**: Projection to AAS models (optional)

```python
aas_projection/
├── aas_mapper.py           # RDF to AAS mapping
├── aas_validator.py        # AAS validation
└── aas_exporter.py         # Export to AAS formats
```

**Input**: Consolidated RDF
**Output**: AAS models (JSON, XML)

## Centralized Configuration

### **config/settings.py** - Global Settings
```python
class Settings:
    llm_model: str           # mistral-large-latest, qwen-2.5-32b
    api_key: str             # from .env
    batch_size: int          # Parallelism (1-64)
    retry_profile: str       # Retry policy
    enable_multilingual: bool
    enable_aas_projection: bool
    graphdb_endpoint: str | None
```

### **config/llm_config.py** - LLM Configuration
```python
class LLMConfig:
    model_name: str
    api_provider: str        # "mistral", "qwen", etc.
    temperature: float       # 0.0-1.0 (determinism vs creativity)
    max_tokens: int          # Output limit
    retry_policy: RetryPolicy
```

### **config/graphdb_config.py** - GraphDB
```python
class GraphDBConfig:
    endpoint: str            # http://localhost:7200
    repository: str          # default
    username: str
    password: str
    ssl_verify: bool
```

## Detailed Data Flow

### Phase 1: Ingestion
```
Manual PDF/TXT
    ↓
document_loader.load()
    ↓
Raw text
    ↓
chunker.chunk_by_semantics()
    ↓
chunks[]: {text: str, metadata: {...}}
```

### Phase 2: Extraction (LLM)
```
chunks[] + extraction_prompts
    ↓
LLM API Call (Mistral/Qwen)
    ↓
Raw RDF output (turtle/n-triples)
    ↓
abox_semantic_validator.validate()
    ↓
abox_input.json
```

### Phase 3: Consolidation
```
abox_input.json + ontology_schema.ttl
    ↓
abox_merger.merge()  # Combine all A-Boxes
    ↓
abox_merged.ttl
    ↓
abox_canonicalizer.canonicalize()  # Dedup entities
    ↓
entity_clusters: {canonical_uri: [alternative_uris]}
    ↓
abox_canonical.ttl
```

### Phase 4: Enrichment
```
abox_canonical.ttl
    ↓
abox_graph_enricher.enrich()  # Add extra links
    ↓
abox_enriched.ttl
    ↓
multilingual_lexicon_builder.build()
    ↓
multilingual_lexicon.json
```

### Phase 5: Publication
```
abox_linked.ttl + multilingual_lexicon.json
    ↓
graphdb_publisher.publish() [optional]
    ↓
Named graphs in GraphDB
    OR
    ↓
abox_linked.ttl (local RDF file)
```

## Entry Point Scripts

### `scripts/build.py` - Main Build
```bash
python scripts/build.py \
  --manual-id my_manual \
  --source-chunks data/input/manual.txt \
  --mode resume-compatible \
  --skip-publish
```

**Orchestration**:
1. `core.ingestion.document_loader.load()`
2. `core.extraction.abox_input_builder.build()`
3. `core.extraction.abox_extractor.extract()` ← LLM call
4. `core.extraction.abox_merger.merge()`
5. `core.extraction.abox_canonicalizer.canonicalize()`
6. `core.extraction.abox_graph_enricher.enrich()`
7. `core.retrieval.qa_evaluator.evaluate()` [if golden set available]
8. `core.database.graphdb_publisher.publish()` [if enabled]

### `scripts/query.py` - Interactive Queries
```bash
python scripts/query.py

# Interactive REPL
> SELECT ?entity WHERE { ?entity rdf:type ?type }
```

### `scripts/evaluate.py` - Evaluation
```bash
python scripts/evaluate.py \
  --qa-file data/golden_sets/qa_test.json \
  --output report.json
```

### `scripts/publish.py` - GraphDB Publication
```bash
python scripts/publish.py \
  --graphdb-endpoint http://localhost:7200 \
  --repository my_graph
```

## Generated Artifacts

| File | Content | Consumer |
|------|---------|----------|
| `abox_input.json` | Raw extraction (LLM) | Merger |
| `ontology_aligned.ttl` | Final T-Box | Query engine |
| `abox_canonical.ttl` | Deduplicated A-Box | Enricher |
| `abox_enriched.ttl` | Enriched A-Box | Link completer |
| `abox_linked.ttl` | **FINAL GRAPH** | Publication / Queries |
| `multilingual_lexicon.json` | EN terms | Query normalizer |
| `build_report.json` | Metrics | Reports |
| `canonicalization_report.json` | Dedup details | Audit |

## LLM Model Selection

### In `.env`:
```ini
# Option 1: Mistral (recommended - fast and accurate)
LLM_MODEL=mistral-large-latest
MISTRAL_API_KEY=...

# Option 2: Qwen (alternative)
LLM_MODEL=qwen-2.5-32b
QWEN_API_KEY=...
```

### Change at runtime:
```python
from config.llm_config import LLMConfig

config = LLMConfig.from_env()
config.model_name = "qwen-2.5-32b"
```

## Execution Modes

| Mode | Behavior | When to use |
|------|----------|------------|
| `resume-compatible` | Reuse previous outputs (recommended) | Always (faster) |
| `force-stale` | Recalculate some steps | Minor adjustments |
| `force-all` | Recalculate everything from scratch | Clean build |

## Debugging and Logs

```bash
# View logs in real-time
tail -f logs/semantic_rag.log

# Increase detail level
# In .env:
LOG_LEVEL=DEBUG

# View build statistics
cat data/processed/build_report.json | jq '.statistics'
```

---

**For more details on configuration**: See [docs/CONFIGURATION.md](docs/CONFIGURATION.md)
