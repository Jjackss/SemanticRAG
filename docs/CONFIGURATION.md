# Configuración Avanzada

Documentación detallada de opciones de configuración.

## Variables de Entorno (.env)

### LLM Configuration

```ini
# Selecciona el modelo a usar
LLM_MODEL=mistral-large-latest

# Opciones disponibles:
# - mistral-large-latest (recomendado, rápido)
# - mistral-medium-latest (equilibrado)
# - qwen-2.5-32b (alternativa)
```

### Batch Processing

```ini
# Número de requests paralelos
BATCH_SIZE=4

# Valores:
# 1-2: Más lento, pero más estable (para APIs con rate limits estrictos)
# 4-8: Óptimo para la mayoría de casos
# 16+: Rápido, pero requiere API generosa
```

### Retry Policy

```ini
RETRY_PROFILE=micro-batch-recovery

# Opciones:
# - standard: Reintentos simples
# - rate-limit-drain: Maneja rate limits
# - micro-batch-recovery: Divide en micro-batches (recomendado)

MAX_RETRIES=5
API_TIMEOUT=60
```

### GraphDB Configuration

Para publicar en GraphDB:

```ini
ENABLE_GRAPHDB_PUBLICATION=true
GRAPHDB_ENDPOINT=http://localhost:7200
GRAPHDB_REPOSITORY=default
GRAPHDB_USERNAME=admin
GRAPHDB_PASSWORD=your_password
```

### Multilinguality

```ini
ENABLE_MULTILINGUAL=true  # Activa lexicalización ES/EN
```

### AAS Projection

```ini
ENABLE_AAS_PROJECTION=false  # Activa si necesitas salida AAS
```

## Configuración Programática

### settings.py

```python
from config.settings import settings

# Acceder a valores
print(settings.llm_model)
print(settings.batch_size)
print(settings.is_graphdb_enabled)

# Validar configuración
if not settings.has_api_key:
    raise ValueError("API key not configured")
```

### LLM Config

Para usuarios avanzados que quieran modificar parámetros LLM:

```python
from config.llm_config import LLMConfig

config = LLMConfig(
    model_name="mistral-large-latest",
    temperature=0.5,  # 0=determinístico, 1=creativo
    max_tokens=2000,
)
```

## Profiles Predefinidos

### Production (Recomendado)
```ini
LLM_MODEL=mistral-large-latest
BATCH_SIZE=8
RETRY_PROFILE=rate-limit-drain
ENABLE_MULTILINGUAL=true
ENABLE_GRAPHDB_PUBLICATION=true
```

### Development (Rápido)
```ini
LLM_MODEL=mistral-medium-latest
BATCH_SIZE=2
LOG_LEVEL=DEBUG
VERBOSE=true
```

### Testing (Económico)
```ini
LLM_MODEL=mistral-medium-latest
BATCH_SIZE=1
ENABLE_GRAPHDB_PUBLICATION=false
```

## Paths Personalizados

Por defecto:
```
data/input/          # Tus manuales
data/processed/      # Outputs generados
data/golden_sets/    # Datasets de validación
logs/                # Archivos de log
```

Para cambiar:
```ini
DATA_INPUT_DIR=/ruta/a/manuales
DATA_PROCESSED_DIR=/ruta/a/outputs
DATA_GOLDEN_SETS_DIR=/ruta/a/datasets
LOG_FILE=/ruta/a/logs/semantic_rag.log
```

## Performance Tuning

### Para Procesamiento Rápido
```ini
BATCH_SIZE=16
LLM_MODEL=mistral-medium-latest
ENABLE_MULTILINGUAL=false  # Desactiva si no lo necesitas
```

### Para Mejor Calidad
```ini
BATCH_SIZE=2  # Menos paralelismo = menos errores
LLM_MODEL=mistral-large-latest
ENABLE_MULTILINGUAL=true
```

### Para Estabilidad (APIs Restrictivas)
```ini
BATCH_SIZE=1
RETRY_PROFILE=micro-batch-recovery
MAX_RETRIES=10
API_TIMEOUT=120
```

## Logging

```ini
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Ver logs en tiempo real
tail -f logs/semantic_rag.log

# Ver solo errores
grep ERROR logs/semantic_rag.log
```

## Debugging

### Modo Verbose
```ini
VERBOSE=true
LOG_LEVEL=DEBUG
```

Genera más output:
- Requests/responses de API
- Detalles de extracción
- Métricas de consolidación

### Temporary Files
```ini
TEMP_DIR=.tmp

# Los archivos temporales se guardan en .tmp/
# Útil para debugging
```

---

**Próximo**: [troubleshooting.md](troubleshooting.md)
