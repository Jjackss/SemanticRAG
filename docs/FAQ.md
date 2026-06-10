# Preguntas Frecuentes (FAQ)

## ¿Cuál es el primer paso?

1. Clonar repositorio
2. Crear `.env` con API key
3. Ejecutar `python scripts/build.py --manual-id my_manual`

Ver: [QUICKSTART.md](../QUICKSTART.md)

## ¿Qué formatos de entrada soporta?

- **.txt** - Texto plano (recomendado)
- **.pdf** - Archivos PDF
- **.md** - Markdown

## ¿Puedo usar un manual en otro idioma?

Soportamos:
- **Español (ES)**
- **Inglés (EN)**
- **Bilingüe (ES + EN)**

Otros idiomas requieren traducción previa.

## ¿Cuánto cuesta ejecutar esto?

Depende de:
- **Tamaño del manual** (número de chunks)
- **Modelo LLM** seleccionado
- **Batch size** configurado

Estimación para manual de 50 KB:
- Mistral: ~$0.05
- Qwen: Variable según proveedor

## ¿Necesito GraphDB?

**No**, es opcional.

- **Sin GraphDB**: Almacenamiento local en RDF (TTL)
- **Con GraphDB**: Mejor para grafos grandes, queries más rápidas

## ¿Puedo procesar múltiples manuales?

Sí, de varias formas:

```bash
# Uno por uno
python scripts/build.py --manual-id manual_1
python scripts/build.py --manual-id manual_2

# O crear script batch
for manual in data/input/*.txt; do
  id=$(basename "$manual" .txt)
  python scripts/build.py --manual-id "$id"
done
```

## ¿Cuál es el output principal?

El archivo más importante es:
**`data/processed/abox_linked.ttl`**

Es tu Knowledge Graph en formato RDF/Turtle.

Otros archivos útiles:
- `build_report.json` - Estadísticas
- `multilingual_lexicon.json` - Términos ES/EN
- `canonicalization_report.json` - Detalles de desduplicación

## ¿Cómo consulto el grafo?

```bash
# Interactivo
python scripts/query.py

# Desde Python
from rdflib import Graph
g = Graph()
g.parse("data/processed/abox_linked.ttl")
results = g.query("SELECT ?entity WHERE { ?entity rdf:type ?type }")
```

## ¿Puedo cambiar el modelo LLM?

Sí, edita `.env`:

```ini
# Mistral (rápido, recomendado)
LLM_MODEL=mistral-large-latest

# Qwen (alternativa)
LLM_MODEL=qwen-2.5-32b
```

## ¿Qué es un Golden Set?

Dataset de Q&A pares para validar calidad:

```json
[
  {
    "question": "¿Cómo instalar?",
    "expected_answer": "Pasos: 1..., 2..., 3...",
    "manual_id": "my_manual"
  }
]
```

Se usa para evaluar: `python scripts/evaluate.py --qa-file golden_set.json`

## ¿Qué es la desduplicación (Canonicalization)?

Proceso de consolidar múltiples referencias a la misma entidad:

- **Antes**: `CNC_8070`, `cnc-8070`, `8070 CNC` (3 entidades)
- **Después**: `CNC_8070` (1 entidad con aliases)

Aumenta calidad y reduce redundancia.

## ¿Puedo contribuir?

¡Sí! Ver [CONTRIBUTING.md](../CONTRIBUTING.md)

Áreas abiertas:
- Nuevos formatos de entrada
- Soporte multilingüe mejorado
- Tests adicionales
- Documentación

## ¿Dónde obtengo soporte?

1. **Documentación**: Ver `/docs`
2. **FAQ**: Este archivo
3. **Troubleshooting**: [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md)
4. **Issues**: GitHub issues
5. **Discusiones**: GitHub Discussions

## ¿Qué debo hacer si algo falla?

1. Revisa [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Verifica logs: `tail -f logs/semantic_rag.log`
3. Ejecuta health check: `python scripts/check_api.py`
4. Si aún falla, abre un issue con:
   - Python version
   - Último error
   - Configuración (.env anónimizada)
   - Pasos para reproducir

## ¿Es necesario conocer SPARQL?

**No**, pero es útil para queries avanzadas.

Para empezar:
- Usa CLI interactivo: `python scripts/query.py`
- Tutorial SPARQL: [w3.org/TR/sparql11-query](https://www.w3.org/TR/sparql11-query)

## ¿Qué es T-Box vs A-Box?

- **T-Box**: Esquema (clases, propiedades, relaciones)
  - Ej: "CNC es una máquina", "tiene modelo"
  - Archivo: `ontology_aligned.ttl`

- **A-Box**: Datos (instancias específicas)
  - Ej: "CNC_8070 es un CNC", "tiene modelo 8070"
  - Archivo: `abox_linked.ttl`

## ¿Puedo usar con otros LLMs?

Actualmente: Mistral y Qwen

Para agregar otro LLM:
1. Ver `core/extraction/llm_client.py`
2. Implementar interfaz
3. Agregar en `config/llm_config.py`
4. Pull Request

## ¿Cuál es el tamaño máximo de manual?

Sin límite teórico, pero:
- **< 5 KB**: Muy pequeño, resultados pobres
- **5-100 KB**: Óptimo
- **100-500 KB**: Bueno
- **> 500 KB**: Procesamiento lento, considera dividir

## ¿Qué es AAS Projection?

Proyección opcional a Asset Administration Shell (estándar de la industria 4.0).

Habilita con: `ENABLE_AAS_PROJECTION=true`

Output: `aas_shell.json` + `submodels.json`

## ¿Puedo ejecutar en Docker?

Pendiente, pero está en roadmap.

Ahora:
```bash
# Manual
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ¿Hay versiones anteriores?

Sí, repositorio original:
- Ubicación: `/reference_project/`
- Estado: Legacy, mantenido para compatibilidad
- Nuevo: Usa v2 para nuevos proyectos

## ¿Puedo usar versión anterior?

No recomendado. La v2 es más limpia y documentada.

Si necesitas features específicas de v1:
1. Abre issue explicando qué necesitas
2. O colabora portando la feature

---

**¿Aún tienes dudas?** → Abre un issue o discussion
