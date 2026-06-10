# Data Pipeline Detallado

Descripción técnica del flujo de datos a través del sistema.

## Fase 1: Ingestion

```
Manual (PDF/TXT/MD)
    ↓
document_loader.load()
    ↓
Raw text (UTF-8)
    ↓
chunker.chunk_by_semantics()
    ↓
chunks[]: {
    "text": str,
    "metadata": {
        "source_file": str,
        "chunk_id": int,
        "language": str,
        "density_score": float
    }
}
```

**Parámetros**:
- `chunk_size`: Tamaño base (512 tokens)
- `overlap`: Sobreposición (64 tokens)
- `language`: Auto-detect (ES/EN)

**Salida**: `chunks_*.json`

## Fase 2: Semantic Extraction (LLM)

```
chunks[] + extraction_prompt.txt
    ↓
LLM API Call (Mistral/Qwen)
    ↓
Raw RDF output (N-Triples)
    ↓
abox_semantic_validator.validate()
    ↓
{
  "triples": [
    {
      "subject": "http://example.org/entity_1",
      "predicate": "http://www.w3.org/2000/01/rdf-schema#label",
      "object": "Entity 1"
    },
    ...
  ],
  "quality_score": 0.92
}
```

**Prompts**:
- `abox_extraction_prompt.txt` - Extrae instancias
- `tbox_generation_prompt.txt` - Genera esquema

**Validación**:
- RDF syntax válido
- Entidades con URIs únicas
- Propiedades tipadas

**Salida**: `abox_input.json`

## Fase 3: A-Box Merge

```
abox_input.json (múltiples si hay varios manuales)
    ↓
abox_merger.merge()
    ↓
Combined RDF (Turtle)
    ↓
abox_merged.ttl
```

**Consolidación**:
- Union de todos los triples
- Preserva URIs originales
- No hay deduplicación aún

## Fase 4: Canonicalization

```
abox_merged.ttl
    ↓
entity_clustering.find_candidates()
    ↓
clusters: {
    "canonical_uri": ["alt_uri_1", "alt_uri_2", ...]
}
    ↓
rewrite_links_to_canonical()
    ↓
abox_canonical.ttl
```

**Algoritmo**:
1. Extrae surface forms (labels)
2. Calcula similitud (edit distance, semantic)
3. Agrupa candidatos
4. Elige URI canónica
5. Reescribe todas las referencias

**Reportes**:
- `canonicalization_report.json` - Detalles
- `canonical_entity_map.json` - Mapeo

## Fase 5: Enrichment

```
abox_canonical.ttl
    ↓
graph_enricher.detect_missing_links()
    ↓
Candidatos de links
    ↓
link_completer.validate_and_accept()
    ↓
abox_enriched.ttl
```

**Enriquecimiento**:
- Agrega links faltantes (basado en patrones)
- Valida nuevos links semánticamente
- Genera surface improvements

**Reportes**:
- `enrichment_report.json` - Links añadidos
- `enrichment_link_map.json` - Mapeo de nuevos links

## Fase 6: Multilinguality

```
abox_enriched.ttl
    ↓
multilingual_lexicon_builder.build()
    ↓
{
  "entity_uri": {
    "es": ["término 1", "término 2", ...],
    "en": ["term 1", "term 2", ...]
  },
  ...
}
    ↓
multilingual_lexicon.json
```

**Construcción**:
1. Extrae labels de todos los idiomas
2. Normaliza términos
3. Agrega sinónimos detectados
4. Genera mappings bidireccionales

**Uso**: Query normalization, answer rendering

## Fase 7: Validation

```
abox_enriched.ttl + ontology_aligned.ttl
    ↓
semantic_validator.validate()
    ↓
{
  "errors": [...],
  "warnings": [...],
  "stats": {
    "entities": 1250,
    "relations": 890,
    "avg_relations_per_entity": 0.71
  }
}
    ↓
Reporte de validación
```

**Checks**:
- Consistency con ontología
- No circular references
- Typed properties
- URI uniqueness

## Fase 8: Evaluation (si golden set)

```
abox_linked.ttl + multilingual_lexicon.json
    ↓
qa_evaluator.load_qa_set()
    ↓
Para cada Q&A pair:
  - Normaliza query
  - Ejecuta SPARQL
  - Compara con expected_answer
    ↓
Métricas:
{
  "accuracy": 0.84,
  "precision": 0.88,
  "recall": 0.81,
  "f1": 0.84
}
```

**Métricas**:
- **Accuracy**: % de preguntas correctas
- **Precision**: % de respuestas relevantes
- **Recall**: % de respuestas posibles encontradas
- **F1**: Promedio armónico

## Fase 9: Publication (opcional)

```
abox_linked.ttl
    ↓
graphdb_publisher.publish()
    ↓
GraphDB API call
    ↓
Named graph creado
    ↓
http://graphdb:7200/sparql
```

**Opciones**:
- Local (RDF file): Siempre guardado
- GraphDB remote (opcional): Si configurado

## Artefactos de Salida

| Archivo | Fase | Uso |
|---------|------|-----|
| `abox_input.json` | Extracción | Auditoría de extracción |
| `ontology_aligned.ttl` | Ontology | T-Box |
| `abox_merged.ttl` | Merge | Diagnóstico pre-canon |
| `abox_canonical.ttl` | Canon | Entidades desdup |
| `abox_enriched.ttl` | Enrich | Grafo enriquecido |
| `abox_linked.ttl` | Final | **GRAFO FINAL** ✓ |
| `multilingual_lexicon.json` | Lingü | Búsqueda multilingüe |
| `build_report.json` | Final | Métricas y stats |
| `canonicalization_report.json` | Canon | Detalles dedup |
| `enrichment_report.json` | Enrich | Links añadidos |
| `eval_report.json` | Eval | Métricas de calidad |

## Performance Características

Por fase (para manual de 50 KB):

| Fase | Tiempo | API Calls | Bottleneck |
|------|--------|-----------|-----------|
| Ingestion | 2-5s | 0 | I/O disk |
| Extraction | 30-60s | 100-200 | LLM API |
| Merge | 5-10s | 0 | Parsing RDF |
| Canon | 10-20s | 0 | Graph reasoning |
| Enrich | 10-15s | 0 | Link detection |
| Evaluation | 5-10s | 0 | SPARQL queries |
| **Total** | **62-120s** | **100-200** | **LLM API** |

## Optimizaciones

### Paralelismo
- **Extraction**: Chunks procesados en paralelo (batch_size)
- **Validation**: Validaciones en paralelo

### Caching
- Extracción: Reutiliza si modo resume-compatible
- Merge: Incremental si multi-manual

### Lazy Loading
- RDF: Se parsea solo cuando se necesita
- Ontology: Se carga bajo demanda

## Debugging

### Ver estado de fase
```bash
# Después de build.py
cat data/processed/build_report.json | jq '.phases'

# Output:
# {
#   "ingestion": {"status": "complete", "duration": 3.2},
#   "extraction": {"status": "complete", "duration": 45.1},
#   ...
# }
```

### Inspeccionar artefactos intermedios
```bash
# Ver entidades después de canonicalización
cat data/processed/canonical_entity_map.json | jq '.entities | length'

# Ver links enriquecidos
cat data/processed/enrichment_report.json | jq '.links_added | length'
```

### Troubleshoot fase específica
```bash
# Si extraction falla:
tail -f logs/semantic_rag.log | grep -i extraction

# Si evaluation baja:
python scripts/evaluate.py --qa-file data/golden_sets/test.json --verbose
```

---

**Referencias**:
- [ARCHITECTURE.md](../ARCHITECTURE.md) - Overview
- [CONFIGURATION.md](CONFIGURATION.md) - Tuning
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problemas
