// docs/algoritmos_de_prueba/prb_existencia_scope.rs
// Archivo de prueba para REGLA 1 (Validación de Existencia) y REGLA 2 (Alcance Local)
// Autor: vicbguti29

fn main() {
    // === CASOS VÁLIDOS ===
    
    // Caso 1: Declaración y uso de variable en el mismo scope
    let x: i32 = 5;
    let y = x + 10;
    
    // Caso 2: Variable mutable declarada y reasignada
    let mut contador = 0;
    contador = 10;
    
    // Caso 3: Variable global usada en scope anidado
    let global_var = 100;
    if true {
        let result = global_var + 50;
    }
    
    
    // === CASOS INVÁLIDOS - REGLA 1: EXISTENCIA ===
    
    // Error 1: Variable no declarada (REGLA 1)
    let z = undefined_var;
    
    // Error 2: Variable no declarada en aritmética (REGLA 1)
    let resultado = unknown_x * 5;
    
    // Error 3: Variable no declarada en asignación (REGLA 1)
    no_existe = 42;
    
    
    // === CASOS INVÁLIDOS - REGLA 2: ALCANCE LOCAL ===
    
    // Error 4: Acceso a variable declarada en if (REGLA 2)
    if true {
        let local_only = 999;
    }
    let try_access = local_only;
    
    // Error 5: Acceso a variable de for (REGLA 2)
    for i in 0..5 {
        let loop_var = i * 2;
    }
    let after_loop = loop_var;
    
    // Error 6: Acceso a variable de bloque anidado (REGLA 2)
    if true {
        let inner_var = 20;
    }
    let try_inner = inner_var;
    
    // Caso válido: Variable de scope superior SÍ es accesible
    let accessible = 50;
    if true {
        let used = accessible + 10;
    }
}
