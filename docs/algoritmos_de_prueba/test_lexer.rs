// test_lexer.rs
// Código de prueba con sintaxis de Rust (VICTOR BORBOR)

// Módulo y uso de tipos
mod math {
    pub fn calculate(x: i32) -> i32 {
        return x * 2;
    }
}

use std::vec::Vec;

// Definición de struct y enum
struct Point {
    x: f64,
    y: f64
}

enum Option<T> {
    Some(T),
    None
}

// Implementación de trait
trait Shape {
    fn area(&self) -> f64;
}

// Función principal con control de flujo
fn main() {
    // Variables y tipos
    let mut count: i32 = 0;
    let pi: f64 = 3.14;
    const MAX_POINTS: u32 = 100;
    
    // Estructuras de control
    if count < 10 {
        count += 1;
    } else {
        count = 0;
    }

    // Loop y break
    loop {
        if count >= MAX_POINTS {
            break;
        }
        count += 1;
    }

    // Vector y Option
    let mut numbers: Vec<i32> = Vec::new();
    let maybe_number: Option<i32> = Some(42);
    
    // String con escapes
    let message = "Hello \"Rust\" world!\n";
}
