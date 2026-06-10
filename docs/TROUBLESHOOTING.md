# Troubleshooting

Soluciones a problemas comunes.

## API y Autenticación

### "API Key not found"

**Síntomas**: `ValueError: MISTRAL_API_KEY not set`

**Solución**:
```bash
# 1. Verifica que .env existe
ls -la .env

# 2. Verifica que tiene el API key
grep MISTRAL_API_KEY .env

# 3. Si está vacío, obtén una clave:
# https://console.mistral.ai/api-keys

# 4. Añade a .env:
echo "MISTRAL_API_KEY=your_key_here" >> .env
```

### "Invalid API Key"

**Síntomas**: `AuthenticationError: Invalid credentials`

**Solución**:
1. Verifica que la clave es correcta en console.mistral.ai
2. Verifica que no tiene espacios antes/después
3. Regenera la clave

### "Rate limit exceeded"

**Síntomas**: `RateLimitError: Too many requests`

**Solución**:
```ini
# En .env:
BATCH_SIZE=2  # Reduce paralelismo
RETRY_PROFILE=rate-limit-drain
MAX_RETRIES=10
API_TIMEOUT=120
```

Espera 15-30 minutos y reintenta.

## Build Pipeline

### Build falla sin error claro

**Solución**:
```bash
# Habilita logging detallado
export LOG_LEVEL=DEBUG
python scripts/build.py --manual-id my_manual --verbose

# Ver logs
tail -f logs/semantic_rag.log
```

### "No such file or directory: data/input/..."

**Solución**:
```bash
# Verifica que el archivo existe
ls -la data/input/

# Verifica el path exacto
python scripts/build.py \
  --source-chunks data/input/my_manual.txt \
  --manual-id my_manual
```

### Build interrumpido

**Solución**:
```bash
# Reanuda desde donde se detuvo
python scripts/build.py \
  --manual-id my_manual \
  --mode resume-compatible  # ← Clave

# Si eso no funciona:
python scripts/build.py \
  --manual-id my_manual \
  --mode force-stale
```

## GraphDB

### "Connection refused" (GraphDB)

**Síntomas**: `ConnectionError: [Errno 111] Connection refused`

**Solución**:
```bash
# Opción 1: Inicia GraphDB local
docker run -d -p 7200:7200 khronus/graphdb:latest

# Opción 2: Verifica que el endpoint es correcto en .env
cat .env | grep GRAPHDB_ENDPOINT

# Opción 3: Comprueba que está activo
curl http://localhost:7200/rest/repositories

# Si todo está bien pero sigue fallando:
python scripts/publish.py --verbose
```

### "Authentication failed" (GraphDB)

**Solución**:
```bash
# Verifica credenciales en .env
# Por defecto:
GRAPHDB_USERNAME=admin
GRAPHDB_PASSWORD=admin  # Cambia si lo modificaste en GraphDB

# O desactiva por ahora
ENABLE_GRAPHDB_PUBLICATION=false
```

## Calidad de Resultados

### "Low evaluation scores"

**Síntomas**: Accuracy < 60% en evaluación

**Posibles causas y soluciones**:

1. **Manual en idioma no soportado**
   ```bash
   # Verifica que es ES/EN
   # Si es otro idioma, requiere traducción previa
   ```

2. **Manual muy corto o fragmentado**
   ```bash
   # SemanticRAG necesita al menos 1,000 palabras
   # Manuales < 5,000 palabras pueden tener extractos incompletos
   ```

3. **Formato de entrada pobre**
   ```bash
   # Verifica que el manual tiene estructura clara
   # Secciones, párrafos, no bloques sin contexto
   ```

4. **Golden set incorrecto**
   ```bash
   # Verifica que las respuestas son precisas
   # Valida el JSON: python -m json.tool QA_file.json
   ```

5. **Modelo inadecuado**
   ```bash
   # Intenta con mistral-large-latest
   # En .env: LLM_MODEL=mistral-large-latest
   ```

### "Too many entity clusters"

**Síntomas**: Deduplicación produce muchos clusters

**Solución**:
```bash
# Aumenta strictness de canonicalización
# Ver: core/extraction/canonical_resolution_policy.py
# o reajusta prompts en core/extraction/prompts/
```

## Performance

### Build muy lento

**Causas**:
- Batch size muy pequeño
- Manual muy grande
- API lenta
- Máquina sin recursos

**Soluciones**:
```bash
# Aumenta batch size
BATCH_SIZE=8

# O reduce otro lado
# - Desactiva multilingüe
# - Desactiva AAS projection
```

### Out of memory

**Síntomas**: `MemoryError: Unable to allocate...`

**Soluciones**:
```bash
# 1. Reduce batch size
BATCH_SIZE=1

# 2. Procesa manual en partes
# Divide manualmente en chunks

# 3. Libera memoria
# Cierra otras aplicaciones
```

## Multilingüalidad

### "Language detection failed"

**Solución**:
```bash
# Especifica idioma explícitamente
# (Requiere modificación de código)
```

### "Poor translation quality"

**Solución**:
- Usa manuales con estructura clara
- Evita jerga muy técnica sin contexto
- Valida contra golden sets en ambos idiomas

## Diagnóstico Completo

```bash
# 1. Verificar configuración
python scripts/check_api.py

# 2. Ver logs
tail -f logs/semantic_rag.log

# 3. Inspeccionar artefactos
cat data/processed/build_report.json | jq '.metrics'

# 4. Evaluar calidad
python scripts/evaluate.py --qa-file data/golden_sets/QA_test.json

# 5. Ver estadísticas de consolidación
cat data/processed/canonicalization_report.json
```

## Reportar Issues

Si nada funciona, reporta un issue con:

```bash
# 1. Recolecta información
python -c "import sys; print(f'Python: {sys.version}')"
pip list | grep semantic

# 2. Anónimiza .env
cat .env | grep -v "API_KEY\|PASSWORD"

# 3. Captura error
python scripts/build.py --manual-id test 2>&1 | head -100

# 4. Sube logs
tar -czf logs.tar.gz logs/
```

Abre un issue con esta información.

---

**¿No encontraste solución?** → [FAQ](faq.md) o abre un issue
