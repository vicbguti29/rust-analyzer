# Manual Técnico del Lexer (ply_lexer.py)

Este documento detalla la arquitectura, el funcionamiento y las convenciones del analizador léxico implementado en `analyzer/ply_lexer.py`. Sirve como una guía para entender cómo el código fuente es convertido en tokens y cómo extender su funcionalidad.

## 1. Estructura General

El lexer está construido utilizando la librería `ply.lex`. En lugar de una clase, el lexer se define a través de un conjunto de variables y funciones en el módulo, que PLY utiliza para construir el autómata subyacente.

La estructura del archivo se divide en:

1.  **`tokens` (Tupla)**: Una lista que declara todos los nombres de los tipos de token que el lexer puede generar. PLY requiere esto para la validación.
2.  **`reserved` (Diccionario)**: Un mapa que asocia palabras clave del lenguaje (ej. `"if"`) con su tipo de token correspondiente (ej. `"IF"`). Se utiliza dentro de la regla de identificadores para distinguir entre un identificador genérico y una palabra reservada.
3.  **Reglas de Tokens (Funciones y Variables)**: El núcleo del lexer. Son variables o funciones con un formato especial `t_TOKENNAME` que PLY reconoce.
    *   **Reglas simples**: Variables con una expresión regular (ej. `t_PLUS = r'\+'`).
    *   **Reglas complejas**: Funciones que tienen una expresión regular en su `docstring` y permiten ejecutar código para realizar acciones más complejas (ej. convertir un string a número, asignar literales, etc.).
4.  **Función `t_error`**: Una regla especial que captura cualquier carácter que no coincida con ninguna otra regla.
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
    -   Para un `NUMBER`, es un `int` o `float`.
    -   Para un `STRING`, es un `str` con las secuencias de escape resueltas (ej. `\n` se convierte en un salto de línea real).
    -   Para `true`/`false`, es el booleano `True`/`False`.
    -   Para otros tokens, suele ser el mismo que el `value`.

**Ejemplo:** `let x = 10;` produce un token `NUMBER` con:
-   `type`: `"NUMBER"`
-   `value`: `"10"`
-   `literal`: `10` (un `int`)

## 3. Tokens Reconocidos

El lexer reconoce los siguientes tokens, agrupados por categoría:

#### Palabras Clave
- **Control de Flujo**: `IF`, `ELSE`, `WHILE`, `FOR`, `LOOP`, `BREAK`, `CONTINUE`
- **Declaraciones**: `FN`, `LET`, `MUT`, `RETURN`, `CONST`, `STATIC`
- **Tipos**: `I32`, `I64`, `U32`, `U64`, `F32`, `F64`, `BOOL`, `CHAR`, `STR`, `STRING_TYPE`, `TRUE`, `FALSE`
- **Estructuras**: `STRUCT`, `ENUM`, `MOD`, `USE`, `PUB`, `SELF`, `SELF_TYPE`
- **Traits**: `TRAIT`, `IMPL`, `WHERE`
- **Memoria**: `BOX`, `VEC`, `OPTION`, `SOME`, `NONE`
- **I/O**: `PRINTLN`, `INPUT`, `IN`

#### Literales e Identificadores
- `IDENT`: Nombres de variables, funciones, etc.
- `NUMBER`: Números enteros.
- `FLOAT`: Números de punto flotante.
- `STRING`: Cadenas de texto.

#### Macros
- `CONSOLE_PRINT`: La macro `println!`.
- `VEC_CREATE`: La macro `vec!`.

#### Operadores y Símbolos
- **Aritméticos**: `PLUS` (+), `MINUS` (-), `TIMES` (*), `DIVIDE` (/)
- **Asignación**: `EQUALS` (=), `PLUS_EQUALS` (+=), `MINUS_EQUALS` (-=), `TIMES_EQUALS` (*=), `DIVIDE_EQUALS` (/=)
- **Comparación**: `EQ` (==), `NEQ` (!=), `LT` (<), `LTE` (<=), `GT` (>), `GTE` (>=)
- **Lógicos**: `AND` (&&), `OR` (||), `NOT` (!)
- **Otros**: `ARROW` (->)

#### Delimitadores
- `LPAREN` ((), `RPAREN` ()), `LBRACE` ({), `RBRACE` (}), `LBRACKET` ([), `RBRACKET` (])
- `SEMICOLON` (;), `COLON` (:), `COMMA` (,)

#### Errores y Comentarios
- `ERROR`: Para caracteres no reconocidos.
- `COMMENT`: (Ignorado) Comentarios de una o varias líneas.


## 4. Reglas Especiales y Manejo de Errores

### Reglas de Prioridad para Macros
Para reconocer `println!` o `vec!` como un solo token en lugar de dos (`println` y `!`), se definen reglas específicas para estos patrones. En PLY, el orden de las reglas importa. Las reglas definidas como funciones tienen prioridad sobre las definidas como variables. Entre funciones, la que aparece primero en el archivo tiene prioridad si ambas pueden coincidir.

Por ello, las funciones `t_CONSOLE_PRINT` y `t_VEC_CREATE` están definidas **antes** que la regla genérica `t_identifier`.

```python
# Reglas para macros específicas (deben ir ANTES de t_identifier)
def t_CONSOLE_PRINT(t):
    r'println!'
    t.literal = t.value
    return t

def t_VEC_CREATE(t):
    r'vec!'
    t.literal = t.value
    return t

# Regla genérica para identificadores
def t_identifier(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    # ...
```
Esto asegura que el lexer intente hacer coincidir `println!` primero. Si no lo logra, pasará a la siguiente regla, `t_identifier`, como respaldo.

### Manejo de Errores
Cuando el lexer encuentra un carácter que no encaja en ninguna regla (ej. `#`, `$`), se invoca la función `t_error(t)`. Nuestra implementación:
1.  **No se detiene**: El lexer no aborta.
2.  **Crea un Token `ERROR`**: En lugar de ignorar el carácter, la función construye y retorna un token especial.
    -   `type`: `"ERROR"`
    -   `value`: El carácter problemático (ej. `'#'`).
    -   `literal`: Un mensaje de error descriptivo (ej. `"Illegal character '#'`)
3.  **Avanza**: Llama a `t.lexer.skip(1)` para avanzar al siguiente carácter y continuar la tokenización.

Esto permite que la interfaz de usuario reciba y muestre una lista completa de errores léxicos en una sola pasada.

## 5. Salida para el Parser

La función `tokenize_source` entrega al parser (o a cualquier otro consumidor) una `list` de diccionarios (los tokens). Esta es la estructura de datos final y el "contrato" que el parser debe esperar.

**Ejemplo de Salida para `vec![1]`:**
```json
[
  { "type": "VEC_CREATE", "value": "vec!", "line": 1, "column": 0, "literal": "vec!" },
  { "type": "LBRACKET", "value": "[", "line": 1, "column": 4, "literal": "[" },
  { "type": "NUMBER", "value": "1", "line": 1, "column": 5, "literal": 1 },
  { "type": "RBRACKET", "value": "]", "line": 1, "column": 6, "literal": "]" }
]
```

## 6. Consideraciones para Agregar Nuevos Tokens

Extender el lexer es un proceso sencillo si se siguen los patrones establecidos.

#### Caso 1: Nuevo Keyword (ej. `async`)

1.  **Añadir el nombre del token** a la tupla `tokens`.
    ```python
    "STATIC", "ASYNC", # ...
    ```
2.  **Añadir la palabra reservada** al diccionario `reserved`.
    ```python
    "static": "STATIC",
    "async": "ASYNC",
    # ...
    ```
La regla `t_identifier` se encargará del resto.

#### Caso 2: Nuevo Símbolo Simple (ej. `^` para XOR)

1.  **Añadir el nombre del token** a la tupla `tokens` (ej. `XOR`).
2.  **Añadir la regla simple** junto a las otras. La expresión regular debe escapar caracteres especiales.
    ```python
    t_NOT = r"!"; t_LT = r"<"; t_GT = r">"; t_XOR = r"\^")
    ```

#### Caso 3: Nueva Macro (ej. `panic!`)

1.  **Añadir el nombre del token** a la tupla `tokens` (ej. `PANIC_MACRO`).
2.  **Crear una nueva función de regla** para la macro. **Es crucial colocarla antes de `t_identifier`**.
    ```python
    def t_PANIC_MACRO(t):
        r'panic!'
        t.literal = t.value
        return t

    # ...después va t_identifier...
def t_identifier(t):
#...
    ```
