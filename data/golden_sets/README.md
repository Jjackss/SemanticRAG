# data/golden_sets/ - Validation Datasets

This directory contains **golden sets** - Q&A datasets for validating Knowledge Graph quality.

## What is a Golden Set?

A golden set is a collection of **question-answer (Q&A) pairs** with manually verified answers. Used for:

1. **Evaluation**: Measure system precision and recall
2. **Validation**: Verify quality before publication
3. **Testing**: Detect regressions in changes
4. **Benchmarking**: Compare different configurations

## Golden Set Format

### JSON Structure
```json
[
  {
    "question": "What are the steps to install the CNC 8070?",
    "expected_answer": "The steps are: 1. Verify requirements, 2. Download software, 3. Connect hardware...",
    "manual_id": "8070_installation",
    "difficulty": "easy",
    "language": "en",
    "category": "installation",
    "source_section": "Chapter 2: Installation Procedure"
  },
  {
    "question": "What are the error codes for the 8070?",
    "expected_answer": "Error codes include: E001 - Power failure, E002 - Communication error...",
    "manual_id": "man_8070_err",
    "difficulty": "medium",
    "language": "en",
    "category": "troubleshooting",
    "source_section": "Appendix A: Error Codes"
  }
]
```

### Required Fields
| Field | Type | Description |
|-------|------|-------------|
| `question` | string | Question in natural language |
| `expected_answer` | string | Correct verified answer |
| `manual_id` | string | Source manual ID |
| `difficulty` | string | easy / medium / hard |
| `language` | string | Language code (en / es) |

### Optional Fields
| Field | Type | Description |
|-------|------|-------------|
| `category` | string | installation, troubleshooting, operation, etc. |
| `source_section` | string | Manual section where it comes from |
| `keywords` | array | Relevant keywords |
| `entity_mentions` | array | Entities mentioned in Q&A |
| `relation_type` | string | Type of relationship asked |
| `metadata` | object | Additional information |

## Create a Golden Set

### Step 1: Select Questions
Extract questions from the manual:
```
Manual: "CNC 8070 Installation Guide"

Question 1: What are the hardware requirements?
Answer: "The requirements are: CPU 2GHz, RAM 4GB, HDD 100GB..."

Question 2: How to connect to the network?
Answer: "Use Cat6 Ethernet cable on RJ45 port..."
```

### Step 2: Format as JSON
```bash
cat > data/golden_sets/QA_my_manual.json << 'EOF'
[
  {
    "question": "What are the hardware requirements?",
    "expected_answer": "The requirements are: CPU 2GHz, RAM 4GB, HDD 100GB...",
    "manual_id": "my_manual",
    "difficulty": "easy",
    "language": "en",
    "category": "installation"
  }
]
EOF
```

### Step 3: Validate Format
```bash
python scripts/validate_golden_set.py \
  --qa-file data/golden_sets/QA_my_manual.json
```

## Golden Set Examples

### Example 1: Basic Bilingual Golden Set
```json
[
  {
    "question": "What is the model of the broacher?",
    "expected_answer": "The model is A218",
    "manual_id": "a218",
    "difficulty": "easy",
    "language": "en",
    "category": "product_info"
  },
  {
    "question": "What is the maximum cutting speed?",
    "expected_answer": "The maximum cutting speed is 50 m/min",
    "manual_id": "a218",
    "difficulty": "easy",
    "language": "en",
    "category": "specifications"
  }
]
```

### Example 2: Complex Golden Set (Multi-step)
```json
[
  {
    "question": "If the CNC 8070 shows error E002, what is the solution?",
    "expected_answer": "Error E002 indicates communication failure. Solution: 1. Verify serial connection, 2. Check communication drivers, 3. Restart controller",
    "manual_id": "man_8070_err",
    "difficulty": "hard",
    "language": "en",
    "category": "troubleshooting",
    "entity_mentions": ["CNC 8070", "E002", "communication"],
    "relation_type": "error_resolution"
  }
]
```

### Example 3: Reference Project Golden Set
```bash
cat data/golden_sets/QA_bilingual.json | head -20

# Output:
# [
#   {"question": "What is a broacher?", "expected_answer": "A broacher is...", ...},
#   {"question": "How does the CNC 8070 work?", "expected_answer": "The CNC 8070 is...", ...},
#   ...
# ]
```

## Use Golden Sets for Evaluation

### Automatic Evaluation
```bash
python scripts/evaluate.py \
  --qa-file data/golden_sets/QA_my_manual.json \
  --output eval_report.json
```

### Evaluation Output
```json
{
  "qa_file": "data/golden_sets/QA_my_manual.json",
  "total_questions": 25,
  "metrics": {
    "accuracy": 0.84,
    "precision": 0.88,
    "recall": 0.81,
    "f1_score": 0.84
  },
  "by_difficulty": {
    "easy": {"accuracy": 0.95, "count": 10},
    "medium": {"accuracy": 0.85, "count": 10},
    "hard": {"accuracy": 0.65, "count": 5}
  },
  "by_language": {
    "en": {"accuracy": 0.87}
  }
}
```

### Interactive Evaluation
```bash
python scripts/evaluate.py \
  --qa-file data/golden_sets/QA_my_manual.json \
  --interactive

# Output:
# Q: What are the requirements?
# Expected: The requirements are...
# Got: The system requires...
# Score: 0.78
```

## Testing Strategy

### Phase 1: Development Testing
```bash
# Small golden set (5-10 Q&A)
# For quick feedback
python scripts/evaluate.py \
  --qa-file data/golden_sets/QA_small_test.json

# Run often (< 1 min)
```

### Phase 2: Regression Testing
```bash
# Medium golden set (25-50 Q&A)
# For CI/CD
python scripts/evaluate.py \
  --qa-file data/golden_sets/QA_regression.json

# Run before each commit
```

### Phase 3: Quality Validation
```bash
# Large golden set (100+ Q&A)
# For final validation
python scripts/evaluate.py \
  --qa-file data/golden_sets/QA_comprehensive.json

# Run before releases
```

## Reference Files

In the reference project:
```
reference_project/data/golden_set/
├── QA_bilingual.json                    # 200+ Q&A in EN
├── QA_8070_quick_ref_bilingual.json     # 50 Q&A from quick ref
├── QA_chunks_8070_installation_manual.json  # 75 Q&A from installation
└── QA_chunks_8070_error_manual.json     # 60 Q&A from errors
```

## Best Practices

### Write Good Questions
- Good: "What is the step-by-step installation procedure?"
- Better: "What are the three initial installation steps?"
- Optimal: Include context: "After verifying requirements, what is the next step?"

- Bad: "What happens?"
- Worse: "Tell me about the product"

### Verify Answers
- Must be accurate and verified against the manual
- Must be complete but concise
- Must include context if necessary

### Balance Difficulty
- 50% easy (basic definitions)
- 30% medium (procedures)
- 20% hard (edge cases, troubleshooting)

### Multilingualism
- Maintain similar EN ratio
- Ensure Q&A are faithful translations if bilingual

## Complete Testing Workflow

```bash
# 1. Create golden set
cat > data/golden_sets/QA_my_manual.json << 'EOF'
[...]
EOF

# 2. Validate format
python scripts/validate_golden_set.py --qa-file data/golden_sets/QA_my_manual.json

# 3. Build KG
python scripts/build.py --manual-id my_manual

# 4. Evaluate
python scripts/evaluate.py --qa-file data/golden_sets/QA_my_manual.json

# 5. Analyze results
cat data/processed/eval_report.json | jq '.metrics'

# 6. Iterate if needed
```

## Troubleshooting

### "JSON parsing error"
Validate JSON is valid: `python -m json.tool QA_my_manual.json`

### "Accuracy too low"
Verify that expected answers are correct in the manual

### "Missing field 'language'"
Ensure all Q&A have required fields

## Resources

- [QUICKSTART.md](../QUICKSTART.md) - Quick start guide
- [ARCHITECTURE.md](../ARCHITECTURE.md) - Architecture
- [Examples](./QA_*.json) - Reference golden sets

---

**Next step**: Create your golden set and validate your Knowledge Graph.
