// --- Archivo de Prueba para el Analizador Léxico ---
// Este archivo contiene ejemplos de la mayoría de tokens válidos
// y varios tokens inválidos para verificar el lexer.

/* 
  Comentario de bloque.
  Keywords: let, mut, const, static, fn, return, if, else, loop, while, for, in, break, continue
  struct, enum, impl, trait, self, Self, true, false.
  Tipos: i32, f64, bool, char, str, String.
  Macros: println!, print!, eprintln!, eprint!
*/

/// Comentario de documentación.

// --- Declaraciones y Palabras Clave ---
const MAX_SIZE: i32 = 100;
static mut COUNTER: i32 = 0;

fn mi_funcion(param: i32) -> bool {
    let mut variable: bool = false;
    if variable == true {
        // no hacer nada
    } else {
        // tampoco
    }
    return variable;
}

struct MiStruct {}
enum MiEnum {}
trait MiTrait {}
implement MiTrait for MiStruct {}

// --- Expresiones y Operadores ---
fn main() {
    let x = (10 + 20) * 3 / 2 - 1;
    let y = 10 % 3;
    let z = x > y && y <= 1 || !false;
    let range = 0..100;
    
    let mut a = 10;
    a += 5;
    a -= 1;
    a *= 2;
    a /= 3;

    // --- Literales y Otros ---
    let mi_string = "hola\nmundo";
    let mi_char = 'c';
    let mi_float = 3.14159;
    let mi_array = [1, 2, 3];
    let mi_closure = |a: i32| a + 1;
    let mi_closure_vacia = || 1;
    let referencia = &x;
    
    // --- Macros de Impresión ---
    println!("Hola");
    print!("Mundo");
    eprintln!("Error");
    eprint!("Grave");
    
    // --- Caracteres Inválidos ---
    // El lexer debería reportar errores para los siguientes caracteres:
    @ $ ? #
}