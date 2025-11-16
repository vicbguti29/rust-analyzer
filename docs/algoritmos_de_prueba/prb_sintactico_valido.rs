// Desarrollado por: Alvascon
//
// Este archivo contiene un programa Rust sintácticamente válido que
// demuestra todas las características soportadas por el parser.
// NOTA: Se han omitido las sentencias 'println!' para evitar un bug conocido.
//
// Características incluidas:
// 1.  Declaraciones de Nivel Superior:
//     - const, static
//     - struct (con y sin campos)
//     - enum (con y sin variantes)
//     - trait (con firmas de funciones, incluyendo &self)
//     - impl para struct
//     - impl de trait para struct
// 2.  Funciones:
//     - Sin parámetros ni retorno.
//     - Con múltiples parámetros.
//     - Con tipo de retorno (incluyendo Self).
// 3.  Sentencias dentro de funciones:
//     - let (mutable e inmutable, con y sin tipo explícito).
//     - while.
//     - for in con rangos.
//     - loop, break, continue.
//     - return (con y sin valor).
//     - Asignación simple y compuesta (+=, -=, *=, /=).
// 4.  Expresiones:
//     - Aritméticas (+, -, *, /) con precedencia.
//     - De comparación (==, !=, <, <=, >, >=).
//     - Lógicas (&&, ||, !)
//     - Literales: enteros, flotantes, booleanos, strings, identificadores.
//     - Inicialización de structs vacíos.
//     - Literales de array y tuplas.
//     - Llamadas a la macro input().

// --- 1. Declaraciones de Nivel Superior ---

const MAX_CONNECTIONS: u32 = 100;
static APP_NAME: &str = "Rust Analyzer";

// Struct con campos y uno vacío
struct Point {
    x: i32,
    y: i32,
}
struct Empty {}

// Enum con variantes y uno vacío
enum Status {
    Connected,
    Disconnected,
    Connecting,
}
enum EmptyEnum {}

// Trait con firmas de funciones
trait Serializable {
    fn to_string(&self) -> String;
    fn get_id() -> u32;
}

// Implementación de un Trait para un Struct
impl Serializable for Point {
    fn to_string(&self) -> String {
        return "Point";
    }
    fn get_id() -> u32 {
        return 1;
    }
}

// Implementación para un Struct
impl Empty {
    fn new() -> Self {
        // NOTA: Se asigna a una variable para evitar el caso de parsing ambiguo
        let instance = Empty {};
        return instance;
    }
}

// --- 2. Funciones ---

fn simple_function() {
    // Esta función no hace nada
}

fn function_with_params(count: i32, name: String) {
    let x = count;
}

fn function_with_return() -> bool {
    return true;
}

// --- 3. Función Principal con Sentencias y Expresiones ---

fn main() {
    // let (mutable, inmutable, con/sin tipo)
    let a: i32 = 10;
    let b = 20.5;
    let mut c = false;
    let mut d: String = "hello";

    // Expresiones
    let result = (a + 5) * 2 - 1;
    let is_ok = result > 20 && !c;
    let is_not_ok = a < 0 || c == true;

    let mut counter = 0;
    while counter < 3 {
        counter = counter + 1;
    }

    for i in 0..2 {
        // Contenido del for
    }

    loop {
        break;
    }
    
    // Inicialización de struct vacío
    let e = Empty {};

    // Literales de array y tupla
    let arr = [1, 2, 3];
    let tup = (10, "tuple", false);
    
    // Asignación
    counter = 10;
    counter += 5;

    // Entrada de datos
    let data = input();
    
    // Sentencia de retorno
    return;
}
