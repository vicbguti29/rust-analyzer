# Manual Técnico del Analizador Sintáctico (Parser)

## 1. Introducción

Este documento proporciona un resumen técnico del estado actual del analizador sintáctico para nuestro compilador de Rust. El parser, construido con `ply.yacc`, es responsable de tomar la secuencia de tokens del analizador léxico y verificar si el código fuente se adhiere a la gramática definida, construyendo un Árbol de Sintaxis Abstracta (AST) como resultado.

El parser ha sido extensamente refactorizado y depurado para soportar un subconjunto significativo de Rust, con un enfoque en la robustez, la eliminación de ambigüedades y la correcta gestión de las estructuras gramaticales.

## 2. Características Soportadas

El parser actualmente reconoce y analiza correctamente las siguientes construcciones del lenguaje:

### 2.1. Declaraciones de Nivel Superior
- **Constantes y Estáticas:** `const NAME: type = value;`, `static NAME: type = value;` y `static mut NAME: type = value;`.
- **Structs:** Definiciones con campos (`struct Point { x: i32, }`) y structs unitarios (`struct Empty {}`). Soporta comas finales.
- **Enums:** Definiciones con variantes (`enum Color { Red, Green, }`) y enums vacíos.
- **Traits:** Definiciones de `trait` con firmas de funciones, incluyendo parámetros `&self`.
- **Bloques `impl`:**
  - Implementación directa para un struct: `impl MyStruct { ... }`.
  - Implementación de un trait para un struct: `impl MyTrait for MyStruct { ... }`.

### 2.2. Sistema de Tipos
- **Tipos Primitivos:** `i32`, `i64`, `u32`, `u64`, `f32`, `f64`, `bool`, `char`.
- **Tipos de String:** `str` y `String`.
- **Tipos de Referencia:** Soporte para referencias simples, como `&str`.
- **Tipo `Self`:** Reconocimiento del tipo `Self` en los cuerpos de `impl` y `trait`.

### 2.3. Sentencias (Statements)
- **Declaración de Variables:**
    - Con inicialización: `let x = ...;` y `let mut x = ...;`.
    - Sin inicialización: `let x: i32;` (requiere tipo explícito).
- **Estructuras de Control:**
  - `if-else`.
  - Bucles `while`, `for i in range`, y `loop`.
  - Sentencias de control de bucle: `break;` y `continue;`.
- **Retorno de Funciones:** `return;` y `return <expr>;`.
- **Asignación:** Asignación simple (`=`) y compuesta (`+=`, `-=`, `*=`, `/=`).

### 2.4. Expresiones (Expressions)
- **Operadores:** Aritméticos (`+`, `-`, `*`, `/`, `%`), de comparación (`==`, `!=`, etc.) y lógicos (`&&`, `||`, `!`), respetando la precedencia.
- **Literales:** Números, strings, booleanos.
- **Estructuras de Datos:**
    - **Tuplas:** `(1, "hola", true)`.
    - **Arrays:** `[1, 2, 3]` y con sintaxis de repetición `[0; 10]`.
- **Inicialización de Structs:** `MiStruct { campo1: valor1, ... }`.
- **Macro `input()`:** La llamada `input()` es reconocida como una expresión válida.
- **Closures (Funciones Lambda):** Se soporta una sintaxis completa:
    - Sin argumentos: `|| expr` o `|| { stmts }`.
    - Con argumentos (con o sin tipo): `|a, b| expr` o `|a: i32, b: i32| expr`.
    - Con tipo de retorno explícito: `|a| -> i32 { ... }`.
    - Con cuerpo de bloque o de expresión.

## 3. Generación del Árbol de Sintaxis Abstracta (AST)

El objetivo principal del parser es construir un AST. Este árbol representa la estructura jerárquica del código usando **tuplas de Python** anidadas.

**Ejemplo de AST para `let x = || 10;`:**
```python
('program', [
    ('let', 'x', None, 
        ('closure', [], None, ('literal', 10, 'NUMBER')), 
    'line_no')
])
```
- **`('closure', params, return_type, body)`:** Es el nodo para una closure.
  - `params`: Una lista de los parámetros.
  - `return_type`: El tipo de retorno si es explícito, o `None`.
  - `body`: La expresión o bloque que forma el cuerpo.

## 4. Estado de la Gramática y Mejoras

La gramática del parser ha sido **significativamente refactorizada** para mejorar su estabilidad y corregir errores críticos.

- **Reducción de Conflictos:** El número de conflictos `shift/reduce` en la gramática se ha reducido drásticamente **de 92 a solo 1**. Esto indica una gramática mucho menos ambigua y más robusta.

- **Solución de Bugs Críticos:** Los dos bugs más importantes que afectaban la versión anterior del parser han sido **solucionados**:
    1.  **Conflicto en `if-else` (SOLUCIONADO):** El error que impedía usar `println!` y otras sentencias dentro de bloques `if-else` complejos ha sido eliminado.
    2.  **Ambigüedad en `return` (SOLUCIONADO):** La ambigüedad que afectaba a `return MiStruct {};` también fue resuelta.

- **Causa de la Mejora:** La solución a ambos problemas se logró introduciendo una regla `initializer` dedicada. Esta regla desambigua la inicialización de structs (`MiStruct {}`) de otros usos de identificadores, lo que resolvió la cascada de conflictos en la gramática.

## 5. Limitaciones Conocidas

- **Bloques que devuelven Expresiones:** El parser actual no soporta la característica de Rust donde un bloque de código devuelve implícitamente el valor de su última expresión si esta no lleva punto y coma.
  - **No Soportado:** `let x = { let y = 5; y };`
  - **Soportado:** `let x = { let y = 5; return y; };`
- **Llamada a Closures:** La sintaxis para *llamar* a una variable que contiene una closure (ej. `mi_closure(5)`) no está implementada. El parser solo reconoce su declaración.
