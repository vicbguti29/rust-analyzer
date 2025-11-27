// docs/algoritmos_de_prueba/prb_semantico.rs
// Archivo de prueba para el Analizador Semántico.
// Contiene casos válidos e inválidos para las reglas de tipado.

// Structs para pruebas semánticas
struct Vec2 {}
struct Color {}

// Pruebas para const y static
const MAX_POINTS: i32 = 100;
static LIVES: i32 = 3;
static mut COUNTER: i32 = 0;

fn main() {
    // --- Casos Válidos ---

    // Declaración explícita correcta
    let a: i32 = 10;
    let b: f64 = 20.5;
    let c: bool = true;
    let d: &str = "hello";

    // Declaración implícita (el tipo se infiere)
    let e = 50;
    let f = false;

    // Reasignación correcta a una variable mutable
    let mut g = 100;
    g = 200;

    let mut h = "texto";
    h = "otro texto";


    // --- Casos Inválidos (el analizador semántico debería detectarlos) ---

    // Regla 1: Discrepancia de tipos en la declaración explícita
    let error1: i32 = "esto no es un i32";
    let error2: bool = 1;


    // Regla 2: Discrepancia de tipos en la reasignación
    let mut error3 = 500;
    error3 = true; // Error: se esperaba i32, se encontró bool

    let mut error4 = "hola";
    error4 = 123; // Error: se esperaba &str, se encontró i32

    
    // --- Nuevos Casos de Prueba para Structs, Arrays y Tuplas ---

    // Structs
    let v1 = Vec2 {};
    let mut v2 = Vec2 {};
    v2 = v1; // Válido

    let c1: Color = Vec2 {}; // Error: se esperaba Color, se encontró Vec2
    let mut v3 = Vec2 {};
    v3 = Color {}; // Error: se esperaba Vec2, se encontró Color

    // Arrays y Tuplas (con tipos inferidos)
    let arr1 = [1, 2, 3];
    let tup1 = (10, true);
    let mut arr2 = [10, 20];
    arr2 = [30, 40]; // Válido

    let mut arr3 = [1.0, 2.0];
    arr3 = [1, 2]; // Error: se esperaba [f64; 2], se encontró [i32; 2]
    
    let mut tup2 = (10, false);
    tup2 = (10, "hello"); // Error: se esperaba (i32, bool), se encontró (i32, &str)

    // Regla de Mutabilidad: Reasignación a variable inmutable
    let immutable_var = 1000;
    immutable_var = 2000; // Error: 'immutable_var' no es mutable.

    // --- Pruebas para const y static ---
    MAX_POINTS = 105; // Error: no se puede reasignar a una constante.
    LIVES = 4; // Error: no se puede reasignar a una variable static inmutable.
    COUNTER = 1; // Válido: COUNTER es static mut.

    // --- Pruebas para nuevos tokens ---
    let modulo_result = 10 % 3; // Válido
    
    print!("Esto es un print sin salto de línea.");
    eprint!("Esto es un eprint.");
    eprintln!("Esto es un eprintln con salto de línea.");

    // --- Pruebas para variables no inicializadas ---
    // Caso válido
    let mut valid_uninit: i32;
    valid_uninit = 50;
    let some_var = valid_uninit + 10; // Válido, se usa después de inicializar

    // Caso inválido
    let invalid_uninit: i32;
    let another_var = invalid_uninit + 5; // Error: 'invalid_uninit' no ha sido inicializada

    // --- Pruebas para la sintaxis de array [valor; tamaño] ---
    let array_repeat = [0; 5]; // Válido
    let array_repeat_error = [0; false]; // Error: el tamaño debe ser un entero

    // --- Pruebas Semánticas para Closures ---

    // Caso Válido: La closure se asigna a una variable
    let mi_closure = |a: i32, b: i32| -> i32 {
        return a + b;
    };

    // Caso Válido: Uso de variable del scope exterior
    let factor = 10;
    let multiplicar = |n| n * factor;
    // let resultado_closure = multiplicar(5); // Llamada a closure no soportada por el parser aún

    // --- Casos que DEBERÍAN producir errores semánticos (una vez implementado) ---

    // Error Semántico: Usar una variable no definida dentro de la closure
    let error_closure_1 = || z + 1; 

    // Error Semántico: Discrepancia de tipos en el cuerpo de la closure
    let error_closure_2 = |a: i32| -> i32 {
        return "no soy un i32";
    };

    // Error Semántico: Uso de variable no inicializada dentro de la closure
    let error_closure_3 = || {
        let x: i32;
        return x; // 'x' no está inicializada
    };
}
