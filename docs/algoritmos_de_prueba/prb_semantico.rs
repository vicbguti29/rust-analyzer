// docs/algoritmos_de_prueba/prb_semantico.rs
// Archivo de prueba para el Analizador Semántico.
// Contiene casos válidos e inválidos para las reglas de tipado.

// Structs para pruebas semánticas
struct Vec2 {}
struct Color {}

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
}
