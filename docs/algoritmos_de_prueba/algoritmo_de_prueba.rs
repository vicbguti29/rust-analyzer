// codigo de prueba de Angello VAsconez (Alvasconv)

// --- Ejemplo de Código Rust Válido ---
// Este archivo contiene únicamente sintaxis
// reconocida por el lexer actual.

/*
  Bloque de comentario multilínea.
  Aquí se define una estructura y funciones.
*/

// Uso del operador de ámbito (SCOPE)
use std::vec;

// Definición de una estructura simple
struct Coordenada {
    x: i32,
    y: i32,
}

// Definición de una función con flecha (ARROW)
fn sumar(a: i32, b: i32) -> i32 {
    return a + b;
}

fn main() {
    // Declaración de variables con let, mut y const
    let inmutable = 100;
    let mut mutable = 20.5;
    const PI: f64 = 3.1416;

    // Instanciación de la estructura
    let origen: Coordenada = Coordenada { x: 0, y: 0 };

    // Operadores aritméticos y de asignación
    mutable = mutable + 10.0;
    let producto = inmutable * 2;
    let division = 100 / 5;

    // Uso de operadores de comparación y lógicos
    if producto > 150 {
        // String con secuencias de escape
        let mensaje = "El producto es mayor\ny usa el ampersand &.";
    } else {
        // Bucle simple
        loop {
            break;
        }
    }

    // Llamada a función
    let resultado_suma = sumar(5, 3);
}

