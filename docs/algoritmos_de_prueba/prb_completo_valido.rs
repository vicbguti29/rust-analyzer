// --- Archivo de Prueba Completo y Válido ---
// Este archivo contiene un programa Rust que es léxica, sintáctica y
// semánticamente válido según las capacidades actuales del analizador.
// Debería ser procesado sin generar ningún error.

// --- Declaraciones de Nivel Superior ---

const PI: f64 = 3.14159;
static mut GLOBAL_COUNTER: i32 = 0;

struct Point {
    x: f64,
    y: f64,
}

enum Color {
    Red,
    Green,
    Blue,
}

trait Drawable {
    fn draw(&self);
}

impl Drawable for Point {
    fn draw(&self) {
        println!("Dibujando un punto.");
    }
}

// --- Funciones ---

fn calculate_distance(p1: Point, p2: Point) -> f64 {
    // El cuerpo de las funciones no se analiza semánticamente en profundidad aún,
    // pero la firma es sintácticamente correcta.
    return 0.0;
}

// --- Función Principal ---

fn main() {
    // --- Variables y Tipos ---
    let a: i32 = 10;
    let b = 20.5; // Inferencia de tipo (f64)
    let mut c = true;
    let message = "Hola, mundo!";
    
    // Declaración sin inicialización (válido)
    let mut uninitialized_var: i32;
    uninitialized_var = 100; // Inicialización (válido)
    
    // --- Expresiones ---
    let result = (a + uninitialized_var) * 2 % 3;
    let is_valid = result > 50 && (b <= 20.5 || !c);

    // --- Estructuras de Control ---
    if is_valid {
        println!("Es válido");
    } else {
        println!("No es válido");
    }

    let mut i = 0;
    while i < 3 {
        i += 1;
        if i == 2 {
            continue;
        }
    }

    for j in 0..5 {
        // loop de for
    }
    
    loop {
        break;
    }

    // --- Structs, Arrays y Tuplas ---
    let origin = Point { x: 0.0, y: 0.0 };
    let colors = [Color::Red, Color::Green];
    let repeated_array = [0; 10]; // Sintaxis de array repetido
    let mixed_tuple = (10, "diez", false, 3.0);

    // --- Closures (Sintaxis Válida) ---
    
    // Closure sin argumentos, cuerpo de expresión
    let get_pi = || 3.14;

    // Closure con argumentos sin tipo, cuerpo de expresión
    let add = |x, y| x + y;

    // Closure con argumentos con tipo y tipo de retorno, cuerpo de bloque
    let subtract = |x: i32, y: i32| -> i32 {
        return x - y;
    };
    
    // Asignación a una variable que fue declarada pero no inicializada
    uninitialized_var = 300; // Válido porque 'uninitialized_var' es mutable.

    println!("Fin del programa válido.");
}
