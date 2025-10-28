# Ticket: Implementar analizador léxico — (Tú)

## Resumen
Implementar el analizador léxico (scanner/lexer) para el proyecto. Este ticket está asignado a ti y cubre la implementación inicial, pruebas básicas y documentación mínima para integrarlo con el analizador sintáctico.

## Asignado a
- Víctor
- Angello

## Trabajo conjunto
Este ticket se trabajará en conjunto por ambos miembros del equipo. La responsabilidad es compartida y las tareas pueden dividirse por subtareas; coordinar en PRs y revisiones. El ticket del colaborador se enfocará con mayor detalle en performance y casos límite, pero ambos tickets tienen igual prioridad y significado.

## Trabajo en paralelo (división propuesta)
Para evitar bloqueos y permitir que ambos trabajen en paralelo, proponemos la siguiente división con puntos de integración claros:

- Acordar el contrato compartido (ambos):
   - `Token` con campos: `type` (string/enum), `lexeme` (string), `line` (int), `column` (int)
   - API pública: `Lexer(source: str)`, `next_token()` -> Token, `tokenize()` -> List[Token]

- Tareas independientes (pueden realizarse en paralelo):
   1. Núcleo del lexer (Víctor): reconocimiento de identificadores, números enteros, operadores, paréntesis, espacios en blanco, saltos de línea y comentarios de línea. Implementación de la máquina/algoritmo de scan y pasos básicos de error handling.
   2. Casos límite y performance (Angello): escapes en strings, literales complejos, números flotantes y en notación exponencial, comentarios multilínea y pruebas de carga/benchmark.

- Puntos de integración (lo que ambos deben compartir):
   - Archivo o sección `analyzer/README.md` con el contrato del `Token` y ejemplos de uso.
   - Tests de interoperabilidad: un conjunto pequeño de fixtures compartidos para validar que `tokenize()` produce la misma estructura.

**Importancia de los edge cases:**
Los edge cases (casos límite) son relevantes porque aseguran que el lexer funcione correctamente en situaciones no triviales, como literales con escapes, números en formatos especiales y comentarios complejos. Esto sigue lo indicado en el README y en el statement, donde se pide robustez y cobertura completa de los tokens definidos. Si el lenguaje no requiere ciertos edge cases, se puede ajustar el alcance, pero es recomendable cubrirlos para evitar errores en producción y facilitar la integración con el parser.

## Prioridad
- Alta

## Objetivo / Historia
Como equipo, necesitamos un analizador léxico que convierta la entrada en una secuencia de tokens para que el parser pueda construir el AST. El lexer debe ser robusto frente a espacios, saltos de línea, comentarios y literales.

## Contrato (inputs/outputs)
- Input: cadena (source code) o stream de caracteres leído desde `backend/` o `analyzer/`.
- Output: flujo/lista de tokens. Cada token debe tener al menos: tipo, valor (lexema), posición (línea, columna).
- Errores: producir errores léxicos claros (token desconocido, literal sin cerrar) sin romper la ejecución — devolver objeto de error con posición.

## Criterios de aceptación
- [ ] Implementa un lexer en `analyzer/lexer.py` o `analyzer/lexer/__init__.py` según convenga.
- [ ] Tokeniza correctamente identificadores, números, cadenas, operadores y paréntesis según las especificaciones del lenguaje (ver `statement.md`).
- [ ] Soporta comentarios de línea y bloques (si aplica) y ignora espacios en blanco y saltos de línea salvo para ubicación.
- [ ] Incluye pruebas unitarias mínimas (happy path + 2 casos de error) en `analyzer/tests/test_lexer.py`.
- [ ] Documentación breve en el README del módulo (`analyzer/README.md`) explicando la API del lexer.

## Tareas técnicas (subtareas)
1. Revisar `statement.md` para los tokens esperados y reglas léxicas.
2. Crear archivo `analyzer/lexer.py` con la clase `Lexer` que exponga:
   - `__init__(source: str)`
   - `next_token()` -> Token
   - `tokenize()` -> List[Token]
3. Definir estructura `Token` (por ejemplo, dataclass con fields: type, lexeme, line, column).
4. Implementar manejo de errores léxicos y tipos de token.
5. Añadir pruebas unitarias (pytest) en `analyzer/tests/`.
6. Añadir documentación breve en `analyzer/README.md`.
7. Ejecutar pruebas locales y validar formato del código (si hay linter/formatter en el repo).

## Archivos a crear/editar
- `analyzer/lexer.py` (nuevo)
- `analyzer/tests/test_lexer.py` (nuevo)
- `analyzer/README.md` (modificar/crear)

## Estimación
- Implementación: 6-10 horas
- Tests y docs: 2 horas

## Pruebas recomendadas
- Tokenizar: `a = 1 + 2 * (3 - 4)` -> tokens esperados
- Literales: cadena con comillas y con escapes
- Errores: carácter inválido y literal sin cerrar

## Notas y dependencias
- Revisar `statement.md` para la definición completa de tokens y operadores.
- Coordinar con el compañero para no duplicar trabajo sobre `analyzer/lexer.py`.

## Comunicación
- Indica en el ticket si prefieres que el compañero revise PR o haga pair-programming en la parte de tests.

---

_Puedes actualizar el título/tu nombre si quieres que lo ponga explícitamente._
