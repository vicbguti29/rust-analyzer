// prb_input_teclado.rs
// Prueba de la regla: Solicitar Datos por Teclado
// Esta prueba valida el correcto funcionamiento de la lectura de entrada desde teclado
// usando io::stdin().read_line()

// ============================================================================
// PARTE 1: CÓDIGO VÁLIDO - Ejemplos correctos de input
// ============================================================================

fn main() {
    // Ejemplo 1: Lectura simple de entrada
    let mut buffer = String::new();
    println!("Ingrese un número:");
    
    // Ejemplo 2: Declaración y uso de String::new()
    let mut nombre = String::new();
    println!("Ingrese su nombre:");
    
    // Ejemplo 3: Referencia mutable a variable
    let mut edad = String::new();
    let ref_edad = &mut edad;
    
    // Ejemplo 4: Uso de String como tipo en parámetro
    procesar_entrada(&mut buffer);
    
    // Ejemplo 5: Input dentro de condicional
    let mut respuesta = String::new();
    if true {
        let mut entrada = String::new();
    }
    
    // Ejemplo 6: Input dentro de bucle
    loop {
        let mut datos = String::new();
        break;
    }
}

// Función con parámetro de referencia mutable
fn procesar_entrada(buffer: &mut String) {
    // Procesar entrada
}

// ============================================================================
// PARTE 2: CÓDIGO CON ERRORES SINTÁCTICOS - Ejemplos inválidos
// ============================================================================

// ERROR 1: Falta punto y coma en declaración
fn error_missing_semicolon() {
    let mut buffer = String::new()
    println!("Error: falta ;");
}

// ERROR 2: Paréntesis no balanceados en función
fn error_unbalanced_parens() {
    let mut buffer = String::new(;
}

// ERROR 3: Tipo no especificado correctamente
fn error_invalid_type() {
    let mut buffer: InvalidType = String::new();
}

// ERROR 4: Referencia sin variable válida
fn error_invalid_reference() {
    let ref_x = &undefined_var;
}

// ERROR 5: String::new sin paréntesis
fn error_missing_parens() {
    let mut buffer = String::new;
}

// ERROR 6: Asignación sin expresión
fn error_no_expression() {
    let mut x = ;
}

// ERROR 7: Múltiples errores juntos
fn error_multiple() {
    let mut buffer = String::new(
    let ref_x = &;
    println!("Error)
}

// ============================================================================
// ESTRUCTURA BNF UTILIZADA:
// ============================================================================
// <Ruta> ::= <Identificador> { "::" <Identificador> }
// <LlamadaFuncion> ::= <Ruta> "(" [ <ListaArgumentos> ] ")"
// <LlamadaMetodo> ::= <Expresion> "." <Identificador> "(" [ <ListaArgumentos> ] ")" ";"
// <Referencia> ::= "&" [ "mut" ] <Identificador>
// <ListaArgumentos> ::= <Expresion> { "," <Expresion> }
//
// Para io::stdin().read_line(&mut buffer):
// - <Ruta> = "io" "::" "stdin"
// - <LlamadaFuncion> = "io::stdin" "(" ")"
// - <LlamadaMetodo> = "io::stdin()" "." "read_line" "(" "&mut buffer" ")"
// ============================================================================
