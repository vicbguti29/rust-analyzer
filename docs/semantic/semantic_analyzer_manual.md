# Manual Técnico del Analizador Semántico

Este documento detalla la arquitectura, el funcionamiento y las reglas implementadas en el analizador semántico del compilador de Rust.

## 1. Arquitectura y Enfoque de Diseño

Para el análisis semántico, hemos adoptado el enfoque de **"Análisis Semántico basado en un Recorrido del AST"** (AST-walking), que es el estándar en la industria y la arquitectura utilizada por compiladores modernos como `rustc`, `Clang` y `gcc`.

### 1.1. ¿Cómo funciona este enfoque?

El proceso se divide en dos fases claras e independientes:

1.  **Fase de Parsing (Análisis Sintáctico):** El parser tiene una única responsabilidad: validar la gramática del código fuente y construir una representación completa y estructurada del mismo, conocida como **Árbol de Sintaxis Abstracta (AST)**.

2.  **Fase de Análisis Semántico:** Un componente totalmente separado, nuestra clase `SemanticAnalyzer`, recibe el AST completo. Este analizador "camina" o "visita" cada nodo del árbol, aplicando las reglas semánticas (como la verificación de tipos o de mutabilidad) en cada punto.

### 1.2. ¿Por qué elegimos este enfoque?

-   **Modularidad y Mantenimiento:** Mantiene la lógica del parser y la del análisis semántico completamente separadas, lo que hace el código más limpio, fácil de probar y de modificar.
-   **Potencia y Flexibilidad:** Al tener el árbol completo desde el principio, el analizador puede tomar decisiones de validación con un contexto global del código, lo que es crucial para las reglas de scope y la resolución de tipos complejos.
-   **Escalabilidad:** Esta arquitectura permite añadir fácilmente fases posteriores del compilador, como la optimización o la generación de código intermedio.

## 2. Tabla de Símbolos (`SymbolTable`)

La Tabla de Símbolos es el componente central del análisis semántico. Es una estructura de datos que rastrea todos los identificadores (variables, funciones, etc.) que están "en scope" en un punto determinado del programa.

### 2.1. Diseño y Gestión de Scopes
Nuestra implementación utiliza una **pila de scopes**.
-   Cada scope (o ámbito) es un diccionario que mapea nombres de identificadores a la información sobre ellos.
-   Cuando el analizador entra en un nuevo bloque de código (como el cuerpo de una función), se "empuja" un nuevo diccionario vacío a la pila (`enter_scope`).
-   Cuando el analizador sale del bloque, el diccionario de ese scope se "saca" de la pila (`exit_scope`), y todas las variables declaradas dentro de él dejan de ser accesibles.
-   La búsqueda de un símbolo (`lookup`) se realiza desde el scope más reciente (el final de la pila) hacia el más antiguo (el global), imitando cómo Rust resuelve los nombres.

### 2.2. Información Almacenada por Símbolo
Para cada identificador, la tabla almacena un diccionario con los siguientes datos:
-   `type`: El tipo de dato de la variable (ej. `'i32'`, `'bool'`).
-   `is_mutable`: Un booleano que indica si la variable fue declarada con `mut`.
-   `is_initialized`: Un booleano para rastrear si a una variable ya se le ha asignado un valor.
-   `scope_level`: El nivel de anidamiento del scope donde fue declarada.
-   `line_declared`: El número de línea donde se realizó la declaración.

## 3. Reglas Semánticas Implementadas

A continuación se detallan las reglas semánticas que el analizador verifica actualmente.

### REGLA 1: VALIDACIÓN DE EXISTENCIA
- **Descripción:** Verifica que cualquier variable utilizada en una expresión haya sido declarada previamente en el scope actual o en uno superior.
- **Error Generado:** `Error Semántico: Identificador no encontrado. La variable 'x' no ha sido declarada.`

### REGLA 2: ALCANCE LOCAL (SCOPE)
- **Descripción:** Asegura que las variables solo sean accesibles dentro del bloque donde fueron declaradas o en bloques anidados. No se puede acceder a una variable de un scope interno desde un scope externo.
- **Error Generado:** `Error Semántico: El identificador 'x' no es accesible. Fue definido en un alcance interno que ya finalizó.`

### REGLA 3: DISCREPANCIA DE TIPOS EN DECLARACIÓN
- **Descripción:** Al declarar una variable con tipo explícito (`let x: T = val;`), verifica que el tipo de `val` coincida con `T`.
- **Error Generado:** `Error Semántico: Discrepancia de tipos. Se esperaba tipo 'bool' pero se encontró tipo 'i32'.`

### REGLA 4: DISCREPANCIA DE TIPOS EN REASIGNACIÓN
- **Descripción:** Al reasignar una variable (`x = nuevo_val;`), verifica que el tipo de `nuevo_val` coincida con el tipo original de `x`.
- **Error Generado:** `Error Semántico: Discrepancia de tipos en la reasignación. La variable 'x' tiene el tipo 'i32', pero se intentó asignar un valor de tipo '&str'.`

### REGLA 5: VALIDACIÓN DE MUTABILIDAD
- **Descripción:** Asegura que solo las variables declaradas con `mut` puedan ser reasignadas. También se aplica a constantes (`const`) y estáticas (`static`) inmutables.
- **Error Generado:** `Error Semántico: No se puede asignar a la variable inmutable 'x'.`

### REGLA 6: USO DE VARIABLES NO INICIALIZADAS
- **Descripción:** Si una variable se declara sin un valor (`let x: i32;`), el analizador la marca como "no inicializada". Se genera un error si se intenta usar en una expresión antes de que se le asigne un valor por primera vez.
- **Error Generado:** `Error Semántico: se usó la variable no inicializada 'x'.`

### REGLA 7: TAMAÑO DE ARRAY INVÁLIDO
- **Descripción:** En la sintaxis de repetición de arrays (`[val; size]`), verifica que la expresión `size` sea de un tipo entero.
- **Error Generado:** `Error Semántico: el tamaño del array debe ser un entero, pero se encontró tipo 'bool'.`

## 4. Limitaciones y Trabajo Futuro

### Análisis Semántico de Closures (Pendiente)
- **Estado Actual:** Aunque el parser reconoce la sintaxis completa de las closures, el analizador semántico **aún no las procesa**.
- **Tareas Pendientes:**
    1.  Implementar la creación de un **nuevo scope** para los parámetros de la closure.
    2.  Añadir los parámetros a la tabla de símbolos dentro de ese scope.
    3.  Realizar la inferencia de tipos para los parámetros no tipados.
    4.  Verificar la consistencia entre el tipo de retorno explícito (`-> T`) y el tipo del valor devuelto por el cuerpo.
    5.  Determinar el tipo de la propia closure (ej. `Fn(i32) -> i32`).