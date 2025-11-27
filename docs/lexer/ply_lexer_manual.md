# Manual Técnico del Lexer (ply_lexer.py)

Este documento detalla la arquitectura, el funcionamiento y las convenciones del analizador léxico implementado en `analyzer/ply_lexer.py`. Sirve como una guía para entender cómo el código fuente es convertido en tokens y cómo extender su funcionalidad.

## 1. Estructura General

El lexer está construido utilizando la librería `ply.lex`. En lugar de una clase, el lexer se define a través de un conjunto de variables y funciones en el módulo, que PLY utiliza para construir el autómata subyacente.

La estructura del archivo se divide en:

1.  **`tokens` (Tupla)**: Una lista que declara todos los nombres de los tipos de token que el parser puede recibir.
2.  **`reserved` (Diccionario)**: Un mapa que asocia palabras clave del lenguaje (ej. `"if"`) con su tipo de token correspondiente (ej. `"IF"`). Se utiliza dentro de la regla de identificadores para distinguir entre un identificador genérico y una palabra reservada.
3.  **Reglas de Tokens (Funciones y Variables)**: El núcleo del lexer. Son variables o funciones con un formato especial `t_TOKENNAME` que PLY reconoce.
    *   **Reglas simples**: Variables con una expresión regular (ej. `t_PLUS = r'\+'`).
    *   **Reglas complejas**: Funciones que tienen una expresión regular en su `docstring` y permiten ejecutar código para realizar acciones más complejas (ej. convertir un string a número, asignar literales, etc.).
4.  **Funciones especiales `t_*`**:
    *   `t_error`: Captura cualquier carácter que no coincida con ninguna otra regla.
    *   `t_comment`, `t_doc_comment`, `t_ignore_multiline_comment`: Reconocen y descartan diferentes tipos de comentarios.
    *   `t_newline`: Maneja los saltos de línea para llevar la cuenta del número de línea.
5.  **Función `tokenize_source`**: La interfaz pública principal que recibe el código fuente y retorna la lista completa de tokens.

## 2. Proceso de Tokenización y Estructura del Token

El análisis léxico se inicia llamando a la función `tokenize_source(source: str)`. Esta función realiza los siguientes pasos:
1.  Inicializa el lexer de PLY con el código fuente.
2.  Itera, llamando al método `lexer.token()` para obtener el siguiente token.
3.  Para cada token generado por PLY, construye un diccionario con una estructura estandarizada.
4.  Retorna una lista de estos diccionarios.

### Estructura de un Token

Cada token es un diccionario con los siguientes campos:

-   `type` (str): La categoría del token (ej. `IDENT`, `NUMBER`, `CONSOLE_PRINT`).
-   `value` (str): El lexema; es el texto exacto que fue extraído del código fuente (ej. `5`, `"Hello\n"`, `println!`).
-   `line` (int): El número de línea donde el token comienza (1-indexed).
-   `column` (int): La posición de la columna (relativa al inicio del archivo) donde el token comienza.
-   `literal` (any): El valor del token interpretado en Python. Es crucial para los siguientes pasos del compilador.
    -   Para un `NUMBER`, es un `int`.
    -   Para un `FLOAT`, es un `float`.
    -   Para un `STRING`, es un `str` con las secuencias de escape resueltas (ej. `\n` se convierte en un salto de línea real).
    -   Para `true`/`false`, es el booleano `True`/`False`.
    -   Para otros tokens, suele ser el mismo que el `value`.

## 3. Tokens Reconocidos

El lexer reconoce los siguientes tokens, agrupados por categoría:

#### Palabras Clave
- **Control de Flujo**: `IF`, `ELSE`, `WHILE`, `FOR`, `LOOP`, `BREAK`, `CONTINUE`
- **Declaraciones**: `FN`, `LET`, `MUT`, `RETURN`, `CONST`, `STATIC`
- **Tipos**: `I32`, `I64`, `U32`, `U64`, `F32`, `F64`, `BOOL`, `CHAR`, `STR`, `STRING_TYPE`, `TRUE`, `FALSE`
- **Estructuras**: `STRUCT`, `ENUM`, `SELF`, `SELF_TYPE`
- **Traits**: `TRAIT`, `IMPL`
- **I/O**: `INPUT`, `IN`

#### Literales e Identificadores
- `IDENT`: Nombres de variables, funciones, etc.
- `NUMBER`: Números enteros.
- `FLOAT`: Números de punto flotante.
- `STRING`: Cadenas de texto.

#### Macros
- `CONSOLE_PRINT`: Las macros `println!`, `print!`, `eprintln!` y `eprint!`.

#### Operadores y Símbolos
- **Aritméticos**: `PLUS` (+), `MINUS` (-), `TIMES` (*), `DIVIDE` (/), `MODULO` (%)
- **Asignación**: `EQUALS` (=), `PLUS_EQUALS` (+=), `MINUS_EQUALS` (-=), `TIMES_EQUALS` (*=), `DIVIDE_EQUALS` (/=)
- **Comparación**: `EQ` (==), `NEQ` (!=), `LT` (<), `LTE` (<=), `GT` (>), `GTE` (>=)
- **Lógicos**: `AND` (&&), `OR` (||), `NOT` (!)
- **Otros**: `ARROW` (->), `DOTDOT` (..)

#### Delimitadores
- `LPAREN` ((), `RPAREN` ()), `LBRACE` ({), `RBRACE` (}), `LBRACKET` ([), `RBRACKET` (])
- `SEMICOLON` (;), `COLON` (:), `COMMA` (,), `PIPE` (|)

#### Referencias
- `AMPERSAND` (&)

## 4. Reglas Especiales y Manejo de Errores

### Reglas de Prioridad para Macros
Para reconocer `println!` como un solo token en lugar de dos (`println` y `!`), se define una regla específica para este patrón. En PLY, el orden de las reglas importa.

La función `t_CONSOLE_PRINT` está definida **antes** que la regla genérica `t_identifier`. Esto asegura que el lexer intente hacer coincidir `println!` (y variantes) primero. Si no lo logra, pasará a la siguiente regla, `t_identifier`, como respaldo.

### Manejo de Errores
Cuando el lexer encuentra un carácter que no encaja en ninguna regla (ej. `#`, `$`), se invoca la función `t_error(t)`. Nuestra implementación:
1.  **No se detiene**: El lexer no aborta.
2.  **Crea un Token `ERROR`**: En lugar de ignorar el carácter, la función construye y retorna un token especial.
    -   `type`: `"ERROR"`
    -   `value`: El carácter problemático (ej. `'#'`).
    -   `literal`: Un mensaje de error descriptivo (ej. `"Illegal character '#'`)
3.  **Avanza**: Llama a `t.lexer.skip(1)` para avanzar al siguiente carácter y continuar la tokenización.

Esto permite que la interfaz de usuario reciba y muestre una lista completa de errores léxicos en una sola pasada.