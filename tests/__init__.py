# 📝 tests/ - Testing Suite

Este directorio contiene tests para validar la calidad del código y funcionalidad del sistema.

# 📂 Estructura

```
tests/
├── __init__.py
├── conftest.py                     # Configuración compartida pytest
├── test_ingestion.py               # Tests de ingesta
├── test_extraction.py              # Tests de extracción
├── test_retrieval.py               # Tests de recuperación
├── test_database.py                # Tests de persistencia
├── test_aas_projection.py          # Tests de proyección AAS
├── test_integration.py             # Tests de integración
└── fixtures/
├── sample_manual.txt           # Manual de ejemplo
└── sample_qa_golden_set.json   # Golden set de prueba
```

# 🏃 Ejecutar Tests

# Todos los tests
```bash
pytest tests/
```

# Con cobertura
```bash
pytest tests / --cov = core - -cov-report = html
# Ver: htmlcov/index.html
```

# Tests específicos
```bash
pytest tests/test_extraction.py
pytest tests/test_extraction.py: : test_abox_extractor
```

# Con logs detallados
```bash
pytest tests / -v - s
```

# 📋 Tipos de Tests

# Unit Tests
Prueban componentes individuales en aislamiento.

```python


def test_chunker_splits_text():
    from core.ingestion import Chunker
    chunker = Chunker(chunk_size=100)
    chunks = chunker.chunk("Text 1. Text 2. Text 3.")
    assert len(chunks) == 3


```

# Integration Tests
Prueban flujos completos entre componentes.

```python


def test_build_pipeline_end_to_end():


    # 1. Ingestion
    # 2. Extraction
    # 3. Canonicalization
    # 4. Validation
    # Verificar que outputs están correctos
```

# Smoke Tests
Pruebas rápidas para detectar problemas obvios.

```python


def test_api_connectivity():


    # Verificar que la API responde
    # Verificar que las credenciales son válidas
```

# ✅ Ejecutar Antes de Commit

```bash
# 1. Linter y formateo
black tests/
flake8 tests/

# 2. Type checking
mypy core/

# 3. Tests
pytest tests / --cov = core

# 4. Todo en uno
make test
```

# 📊 Cobertura de Código

Objetivo: ** > 80 % cobertura**

Ver reporte: `htmlcov/index.html`

---

Ver[CONTRIBUTING.md](../CONTRIBUTING.md) para más detalles.
