// test_sintactico.rs
// Código Rust para prueba del analizador sintáctico
// Desarrollador: vicbguti29
// 
// RESPONSABILIDADES ASIGNADAS:
// - Impresión (println!)
// - Ingreso de datos (input)
// - Expresiones aritméticas con uno o más operadores
// - Condiciones con uno o más conectores lógicos
// - Asignación de variables con todos los tipos
// - Mínimo: 1 estructura de datos, 1 estructura de control, 1 función

// ============================================================================
// REGLA 1: ASIGNACIÓN DE VARIABLES CON TODOS LOS TIPOS
// ============================================================================

// Variables inmutables con tipo explícito
let x: i32 = 42;
let pi: f64 = 3.14159;
let is_active: bool = true;
let letra: char = 'A';

// Variables mutables
let mut count: i32 = 0;
let mut temperatura: f64 = 25.5;

// Constantes
const MAX_SIZE: u32 = 100;
const GRAVITY: f64 = 9.8;

// Variables estáticas
static COUNTER: i32 = 0;

// ============================================================================
// REGLA 2: EXPRESIONES ARITMÉTICAS CON UNO O MÁS OPERADORES
// ============================================================================

let suma = 10 + 5;
let resta = 20 - 7;
let multiplicacion = 4 * 5;
let division = 100 / 2;

// Expresiones con múltiples operadores (precedencia)
let resultado = 10 + 5 * 2;
let valor = (15 - 3) * (8 + 2);
let operacion_compleja = 100 / 2 + 5 * 3 - 10;

// ============================================================================
// REGLA 3: CONDICIONES CON UNO O MÁS CONECTORES LÓGICOS
// ============================================================================

// Condición con AND lógico
if x > 0 && y < 100 {
    println!("x es positivo AND y es menor a 100");
}

// Condición con OR lógico
if edad < 18 || edad >= 65 {
    println!("Descuento aplicable");
}

// Condición con NOT lógico
if !es_bloqueado {
    println!("Acceso permitido");
}

// Condiciones complejas con múltiples conectores
if (x > 5 && y < 10) || (z == 0) {
    println!("Condición compleja cumplida");
}

// ============================================================================
// REGLA 4: ESTRUCTURAS DE CONTROL - if (MÍNIMO 1)
// ============================================================================

// Control if-else simple (RESPONSABILIDAD DE vicbguti29)
if num > 0 {
    println!("Número positivo");
} else {
    println!("Número no positivo");
}

// TODO: while, for, loop - A CARGO DE COMPAÑERO
// TODO: if-else if-else - A CARGO DE COMPAÑERO

// ============================================================================
// REGLA 5: ESTRUCTURA DE DATOS - struct (MÍNIMO 1)
// ============================================================================

struct Persona {
    nombre: String,
    edad: u32,
    altura: f64
}

// TODO: Otras estructuras de datos - A CARGO DE COMPAÑERO

// ============================================================================
// REGLA 6: DEFINICIÓN DE FUNCIONES (MÍNIMO 1)
// ============================================================================

// Función sin parámetros y sin retorno (RESPONSABILIDAD DE vicbguti29)
fn saludar() {
    println!("Hola desde la función saludar");
}

// TODO: Funciones con parámetros y retorno - A CARGO DE COMPAÑERO
// TODO: Funciones con múltiples parámetros - A CARGO DE COMPAÑERO

// ============================================================================
// REGLA 7: IMPRESIÓN (println!) - RESPONSABILIDAD DE vicbguti29
// ============================================================================

println!("Mensaje simple");
println!("El valor de x es: {}", x);
println!("Valores: x={}, y={}", x, y);
println!("Resultado: {}", suma);

// ============================================================================
// REGLA 8: ENTRADA DE DATOS (input) - RESPONSABILIDAD DE vicbguti29
// ============================================================================

let numero = input();
let mut dato = input();

// ============================================================================
// REGLA 9: REASIGNACIÓN DE VARIABLES - RESPONSABILIDAD DE vicbguti29
// ============================================================================

x = 100;
count = 50;

// Operadores de asignación compuesta
count += 5;
temperatura -= 2.5;
multiplicador *= 2;
divisor /= 3;

// ============================================================================
// FUNCIÓN MAIN
// ============================================================================

fn main() {
    let x: i32 = 5;
    let mut y: i32 = 10;
    
    // Impresión
    println!("Iniciando programa");
    
    // Condicional con conectores lógicos
    if x > 0 && y > 0 {
        let suma = x + y;
        println!("La suma es: {}", suma);
    }
    
    // TODO: Bucles (while, for, loop) - A CARGO DE COMPAÑERO
    
    // Ingreso de datos
    let numero_ingresado = input();
    
    println!("Programa finalizado");
}
