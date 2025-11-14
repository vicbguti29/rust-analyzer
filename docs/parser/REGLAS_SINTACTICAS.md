# Reglas Sintácticas del Analizador Sintáctico (Parser) Rust

**Autor:** Victor Borbor (@vicbguti29)  
**Fecha:** 13-11-2025  
**Herramienta:** PLY (Python Lex-Yacc)

---

## Introducción

Este documento describe las **reglas sintácticas definidas** en el analizador sintáctico (`ply_parser.py`) para el lenguaje Rust. El parser implementa la gramática BNF necesaria para validar la estructura sintáctica del código.

**Nota:** Las reglas de funciones avanzadas, clases, métodos, traits e implementaciones están asignadas a otro compañero. Este parser solo incluye reglas básicas.

---

## Reglas Sintácticas Definidas

### 1. ASIGNACIÓN DE VARIABLES CON TODOS LOS TIPOS

**Descripción:** Declaración de variables inmutables, mutables, constantes y estáticas con soporte para tipos explícitos.

**Función:** `p_var_decl()`

**Tipos soportados:**
- `i32`, `i64`, `u32`, `u64` (enteros con/sin signo)
- `f32`, `f64` (punto flotante)
- `bool`, `char` (booleano, carácter)
- `str`, `String` (cadenas)

**Sintaxis soportada:**
```rust
let x = 5;                      // Inferencia de tipo
let x: i32 = 5;                // Tipo explícito
let mut x = 10;                // Mutable
let mut x: i32 = 10;           // Mutable con tipo
const MAX: u32 = 100;          // Constante
static COUNTER: i32 = 0;       // Variable estática
```

**Ejemplos válidos:**
```rust
let edad: u32 = 25;
let temperatura: f64 = 37.5;
let activo: bool = true;
let inicial: char = 'A';
const TAMAÑO: i32 = 1024;
static VERSION: i32 = 1;
```

---

### 2. EXPRESIONES ARITMÉTICAS CON UNO O MÁS OPERADORES

**Descripción:** Soporte para expresiones matemáticas con múltiples operadores respetando precedencia.

**Función:** `p_expr_binop()`

**Operadores soportados:**
- Suma: `+`
- Resta: `-`
- Multiplicación: `*`
- División: `/`

**Sintaxis soportada:**
```rust
expr := expr + expr
      | expr - expr
      | expr * expr
      | expr / expr
      | (expr)
```

**Ejemplos válidos:**
```rust
let suma = 10 + 5;
let resta = 20 - 7;
let mult = 4 * 5;
let div = 100 / 2;
let resultado = 10 + 5 * 2;     // Respeta precedencia
let valor = (15 - 3) * (8 + 2); // Con paréntesis
```

---

### 3. CONDICIONES CON UNO O MÁS CONECTORES LÓGICOS

**Descripción:** Expresiones booleanas con operadores lógicos y de comparación.

**Funciones:** `p_expr_and()`, `p_expr_or()`, `p_expr_not()`, `p_expr_cmp()`

**Operadores lógicos:**
- AND: `&&`
- OR: `||`
- NOT: `!`

**Operadores de comparación:**
- Igual: `==`
- No igual: `!=`
- Menor: `<`
- Menor o igual: `<=`
- Mayor: `>`
- Mayor o igual: `>=`

**Sintaxis soportada:**
```rust
condition := expr && expr         // AND lógico
           | expr || expr         // OR lógico
           | !expr                // NOT lógico
           | expr == expr         // Comparación
           | expr != expr
           | expr < expr
           | expr <= expr
           | expr > expr
           | expr >= expr
```

**Ejemplos válidos:**
```rust
if x > 0 && y < 100 { }          // AND
if edad < 18 || edad >= 65 { }   // OR
if !es_bloqueado { }             // NOT
if x == 5 { }                    // Comparación
if (x > 0 && y < 10) || z == 0 { } // Combinado
```

---

### 4. ESTRUCTURA DE CONTROL: if-else

**Descripción:** Control de flujo condicional simple y con alternativa.

**Función:** `p_if_simple()`, `p_if_else()`

**Sintaxis soportada:**
```rust
if condition {
    statements
}

if condition {
    statements
} else {
    statements
}
```

**Ejemplos válidos:**
```rust
if num > 0 {
    println!("Positivo");
}

if edad < 13 {
    println!("Niño");
} else {
    println!("Adulto");
}

if x > 0 && y < 100 {
    println!("Dentro de rango");
}
```

---

### 5. ESTRUCTURA DE DATOS: struct

**Descripción:** Definición de estructuras de datos con campos tipados.

**Función:** `p_struct_decl()`, `p_field()`

**Sintaxis soportada:**
```rust
struct Nombre {
    campo1: tipo1,
    campo2: tipo2,
    ...
}

struct Nombre { }  // Vacío
```

**Ejemplos válidos:**
```rust
struct Persona {
    nombre: String,
    edad: u32,
    altura: f64
}

struct Punto {
    x: i32,
    y: i32
}

struct Vacio { }
```

---

### 6. DEFINICIÓN DE FUNCIÓN

**Descripción:** Declaración de funciones con parámetros y tipos de retorno opcionales.

**Función:** `p_fn_full()`, `p_fn_no_return()`, `p_fn_empty_params()`, etc.

**Sintaxis soportada:**
```rust
fn nombre(param1: tipo1, param2: tipo2) -> tipo_retorno {
    statements
}

fn nombre(param1: tipo1) {
    statements
}

fn nombre() -> tipo_retorno {
    statements
}

fn nombre() {
    statements
}
```

**Ejemplos válidos:**
```rust
fn sumar(a: i32, b: i32) -> i32 {
    a + b
}

fn saludar(nombre: String) {
    println!("Hola {}", nombre);
}

fn main() {
    println!("Programa iniciado");
}
```

---

### 7. IMPRESIÓN: println!

**Descripción:** Macro para imprimir texto en la salida estándar.

**Función:** `p_print_stmt()`

**Sintaxis soportada:**
```rust
println!("texto");
println!("formato {}", expresion);
println!("múltiples {} {}", expr1, expr2);
```

**Ejemplos válidos:**
```rust
println!("Hola, mundo");
println!("El valor de x es: {}", x);
println!("x={}, y={}", x, y);
println!("Resultado: {}", resultado);
```

---

### 8. INGRESO DE DATOS: input()

**Descripción:** Lectura de entrada desde teclado.

**Función:** `p_input_stmt()`

**Sintaxis soportada:**
```rust
let variable = input();
let mut variable = input();
```

**Ejemplos válidos:**
```rust
let numero = input();
let mut nombre = input();
```

---

## Estructura General de la Gramática

### Regla Principal
```
program := items
         | empty

items := item
       | items item

item := function_decl
      | struct_decl
      | var_decl
```

### Manejo de Errores

El parser captura errores sintácticos mediante la función `p_error()`:
- Registra el número de línea del error
- Almacena el token inesperado
- Permite continuar con el análisis
- Genera archivo de log detallado

---

## Precedencia de Operadores

```
1. OR        (||)    - Menor precedencia
2. AND       (&&)
3. ==, !=, <, <=, >, >=
4. +, -
5. *, /      - Mayor precedencia
6. NOT       (!)
```

---

## Archivo de Log

Cada análisis genera un archivo de log con formato:
```
sintactico-vicbguti29-ddmmyyyy-hhmm.txt
```

Contenido:
- Fecha y hora del análisis
- Código fuente analizado
- Cantidad de errores encontrados
- Detalle de cada error (línea, mensaje, token)

---

## Ejemplo de Programa Válido

```rust
struct Persona {
    nombre: String,
    edad: u32
}

fn calcular_edad(anio_actual: i32, anio_nacimiento: i32) -> i32 {
    anio_actual - anio_nacimiento
}

fn main() {
    let x: i32 = 10;
    let mut y: i32 = 20;
    
    println!("Valores iniciales");
    
    if x > 0 && y > 0 {
        let suma = x + y;
        println!("Suma: {}", suma);
    }
    
    y = y + 5;
}
```

---

## Referencias

- [PLY Documentation](https://ply.readthedocs.io/)
- [The Rust Programming Language](https://doc.rust-lang.org/book/)
- [Yacc/Bison Manual](https://www.gnu.org/software/bison/manual/)
