# Manual Técnico del Analizador Semántico

Este documento detalla la arquitectura, el funcionamiento y las reglas implementadas en el analizador semántico del compilador de Rust.

## 1. Arquitectura y Enfoque de Diseño

Para el análisis semántico, hemos adoptado el enfoque de **"Análisis Semántico basado en un Recorrido del AST"** (AST-walking), que es el estándar en la industria y la arquitectura utilizada por compiladores modernos como `rustc`, `Clang` y `gcc`.

### 1.1. ¿Cómo funciona este enfoque?

El proceso se divide en dos fases claras e independientes:

1.  **Fase de Parsing (Análisis Sintáctico):** El parser, construido con `ply.yacc`, tiene una única responsabilidad: validar la gramática del código fuente y construir una representación completa y estructurada del mismo, conocida como **Árbol de Sintaxis Abstracta (AST)**. En esta fase no se toma ninguna decisión sobre el significado del código.

2.  **Fase de Análisis Semántico:** Un componente totalmente separado, nuestra clase `SemanticAnalyzer`, recibe el AST completo. Este analizador "camina" o "visita" cada nodo del árbol, aplicando las reglas semánticas (como la verificación de tipos o de mutabilidad) en cada punto.

### 1.2. ¿Por qué elegimos este enfoque?

Aunque existen otras técnicas, como ejecutar acciones semánticas directamente dentro de las reglas del parser, nuestro enfoque ofrece ventajas significativas para un lenguaje tan complejo como Rust:

-   **Modularidad y Mantenimiento:** Mantiene la lógica del parser y la del análisis semántico completamente separadas. Esto hace que el código sea más limpio, más fácil de entender, de probar y de modificar en el futuro.
-   **Potencia y Flexibilidad:** Al tener el árbol completo desde el principio, el analizador puede tomar decisiones de validación con un contexto global del código, lo que es crucial para las reglas de scope y la resolución de tipos complejos.
-   **Escalabilidad:** Esta arquitectura es la única que permite añadir fácilmente fases posteriores del compilador, como la optimización de código o la generación de código intermedio, ya que todas ellas pueden operar sobre el mismo AST.

---

## 2. Tabla de Símbolos (Pendiente)

*(Esta sección será completada una vez se desarrolle la Tabla de Símbolos).*


*(Aquí se explicará el diseño de la tabla de símbolos, cómo maneja los scopes anidados, y qué información almacena para cada símbolo: tipo, mutabilidad, etc.)*

---

## 3. Reglas Semánticas Implementadas

A continuación se detallan las reglas semánticas implementadas y las que están pendientes.

### 3.1. Reglas Pendientes (vicbguti29)

#### REGLA 1: VALIDACIÓN DE EXISTENCIA

*(Aquí se explicará cómo se utiliza la tabla de símbolos para verificar que una variable ha sido declarada antes de ser utilizada).*

#### REGLA 2: ALCANCE LOCAL (SCOPE)

*(Aquí se explicará la gestión de scopes, asegurando que las variables solo sean accesibles dentro del bloque donde fueron declaradas).*

---

### 3.2. Reglas Implementadas (Alvascon)

#### REGLA 3: DISCREPANCIA DE TIPOS EN DECLARACIÓN

**Descripción:** Esta regla se activa al declarar una variable con una anotación de tipo explícita (ej. `: i32`). Verifica que el tipo de la expresión asignada a la derecha coincida exactamente con el tipo declarado.

-   **Caso Válido:** El tipo de la expresión coincide con el tipo declarado.
    ```rust
    // El valor '10' es de tipo i32, que coincide con la declaración.
    let x: i32 = 10; 
    ```

-   **Caso Inválido:** El tipo de la expresión no coincide con el tipo declarado.
    ```rust
    // Se esperaba un 'bool', pero se asignó un 'i32'.
    let error: bool = 1;
    ```
    **Error Generado:** `Error Semántico (Línea 34): Discrepancia de tipos. Se esperaba tipo 'bool' pero se encontró tipo 'i32' en la asignación de 'error'.`

---

#### REGLA 4: DISCREPANCIA DE TIPOS EN REASIGNACIÓN

**Descripción:** Esta regla se activa al reasignar un valor a una variable mutable. Verifica que el tipo del nuevo valor sea el mismo que el tipo con el que la variable fue declarada originalmente.

-   **Caso Válido:** El nuevo valor tiene el mismo tipo que la variable.
    ```rust
    let mut variable = "hola"; // El tipo de 'variable' se infiere como &str
    variable = "mundo";       // Válido, ambos son &str
    ```

-   **Caso Inválido:** El nuevo valor tiene un tipo diferente al original.
    ```rust
    let mut variable = 123; // El tipo de 'variable' se infiere como i32
    variable = "texto";    // Inválido, se intenta asignar &str a i32
    ```
    **Error Generado:** `Error Semántico (Línea 42): Discrepancia de tipos en la reasignación. La variable 'error4' tiene el tipo '&str', pero se intentó asignar un valor de tipo 'i32'.`

---

#### REGLA 5: VALIDACIÓN DE MUTABILIDAD EN REASIGNACIÓN

**Descripción:** Esta regla garantiza que solo las variables declaradas con la palabra clave `mut` puedan ser reasignadas. Si se intenta modificar una variable inmutable, se genera un error.

-   **Caso Válido:** Se reasigna una variable declarada como mutable.
    ```rust
    let mut variable_mutable = 10;
    variable_mutable = 20; // Válido
    ```

-   **Caso Inválido:** Se intenta reasignar una variable inmutable.
    ```rust
    let variable_inmutable = 1000;
    variable_inmutable = 2000; // Inválido
    ```
    **Error Generado:** `Error Semántico (Línea 70): No se puede asignar a la variable inmutable 'immutable_var'. Las variables deben ser declaradas con 'mut' para poder ser reasignadas.`
