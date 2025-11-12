# Ticket: Implementar analizador léxico — (Colaborador)

## Resumen
Implementar y/o revisar partes del analizador léxico enfocadas en casos límite, pruebas y documentación. Este ticket está pensado para el segundo miembro del equipo.

## Asignado a
- Angello
- Víctor

## Trabajo conjunto
Este ticket se trabajará en conjunto por ambos miembros del equipo. Aunque aquí se destaca el enfoque en rendimiento y pruebas de carga, la responsabilidad es igualitaria: ambos implementarán, revisarán y validarán el lexer. Coordinar el reparto de subtareas en la rama/PR (por ejemplo: uno implementa el manejo de escapes y números, el otro agrega benchmarks y tests de carga).

## Trabajo en paralelo (división propuesta)
Propuesta para trabajar en paralelo sin bloqueos:

- Contrato compartido (ambos):
   - Definir `Token` y API pública (`Lexer(source)`, `next_token()`, `tokenize()`). Añadir ejemplos en `analyzer/README.md`.

- Tareas independientes (paralelizables):
   1. Núcleo del lexer (Víctor): identificadores, operadores básicos, números enteros, paréntesis, espacios y comentarios de línea.
   2. Casos límite y rendimiento (Angello): escapes en strings, números flotantes/exponenciales, comentarios multilínea, pruebas de carga y optimizaciones.

- Puntos de integración y verificación:
   - Un pequeño archivo `analyzer/token_spec.md` o la sección en `analyzer/README.md` que especifique tipos de token y formato del `Token`.
   - Fixtures compartidos en `analyzer/tests/fixtures/` para validar que ambas implementaciones producen tokens con el formato correcto.

**Importancia de los edge cases:**
Los edge cases (casos límite) son importantes porque garantizan que el lexer sea robusto y cumpla con los requisitos del README y el statement. Cubrir estos casos previene errores difíciles de detectar y asegura que el lexer funcione correctamente en situaciones reales y de integración. Si el lenguaje no requiere ciertos edge cases, se puede ajustar el alcance, pero es recomendable incluirlos para calidad y mantenibilidad.

## Prioridad
- Alta

## Objetivo / Historia
Completar y robustecer el lexer: enfocarse en casos límite (escapes en strings, números flotantes, comentarios anidados si aplica), añadir pruebas adicionales y preparar el módulo para integración con el parser.

## Contrato (inputs/outputs)
- Input: cadena (source code)
- Output: lista/stream de tokens con `type`, `lexeme`, `line`, `column`.
- Debe reportar errores léxicos con suficiente detalle.

## Criterios de aceptación
- [ ] Añadir/ajustar casos de tokenization en `analyzer/tests/test_lexer.py` cubriendo edge-cases.
- [ ] Implementar soporte para escapes dentro de strings y números con notación científica si el lenguaje lo requiere.
- [ ] Mejorar los mensajes de error léxico y devolver ubicación precisa.
- [ ] Revisar performance básica para entradas grandes (simular archivo de ~1MB).

## Tareas técnicas (subtareas)
1. Revisar el archivo `analyzer/lexer.py` y la especificación en `statement.md`.
2. Añadir soporte para:
   - Secuencias de escape en literales de string (`\n`, `\t`, `\\`, `\"`)
   - Números con punto decimal y notación exponencial si aplica
   - Comentarios multilínea (si el lenguaje los define)
3. Escribir pruebas unitarias adicionales en `analyzer/tests/test_lexer.py` (edge cases y cargas)
4. Añadir benchmarks simples o test de performance (opcional)
5. Documentar los casos límite en `analyzer/README.md`.

## Archivos a crear/editar
- `analyzer/lexer.py` (editar/acomodar)
- `analyzer/tests/test_lexer.py` (editar/agregar tests)
- `analyzer/README.md` (editar: casos límite y ejemplos)

## Estimación
- Implementación y tests: 6-12 horas
- Performance check y docs: 2 horas

## Pruebas recomendadas
- Strings con escapes y sin escapes
- Numeros: enteros, flotantes, exponenciales
- Archivo grande ~1MB para medir throughput básico

## Notas y dependencias
- Coordinación con la persona asignada al otro ticket para definir el formato exacto del Token.
 - Reparto sugerido: enfoque en performance y casos límite aquí; implementación básica y tests iniciales en el otro ticket. Ajustar según preferencia del equipo.

## Comunicación
- Dejar comentarios en el PR indicando qué pruebas se añadieron y qué casos faltan.

---

_Puedes reemplazar "Colaborador" por el nombre real y ajustar prioridades o tiempo estimado._
