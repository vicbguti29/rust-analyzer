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

def test_simple_impl_block():
    """
    Prueba un bloque 'impl' simple para una estructura.
    Fallará hasta que se implemente la regla para 'impl'.
    """
    code = """
        struct MyStruct {}
        impl MyStruct {}
        """
    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    # Estructura esperada: ('impl_block', tipo_implementado, [items_del_impl])
    expected_ast = (
        'program',
        [
            ('struct', 'MyStruct', []),
            ('impl_block', 'MyStruct', [])
        ]
    )
    assert ast == expected_ast, "El AST para el bloque impl no es el esperado."

def test_simple_impl_block():
    """
    Prueba un bloque 'impl' simple para una estructura.
    Fallará hasta que se implemente la regla para 'impl'.
    """
    code = """
        struct MyStruct {}
        impl MyStruct {}
        """
    ast, errors = parse_source(code)

    assert not errors, f"Se encontraron errores de sintaxis: {errors}"

    # Estructura esperada: ('impl_block', tipo_implementado, [items_del_impl])
    expected_ast = (
        'program',
        [
            ('struct', 'MyStruct', []),
            ('impl_block', 'MyStruct', [])
        ]
    )
    assert ast == expected_ast, "El AST para el bloque impl no es el esperado."

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
