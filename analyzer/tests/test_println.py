# analyzer/tests/test_println.py
# Pruebas unitarias específicas para la macro println!

import pytest
from analyzer.ply_parser_final import parse_source

def test_println_simple_in_main():
    """Prueba un println! simple en el cuerpo de una función."""
    code = """
fn main() {
    println!("Hello, World!");
}
"""
    ast, errors = parse_source(code)
    assert not errors, f"Falló el caso más simple de println!: {errors}"

    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None, [
                ('println', '"Hello, World!"', [])
            ])
        ]
    )
    assert ast == expected_ast

def test_println_with_args_in_main():
    """Prueba un println! con argumentos."""
    code = """
fn main() {
    let x = 10;
    println!("El valor es: {}", x);
}
"""
    ast, errors = parse_source(code)
    assert not errors, f"Falló el println! con argumentos: {errors}"

    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None, [
                ('let', 'x', None, ('literal', 10)),
                ('println', '"El valor es: {}"', [('literal', 'x')])
            ])
        ]
    )
    assert ast == expected_ast

def test_println_in_if_block():
    """Prueba un println! dentro de un bloque 'if'."""
    code = """
fn main() {
    if true {
        println!("Dentro del if");
    }
}
"""
    ast, errors = parse_source(code)
    assert not errors, f"Falló el println! dentro de un 'if': {errors}"

    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None, [
                ('if', ('literal', True), [
                    ('println', '"Dentro del if"', [])
                ])
            ])
        ]
    )
    assert ast == expected_ast

def test_println_in_else_block():
    """Prueba un println! dentro de un bloque 'else'."""
    code = """
fn main() {
    if false {
        // nothing
    } else {
        println!("Dentro del else");
    }
}
"""
    ast, errors = parse_source(code)
    assert not errors, f"Falló el println! dentro de un 'else': {errors}"

    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None, [
                ('if_else', ('literal', False), [], [
                    ('println', '"Dentro del else"', [])
                ])
            ])
        ]
    )
    assert ast == expected_ast

def test_println_in_while_loop():
    """Prueba un println! dentro de un bucle 'while'."""
    code = """
fn main() {
    while false {
        println!("loop");
    }
}
"""
    ast, errors = parse_source(code)
    assert not errors, f"Falló el println! dentro de un 'while': {errors}"

    expected_ast = (
        'program',
        [
            ('fn', 'main', [], None, [
                ('while_loop', ('literal', False), [
                    ('println', '"loop"', [])
                ])
            ])
        ]
    )
    assert ast == expected_ast
