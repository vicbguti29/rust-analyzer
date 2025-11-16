# Resumen Técnico del Analizador Sintáctico (Parser)

## 1. Introducción

Este documento proporciona un resumen técnico del estado actual del analizador sintáctico para nuestro compilador de Rust. El parser, construido con PLY, es responsable de tomar la secuencia de tokens del analizador léxico y verificar si el código fuente se adhiere a la gramática definida, construyendo un Árbol de Sintaxis Abstracta (AST) como resultado.

El parser ha sido desarrollado y depurado para soportar un subconjunto significativo de las características de Rust, con un enfoque en la robustez y la correcta gestión de las estructuras gramaticales.


## 2. Características Soportadas

El parser actualmente reconoce y analiza correctamente las siguientes construcciones del lenguaje:

### 2.1. Declaraciones de Nivel Superior
- **Constantes y Estáticas:** `const NAME: type = value;` y `static NAME: type = value;`.
- **Structs:** Definiciones con campos (`struct Point { x: i32, }`) y structs unitarios (`struct Empty {}`). Soporta comas finales (trailing commas).
- **Enums:** Definiciones con variantes (`enum Color { Red, Green, }`) y enums vacíos (`enum Empty {}`). Soporta comas finales.
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
- **Declaración de Variables:** `let x = ...;` y `let mut x = ...;`, con y sin anotaciones de tipo explícitas.
- **Estructuras de Control:**
  - `if-else` (con bloques no vacíos).
  - Bucles `while`, `for i in range`, y `loop`.
  - Sentencias de control de bucle: `break;` y `continue;`.
- **Retorno de Funciones:** `return;` y `return <expr>;`.
- **Asignación:** Asignación simple (`=`) y compuesta (`+=`, `-=`, `*=`, `/=`).

### 2.4. Expresiones (Expressions)
- **Operadores:** Aritméticos, de comparación y lógicos, respetando la precedencia.
- **Literales:** Números, strings, booleanos, tuplas y arrays.
- **Inicialización de Structs:** Únicamente para structs sin campos (ej. `let e = Empty {};`).
- **Macro `input()`:** La llamada `input()` es reconocida como una expresión válida.

---

## 3. Generación del Árbol de Sintaxis Abstracta (AST)

El objetivo principal del parser, además de validar la sintaxis, es construir un AST. Este árbol representa la estructura jerárquica del código de una manera que es fácil de procesar para las fases posteriores del compilador (como el análisis semántico).

### 3.1. ¿Cómo se genera?

Cada regla de la gramática en el parser (las funciones `p_...`) tiene una acción asociada que define qué estructura de datos crear cuando la regla se cumple. En nuestro caso, hemos usado **tuplas de Python** para representar cada nodo del árbol.

Estas tuplas se anidan unas dentro de otras para formar la estructura completa del programa.

### 3.2. Ejemplo de AST

Tomemos un fragmento de código simple:
```rust
fn main() {
    let x = 10;
}
```

El parser procesa este código y genera la siguiente estructura de AST:

```python
('program', [
    ('fn', 'main', [], None, [
        ('let', 'x', None, ('literal', 10))
    ])
])
```

**Desglose del ejemplo:**

- **`('program', ...)`:** Es el nodo raíz de todo el programa. Su segundo elemento es una lista de todas las declaraciones de nivel superior.
- **`('fn', ...)`:** Representa una declaración de función.
  - `'main'`: Nombre de la función.
  - `[]`: Lista de parámetros (vacía en este caso).
  - `None`: Tipo de retorno (ninguno en este caso).
  - `[...]`: Lista de sentencias que forman el cuerpo de la función.
- **`('let', ...)`:** Representa una declaración de variable.
  - `'x'`: Nombre de la variable.
  - `None`: Tipo de dato (inferido, no explícito).
  - `(...)`: La expresión que se asigna a la variable.
- **`('literal', 10)`:** Representa un valor literal, en este caso el número 10.

Esta estructura anidada es el resultado final del análisis sintáctico y la entrada principal para el analizador semántico.

---

## 4. Limitaciones Actuales y Trabajo Futuro

Durante el desarrollo y la depuración, se identificaron dos bugs complejos relacionados con la forma en que el motor LALR(1) de PLY resuelve conflictos en la gramática.

### 4.1. Conflicto de Gramática en Bloques de Control
- **Descripción:** Se detectó un bug crítico donde el parser falla al analizar sentencias (`println!`, `let`, asignaciones) dentro de un bloque `if-else`, pero solo cuando el bloque está precedido por una combinación específica de otras sentencias complejas.
- **Diagnóstico:** Las pruebas aisladas demuestran que las reglas para `if-else` y para las sentencias individuales son correctas. El problema es un **conflicto de estados** en la gramática, que es difícil de depurar sin herramientas avanzadas.
- **Solución Futura:** La resolución de este bug requerirá probablemente una reescritura significativa de las reglas de expresiones y sentencias para eliminar las ambigüedades que causan el conflicto. Por ahora, se ha documentado con un test que falla (`@pytest.mark.xfail`).

### 4.2. Ambigüedad en `return` con Inicialización de Structs
- **Descripción:** Una sentencia como `return MyStruct {};` no es analizada correctamente.
- **Diagnóstico:** Es un clásico conflicto de ambigüedad. El parser no sabe si debe tratar `MyStruct` como una expresión completa o esperar a las llaves `{}` para formar una inicialización.
- **Solución Futura:** Al igual que el punto anterior, una reestructuración de la gramática de expresiones es necesaria para dar pistas al parser y resolver la ambigüedad.

**Conclusión:** El parser es funcional para una amplia gama de características y proporciona una base sólida para el desarrollo del analizador semántico. Las limitaciones actuales están bien identificadas y documentadas, y su resolución se planea para una futura fase de refactorización del parser.