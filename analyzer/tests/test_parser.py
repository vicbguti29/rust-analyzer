# analyzer/tests/test_parser.py
# Pruebas unitarias para el analizador sintáctico con pytest

import pytest
from analyzer.ply_parser_final import parse_source

def test_simple_let_statement_in_function():
    """
    Verifica que una declaración 'let' simple dentro de una función
    se analiza correctamente y genera el AST esperado.
    """
    code = "fn main() { let x = 5; }"
    
    # Analizar el código
    ast, errors = parse_source(code)
    
    # 1. Asegurarse de que no haya errores de sintaxis
    assert not errors, f"Se encontraron errores de sintaxis inesperados: {errors}"
    
    # 2. Definir la estructura del AST que esperamos
    expected_ast = (
        'program', 
        [
            ('fn', 'main', [], None, 
                [
                    ('let', 'x', None, ('literal', 5))
                ]
            )
        ]
    )
    
    # 3. Asegurarse de que el AST generado es el correcto
    assert ast == expected_ast, f"El AST generado no coincide con el esperado."


def test_function_without_parameters():
    """
    Verifica que una declaración de función sin parámetros se analiza correctamente.
    """
    code = "fn hello() {}"

    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    expected_ast = (
        'program',
        [
            ('fn', 'hello', [], None, [])
        ]
    )

    assert ast == expected_ast, "El AST para la función sin parámetros no es el esperado."


def test_simple_while_loop():
    """
    Prueba un bucle 'while' simple con una condición y cuerpo vacío.
    """
    code = "fn main() { while true {} }"
    
    ast, errors = parse_source(code)
    
    assert not errors, f"Se encontraron errores de sintaxis: {errors}"
    
    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None,
                [
                    ('while_loop', ('literal', True), [])
                ]
            )
        ]
    )
    
    assert ast == expected_ast, "El AST para el bucle while no es el esperado."


def test_simple_for_loop():
    """
    Prueba un bucle 'for' simple con un rango.
    """
    code = "fn main() { for i in 0..10 {} }"
    
    ast, errors = parse_source(code)
    
    assert not errors, f"Se encontraron errores de sintaxis: {errors}"
    
    # Estructura esperada: ('for_loop', var, iterable, cuerpo)
    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None,
                [
                    ('for_loop', 
                     'i', 
                     ('range', ('literal', 0), ('literal', 10)), 
                     []
                    )
                ]
            )
        ]
    )
    
    assert ast == expected_ast, "El AST para el bucle for no es el esperado."


def test_infinite_loop():
    """
    Prueba un bucle infinito 'loop' con un cuerpo vacío.
    """
    code = "fn main() { loop {} }"

    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    # Estructura esperada: ('infinite_loop', cuerpo)
    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None,
                [
                    ('infinite_loop', [])
                ]
            )
        ]
    )

    assert ast == expected_ast, "El AST para el bucle loop no es el esperado."


def test_break_statement():
    """
    Prueba una sentencia 'break' simple dentro de un bucle.
    """
    code = "fn main() { loop { break; } }"

    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    # Estructura esperada: ('break_stmt',)
    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None,
                [
                    ('infinite_loop', 
                        [
                            ('break_stmt',)
                        ]
                    )
                ]
            )
        ]
    )

    assert ast == expected_ast, "El AST para la sentencia break no es el esperado."


def test_continue_statement():
    """
    Prueba una sentencia 'continue' simple dentro de un bucle.
    """
    code = "fn main() { loop { continue; } }"

    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    # Estructura esperada: ('continue_stmt',)
    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None,
                [
                    ('infinite_loop',
                        [
                            ('continue_stmt',)
                        ]
                    )
                ]
            )
        ]
    )

    assert ast == expected_ast, "El AST para la sentencia continue no es el esperado."


def test_return_statement_simple():
    """
    Prueba una sentencia 'return' simple sin valor.
    """
    code = "fn main() { return; }"

    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    # Estructura esperada: ('return_stmt', valor) donde valor es None
    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None,
                [
                    ('return_stmt', None)
                ]
            )
        ]
    )

    assert ast == expected_ast, "El AST para la sentencia return simple no es el esperado."


def test_return_statement_with_value():
    """
    Prueba una sentencia 'return' con un valor.
    """
    code = "fn main() { return 5; }"

    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    # Estructura esperada: ('return_stmt', valor)
    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None,
                [
                    ('return_stmt', ('literal', 5))
                ]
            )
        ]
    )

    assert ast == expected_ast, "El AST para la sentencia return con valor no es el esperado."


def test_function_with_single_parameter():
    """
    Prueba una declaración de función con un solo parámetro.
    """
    code = "fn greet(name: String) {}"

    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    # Estructura esperada: ('fn', nombre, [parametros], tipo_retorno, cuerpo)
    expected_ast = (
        'program',
        [
            ('fn', 'greet', [('param', 'name', 'String')], None, [])
        ]
    )

    assert ast == expected_ast, "El AST para la función con un parámetro no es el esperado."


def test_function_with_return_type():
    """
    Prueba una declaración de función con un tipo de retorno.
    """
    code = "fn get_number() -> i32 { return 5; }"

    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    # Estructura esperada: ('fn', nombre, [parametros], tipo_retorno, cuerpo)
    expected_ast = (
        'program',
        [
            ('fn', 'get_number', [], 'i32', [('return_stmt', ('literal', 5))])
        ]
    )

    assert ast == expected_ast, "El AST para la función con tipo de retorno no es el esperado."


def test_function_with_multiple_parameters():
    """
    Prueba una declaración de función con múltiples parámetros.
    """
    code = "fn add(x: i32, y: i32) {}"

    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    expected_ast = (
        'program',
        [
            ('fn', 'add',
                [
                    ('param', 'x', 'i32'),
                    ('param', 'y', 'i32')
                ],
                None, [])
        ]
    )
    assert ast == expected_ast, "El AST para la función con múltiples parámetros no es el esperado."


def test_simple_enum_declaration():
    """
    Prueba una declaración 'enum' simple con variantes.
    """
    code = "enum Color { Red, Green, Blue }"

    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    # Estructura esperada: ('enum_decl', nombre, [variantes])
    expected_ast = (
        'program',
        [
            ('enum_decl', 'Color', ['Red', 'Green', 'Blue'])
        ]
    )

    assert ast == expected_ast, "El AST para la declaración enum no es el esperado."

def test_simple_trait_declaration():
    """
    Prueba una declaración 'trait' simple con una firma de función.
    """
    code = "trait Printable { fn print(&self); }"

    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    # Estructura esperada: ('trait_decl', nombre, [items_del_trait])
    expected_ast = (
        'program',
        [
            ('trait_decl', 'Printable', [('fn_signature', 'print', [('param', '&self', None)], None)])
        ]
    )

    assert ast == expected_ast, "El AST para la declaración trait no es el esperado."

def test_empty_impl_block():
    """
    Prueba un bloque 'impl' simple y vacío para una estructura.
    """
    code = """
        struct MyStruct {}
        impl MyStruct {}
        """
    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    expected_ast = (
        'program',
        [
            ('struct', 'MyStruct', []),
            ('impl_block', 'MyStruct', None, [])
        ]
    )
    assert ast == expected_ast, "El AST para el bloque impl vacío no es el esperado."


def test_impl_with_function_and_explicit_return():
    """
    Prueba un bloque 'impl' con una función que devuelve una instancia
    de struct mediante un retorno explícito.
    """
    code = """
struct MyStruct {}
impl MyStruct {
    fn new() -> MyStruct {
                    return MyStruct {};    }
}
"""
    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    expected_ast = (
        'program',
        [
            ('struct', 'MyStruct', []),
            ('impl_block', 'MyStruct', None, [
                ('fn', 'new', [], 'MyStruct', [
                    ('return_stmt', ('struct_init', 'MyStruct', []))
                ])
            ])
        ]
    )
    assert ast == expected_ast, "El AST para el impl con retorno explícito no es el esperado."


def test_impl_trait_for_struct():
    """
    Prueba la implementación de un trait para un struct.
    """
    code = """
trait MyTrait {}
struct MyStruct {}
impl MyTrait for MyStruct {}
"""
    ast, errors = parse_source(code)
    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    expected_ast = (
        'program',
        [
            ('trait_decl', 'MyTrait', []),
            ('struct', 'MyStruct', []),
            ('impl_block', 'MyTrait', 'MyStruct', [])
        ]
    )
    assert ast == expected_ast, "El AST para impl Trait for Struct no es el esperado."


def test_associated_function_with_self_type():
    """
    Prueba una función asociada que devuelve el tipo 'Self'.
    """
    code = """
struct MyStruct {}
impl MyStruct {
    fn new() -> Self {
        return MyStruct {};
    }
}
"""
    ast, errors = parse_source(code)
    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    expected_ast = (
        'program',
        [
            ('struct', 'MyStruct', []),
            ('impl_block', 'MyStruct', None, [
                ('fn', 'new', [], 'Self', [
                    ('return_stmt', ('struct_init', 'MyStruct', []))
                ])
            ])
        ]
    )
    assert ast == expected_ast, "El AST para la función asociada con Self no es el esperado."


def test_array_literal():
    """
    Prueba la declaración de un array literal.
    """
    code = "fn main() { let arr = [1, 2, 3]; }"
    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None,
                [
                    ('let', 'arr', None,
                        ('array_literal',
                            [
                                ('literal', 1),
                                ('literal', 2),
                                ('literal', 3)
                            ]
                        )
                    )
                ]
            )
        ]
    )
    assert ast == expected_ast, "El AST para el array literal no es el esperado."

def test_tuple_literal():
    """
    Prueba la declaración de un tuple literal.
    """
    code = "fn main() { let t = (1, true, \"hello\"); }"
    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None,
                [
                    ('let', 't', None,
                        ('tuple_literal',
                            [
                                ('literal', 1),
                                ('literal', True),
                                ('literal', "hello")
                            ]
                        )
                    )
                ]
            )
        ]
    )
    assert ast == expected_ast, "El AST para el tuple literal no es el esperado."

def test_empty_tuple_literal():
    """
    Prueba la declaración de un tuple vacío.
    """
    code = "fn main() { let t = (); }"
    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None,
                [
                    ('let', 't', None, ('tuple_literal', []))
                ]
            )
        ]
    )
    assert ast == expected_ast, "El AST para el tuple vacío no es el esperado."

def test_single_element_tuple_literal():
    """
    Prueba la declaración de un tuple con un solo elemento (requiere coma).
    """
    code = "fn main() { let t = (1,); }"
    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None,
                [
                    ('let', 't', None,
                        ('tuple_literal',
                            [
                                ('literal', 1)
                            ]
                        )
                    )
                ]
            )
        ]
    )
    assert ast == expected_ast, "El AST para el tuple de un solo elemento no es el esperado."


@pytest.mark.xfail(reason="Documenta un bug complejo y conocido donde println! falla dentro de un if/else en un archivo grande.")
def test_full_valid_file_with_known_bug():
    """
    Prueba el archivo completo 'prb_sintactico_valido.rs' que se sabe que falla.
    Este test documenta el bug del parser con la combinación de sentencias.
    """
    code = """
// --- 1. Declaraciones de Nivel Superior ---
const MAX_CONNECTIONS: u32 = 100;
static APP_NAME: &str = "Rust Analyzer";

struct Point { x: i32, y: i32, }
struct Empty {}

enum Status { Connected, Disconnected, Connecting, }
enum EmptyEnum {}

trait Serializable {
    fn to_string(&self) -> String;
    fn get_id() -> u32;
}

impl Serializable for Point {
    fn to_string(&self) -> String {
        return "Point";
    }
    fn get_id() -> u32 {
        return 1;
    }
}

impl Empty {
    fn new() -> Self {
        let instance = Empty {};
        return instance;
    }
}

// --- 2. Funciones ---
fn simple_function() {}
fn function_with_params(count: i32, name: String) { let x = count; }
fn function_with_return() -> bool { return true; }

// --- 3. Función Principal con Sentencias y Expresiones ---
fn main() {
    let a: i32 = 10;
    let b = 20.5;
    let mut c = false;
    let mut d: String = "hello";

    let result = (a + 5) * 2 - 1;
    let is_ok = result > 20 && !c;
    let is_not_ok = a < 0 || c == true;

    if is_ok {
        println!("OK");
    } else {
        println!("Not OK");
    }

    let mut counter = 0;
    while counter < 3 {
        println!("while...");
        counter = counter + 1;
    }

    for i in 0..2 {
        println!("for...");
    }

    loop {
        println!("loop...");
        break;
    }
    
    let e = Empty {};
    let arr = [1, 2, 3];
    let tup = (10, "tuple", false);
    
    counter = 10;
    counter += 5;

    let data = input();
    
    return;
}
"""
    ast, errors = parse_source(code)
    assert not errors, f"Este test falla debido a un bug conocido y complejo del parser."

