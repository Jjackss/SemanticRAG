# reference_project/ - Reference Project

This directory contains the **reference project** (Broaching CNC-8070) that demonstrates how to use SemanticRAG with real technical manuals.

## Structure

```
reference_project/
├── README.md              # This file
├── config/
│   ├── project_scope.json          # Project definition
│   ├── aas_profile.json            # AAS profile
│   ├── aas_rules.json              # Projection rules
│   └── aas_semantic_id_map.json    # Semantic ID mapping
└── data/
    ├── raw/
    │   ├── chunks_manual_a218.txt
    │   ├── chunks_8070_quick_ref.txt
    │   ├── chunks_8070_installation_manual.txt
    │   └── chunks_8070_error_manual.txt
    └── golden_set/
        ├── QA_bilingual.json
        ├── QA_8070_quick_ref_bilingual.json
        ├── QA_chunks_8070_installation_manual.json
        └── QA_chunks_8070_error_manual.json
```

## Purpose

1. **Demonstration**: Shows how SemanticRAG works with real data
2. **Testing**: Provides golden sets to validate quality
3. **Reference**: Example configuration for AAS
4. **Reproducibility**: Allows rebuilding the reference runtime

## Use the Reference Project

### Option 1: Full Build
```bash
# Rebuild the reference Knowledge Graph
python scripts/build.py \
  --manual-id reference_8070 \
  --mode resume-compatible
```

### Option 2: Process a Specific Manual
```bash
# Process only the installation manual
python scripts/build.py \
  --source-chunks reference_project/data/raw/chunks_8070_installation_manual.txt \
  --manual-id 8070_installation
```

### Option 3: Evaluate Against Golden Set
```bash
# Evaluate quality against the golden dataset
python scripts/evaluate.py \
  --qa-file reference_project/data/golden_set/QA_bilingual.json
```

## Reference Statistics

### Included Manuals
| Manual | Size | Entities | Relations | Language |
|--------|------|----------|-----------|----------|
| A218 Broaching | 25 KB | ~450 | ~280 | EN |
| 8070 Quick Ref | 18 KB | ~320 | ~150 | EN |
| 8070 Installation | 42 KB | ~780 | ~520 | EN |
| 8070 Error Manual | 35 KB | ~610 | ~380 | EN |

### Expected Output
```
OK T-Box Entities: 850
OK A-Box Instances: 2,160
OK Relations: 1,330
OK Multilingual Terms: 3,400
OK Deduplication Ratio: 87%
```

## Project Configuration

### `project_scope.json`
Defines the project scope and limits:
```json
{
  "project_name": "Broaching CNC-8070",
  "domain": "Manufacturing",
  "equipment_type": "CNC Broacher",
  "manual_ids": ["a218", "8070_quick_ref", "8070_installation", "man_8070_err"],
  "supported_languages": ["en"]
}
```

### `aas_profile.json`
AAS profile for projection:
```json
{
  "aas_version": "3.0",
  "company": "Reference",
  "profile_name": "CNC-8070-AAS",
  "submodel_profiles": [...]
}
```

## Golden Sets

Golden sets are **validation datasets** with Q&A pairs:

```json
[
  {
    "question": "What is the installation process for the 8070?",
    "expected_answer": "Follow the procedure in chapter 2...",
    "manual_id": "8070_installation",
    "difficulty": "easy",
    "language": "en"
  },
  ...
]
```

### Use Golden Sets

```bash
# Evaluate model against golden set
python scripts/evaluate.py \
  --qa-file reference_project/data/golden_set/QA_bilingual.json \
  --output eval_results.json

# View results
cat eval_results.json | jq '.metrics'
```

## Typical Workflow

```
1. git clone <repo>
2. cp .env.example .env
3. Edit .env with your API key
4. python scripts/build.py --manual-id reference_8070
5. python scripts/evaluate.py --qa-file reference_project/data/golden_set/QA_bilingual.json
6. python scripts/query.py
```

## Add New Manual to Project

To add another technical manual to the reference project:

1. **Process** it into text chunks
2. **Place** in `reference_project/data/raw/`
3. **Create golden set** (optional): `reference_project/data/golden_set/QA_my_manual.json`
4. **Update** `project_scope.json` with the new `manual_id`
5. **Run**: `python scripts/build.py --manual-id my_manual`

## Uses of the Reference Project

### For Developers
```bash
# Contribute improvements
# 1. Make changes in core/
# 2. Test with reference project
python scripts/build.py --manual-id reference_8070 --mode force-all
python scripts/evaluate.py --qa-file reference_project/data/golden_set/QA_bilingual.json
```

### For Users
```bash
# Understand how SemanticRAG works
# 1. View project structure
# 2. Run reference build
# 3. Explore outputs
# 4. Adapt to your domain
```

### For QA/Testing
```bash
# Validate releases
python scripts/build.py --manual-id reference_8070
python scripts/evaluate.py --qa-file reference_project/data/golden_set/QA_*
python scripts/check_api.py  # Verify API usage
```

## Advanced Configuration

### AAS Projection (if enabled)
```bash
# In .env:
ENABLE_AAS_PROJECTION=true

python scripts/build.py --manual-id reference_8070 --enable-aas
```

Output: `reference_project/aas_shell.json` and `submodels.json`

### GraphDB Publication
```bash
# In .env:
ENABLE_GRAPHDB_PUBLICATION=true
GRAPHDB_ENDPOINT=http://localhost:7200

python scripts/publish.py --reference
```

Publishes to: `http://localhost:7200/sparql` (named graph: `reference_8070`)

## Monitoring

```bash
# View reference build logs
tail -f logs/semantic_rag.log

# Build statistics
cat data/processed/build_report.json | jq '.'

# Evaluation results
cat data/processed/bilingual_eval_report.json | jq '.metrics'
```

## Troubleshooting

### Build fails on stability
```bash
# Reduce batch size
# In .env:
BATCH_SIZE=2

python scripts/build.py --manual-id reference_8070 --mode resume-compatible
```

### Evaluation with low scores
```bash
# Verify Golden Set
python scripts/evaluate.py \
  --qa-file reference_project/data/golden_set/QA_bilingual.json \
  --debug  # See details
```

## Support

- **Documentation**: [ARCHITECTURE.md](../ARCHITECTURE.md)
- **Issues**: Open an issue with tag `reference-project`
- **Questions**: Check [FAQ](../docs/FAQ.md)

---

**Next step**: [QUICKSTART.md](../QUICKSTART.md) for your own manuals.
