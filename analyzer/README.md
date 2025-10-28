# Analyzer — Lexer (especificaciones y contrato)

Este directorio contendrá el código del analizador léxico y la documentación del contrato compartido entre los desarrolladores.

Archivos importantes:

- `token_spec.md` — especificación del `Token` y la API pública del lexer (contrato). (VER .\/token_spec.md)

Objetivo
--------
Implementar un lexer que transforme texto fuente en una secuencia de tokens estructurados. Este README enlaza a `token_spec.md` que define la estructura mínima de los tokens y ejemplos de uso.

Decisión sobre errores
----------------------
Se recomienda que el lexer devuelva tokens `ERROR` en lugar de lanzar excepciones cuando sea posible, para permitir tests más robustos y detección de múltiples errores en una pasada. Documentar cualquier desviación en el código.

Cómo usar (ejemplo)
-------------------
```python
from analyzer.lexer import Lexer

source = 'a = 1 + 2 * (3 - 4)\n'
lexer = Lexer(source)
for t in lexer.tokenize():
    print(t)
```

Fixtures de pruebas
-------------------
Crear `analyzer/tests/fixtures/` con casos básicos y edge-cases listados en `token_spec.md`.

Siguientes pasos
----------------
1. Implementar `analyzer/token.py` con la representación del Token (dataclass).
2. Implementar `analyzer/lexer.py` con la clase `Lexer` y funciones `next_token()` y `tokenize()`.
3. Crear tests y fixtures en `analyzer/tests/`.

Si modificas el contrato, actualiza `token_spec.md` y revisa con tu compañero.
