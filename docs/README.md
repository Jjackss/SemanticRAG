# Documentation

Complete documentation index for SemanticRAG.

## Getting Started

| Document | For Whom | Time |
|----------|----------|------|
| [README.md](../README.md) | Everyone | 5 min |
| [QUICKSTART.md](../QUICKSTART.md) | New users | 10 min |
| [ARCHITECTURE.md](../ARCHITECTURE.md) | Developers | 15 min |

## Usage Guides

| Document | Topic | Level |
|----------|-------|-------|
| [DATA_PIPELINE.md](DATA_PIPELINE.md) | Data flow | Intermediate |
| [CONFIGURATION.md](CONFIGURATION.md) | Advanced configuration | Advanced |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Problem solving | All |
| [FAQ.md](FAQ.md) | Frequently asked questions | All |

## For Developers

| Document | Topic |
|----------|-------|
| [CONTRIBUTING.md](../CONTRIBUTING.md) | How to contribute |
| [ARCHITECTURE.md](../ARCHITECTURE.md) | Code architecture |

## Documented Directories

| Path | Purpose |
|------|---------|
| [data/input/](../data/input/README.md) | Where to add your manuals |
| [data/golden_sets/](../data/golden_sets/README.md) | Validation datasets |
| [reference_project/](../reference_project/README.md) | Reference project |
| [tests/](../tests/__init__.py) | Test suite |

## Search by Topic

### Installation and Setup
- Quick start: [README.md - Quick Start](../README.md#quick-start-5-minutes)
- Detailed: [QUICKSTART.md](../QUICKSTART.md)
- Issues: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Adding Manuals
- Guide: [data/input/README.md](../data/input/README.md)
- Examples: [QUICKSTART.md - Common Use Cases](../QUICKSTART.md#common-use-cases)
- Formats: [FAQ.md - What input formats are supported?](FAQ.md#what-input-formats-are-supported)

### Configuration
- Basic: [.env.example](../.env.example)
- Advanced: [CONFIGURATION.md](CONFIGURATION.md)
- By use case: [CONFIGURATION.md - Predefined Profiles](CONFIGURATION.md#predefined-profiles)

### Evaluation and Validation
- Golden Sets: [data/golden_sets/README.md](../data/golden_sets/README.md)
- Evaluation: [QUICKSTART.md - Step 4](../QUICKSTART.md#step-4-run-build-5-30-minutes)
- Results: [DATA_PIPELINE.md - Phase 8](DATA_PIPELINE.md#phase-8-evaluation-if-golden-set)

### GraphDB and Publication
- Setup: [README.md - GraphDB](../README.md#use-remote-graphdb)
- Troubleshooting: [TROUBLESHOOTING.md - GraphDB](TROUBLESHOOTING.md#graphdb)
- Details: [DATA_PIPELINE.md - Phase 9](DATA_PIPELINE.md#phase-9-publication-optional)

### Performance and Optimization
- Quick tips: [README.md](../README.md)
- Tuning: [CONFIGURATION.md - Performance](CONFIGURATION.md#performance-tuning)
- Monitoring: [docs/TROUBLESHOOTING.md - Diagnosis](TROUBLESHOOTING.md#complete-diagnosis)

### Contributing and Development
- Getting started: [CONTRIBUTING.md](../CONTRIBUTING.md)
- Standards: [CONTRIBUTING.md - Code Standards](../CONTRIBUTING.md#code-standards)
- Architecture: [ARCHITECTURE.md - Components](../ARCHITECTURE.md#core-components)

### Multilingual (English)
- How it works: [ARCHITECTURE.md - Configuration](../ARCHITECTURE.md#llm-model-selection)
- Golden sets: [data/golden_sets/README.md - Multilingualism](../data/golden_sets/README.md#multilingualism)
- FAQ: [FAQ.md - Other languages](FAQ.md#can-i-use-a-manual-in-another-language)

## Quick Checklist

### For New Users
- [ ] Read [README.md](../README.md) (5 min)
- [ ] Follow [QUICKSTART.md](../QUICKSTART.md) (10 min)
- [ ] Run your first build
- [ ] Open [FAQ.md](FAQ.md) if you have questions

### For Adding Your Own Manual
- [ ] Prepare your manual (TXT/PDF/MD)
- [ ] Read [data/input/README.md](../data/input/README.md)
- [ ] Run `python scripts/build.py`
- [ ] Verify outputs in `data/processed/`

### For Production Setup
- [ ] Read [ARCHITECTURE.md](../ARCHITECTURE.md)
- [ ] Configure `.env` according to [CONFIGURATION.md](CONFIGURATION.md)
- [ ] Setup GraphDB if necessary
- [ ] Create golden sets for validation
- [ ] Run tests: `pytest tests/`

### For Contributing
- [ ] Read [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Fork repository
- [ ] Create feature branch
- [ ] Follow [CONTRIBUTING.md - Code Standards](../CONTRIBUTING.md#code-standards)
- [ ] Create PR with description

## Troubleshooting

1. **General problem** → Check [FAQ.md](FAQ.md)
2. **Specific error** → Search [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. **Configuration** → See [CONFIGURATION.md](CONFIGURATION.md)
4. **Performance** → Read [DATA_PIPELINE.md](DATA_PIPELINE.md)
5. **Still failing** → Open an issue with details

## Reading Roadmap

### Path 1: User (Add manuals)
1. [README.md](../README.md) - Overview
2. [QUICKSTART.md](../QUICKSTART.md) - First steps
3. [data/input/README.md](../data/input/README.md) - How to add
4. [FAQ.md](FAQ.md) - Answer questions
5. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - If something fails

### Path 2: Evaluator (Validate quality)
1. [README.md](../README.md)
2. [data/golden_sets/README.md](../data/golden_sets/README.md) - Create datasets
3. [QUICKSTART.md](../QUICKSTART.md) - Build and evaluate
4. [DATA_PIPELINE.md](DATA_PIPELINE.md) - Understand phases

### Path 3: Developer (Contribute)
1. [README.md](../README.md)
2. [ARCHITECTURE.md](../ARCHITECTURE.md) - Components
3. [DATA_PIPELINE.md](DATA_PIPELINE.md) - Detailed flow
4. [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute
5. [CONFIGURATION.md](CONFIGURATION.md) - Advanced

### Path 4: DevOps (Deploy)
1. [ARCHITECTURE.md](../ARCHITECTURE.md)
2. [CONFIGURATION.md](CONFIGURATION.md) - Profiles
3. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problem solving
4. [DATA_PIPELINE.md](DATA_PIPELINE.md) - Performance

## Useful Links

- **Code**: [core/](../core/) - Reusable modules
- **Scripts**: [scripts/](../scripts/) - Entry points
- **Reference Project**: [reference_project/](../reference_project/)
- **Config**: [config/](../config/)
- **Tests**: [tests/](../tests/)

## Support

- Documentation: Complete in this directory
- Issues: GitHub Issues
- Questions: GitHub Discussions
- Emergencies: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Start with**: [README.md](../README.md) or [QUICKSTART.md](../QUICKSTART.md)
