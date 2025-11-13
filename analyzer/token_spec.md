# Especificación: Token y API del Lexer

Este documento define el contrato mínimo para el analizador léxico (lexer) que emplearán ambos miembros del equipo. Sirve como referencia acordada para la estructura de los tokens y la API pública del módulo.

## Estructura del Token
Cada token producido por el lexer debe ser un objeto con, como mínimo, los siguientes campos:

- `type` (string): identificador del tipo de token, por ejemplo: `IDENT`, `NUMBER`, `STRING`, `PLUS`, `LPAREN`, `EOF`, `ERROR`, etc. Recomendado usar cadenas constantes o un Enum.
- `lexeme` (string): el texto exacto del token tal como apareció en la entrada (el lexema).
- `line` (int): número de línea donde comienza el token (1-indexed).
- `column` (int): número de columna donde comienza el token (1-indexed).

Ejemplo (pseudo-JSON):

```json
{ "type": "IDENT", "lexeme": "variable", "line": 3, "column": 5 }
```

Opcionalmente se puede añadir:
- `literal` (any): valor interpretado (por ejemplo, número -> int/float, string -> string con escapes resueltos).
- `end_line` / `end_column` para tokens multilínea (si es relevante).

## API pública del módulo `analyzer.lexer`
Propuesta mínima de API que el lexer debe exponer:

- Clase `Lexer`:
  - `__init__(self, source: str)` — inicializa el lexer con la fuente a tokenizar.
  - `next_token(self) -> Token` — devuelve el siguiente token (consumido). En caso de error léxico, puede devolver un token con `type = "ERROR"` y detalles en `lexeme` o `literal`.
  - `tokenize(self) -> List[Token]` — tokeniza toda la entrada y devuelve la lista de tokens (incluyendo un token final `EOF`).

- Alternativas:
  - `peek(n=1) -> Token` para mirar tokens sin consumir (opcional).
  - `reset()` para reiniciar el cursor al inicio (opcional).

## Formato de import / ejemplo de uso (Python)

```python
from analyzer.lexer import Lexer

source = 'a = 1 + 2 * (3 - 4)\n'
lexer = Lexer(source)
tokens = lexer.tokenize()
for t in tokens:
    print(t)
```

Ejemplo de retorno esperado (lista simplificada):

```
[IDENT('a'), EQ('='), NUMBER('1'), PLUS('+'), NUMBER('2'), STAR('*'), LPAREN('('), NUMBER('3'), MINUS('-'), NUMBER('4'), RPAREN(')'), EOF]
```

Cada token debe contener metadata de posición.

## Tokens recomendados (iniciales)
- IDENT — identificadores
- NUMBER — números enteros (y luego floats)
- STRING — literales de cadena
- PLUS, MINUS, STAR, SLASH — operadores aritméticos
- EQ, NEQ, LT, GT, LTE, GTE — operadores relacionales (según lenguaje)
- LPAREN, RPAREN, LBRACE, RBRACE, COMMA, SEMICOLON — símbolos
- COMMENT — (o ignorar) comentarios de línea / bloque
- EOF — fin de archivo
- ERROR — token de error léxico

Ajustar esta lista según `statement.md`.

## Errores léxicos
- Cuando se encuentra un carácter inválido o un literal sin cerrar, el lexer debe generar un token `ERROR` con `lexeme` indicando el fragmento problemático y `line`/`column` de su inicio.
- El lexer puede elegir entre recuperar y seguir tokenizando (recomendado para tests de robustez) o abortar lanzando excepción; documentar la elección en `analyzer/README.md`.

## Fixtures y tests de interoperabilidad
Crear un directorio de fixtures compartidos que incluya casos simples y edge-cases:

- `analyzer/tests/fixtures/simple1.src` — `a = 1 + 2`
- `analyzer/tests/fixtures/strings.src` — ejemplos de cadenas con escapes
- `analyzer/tests/fixtures/numbers.src` — enteros, flotantes y notación exponencial
- `analyzer/tests/fixtures/large.src` — archivo simulado de ~1MB para pruebas de throughput

Los tests deben validar que `tokenize()` devuelve tokens con el formato exacto definido aquí.

## Versionado del contrato
Si se requieren extensiones (por ejemplo `literal` o `end_line`), añadir una nota de versión en este archivo para coordinar cambios entre ambos desarrolladores.

---

(Actualizar esta especificación si algún punto en `statement.md` obliga a cambiar los nombres o la presencia de tokens.)
