import pytest
import os
import sys

# Añadir la raíz del proyecto al sys.path para permitir importaciones absolutas
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from analyzer.ply_parser_final import parse_source

def test_parse_simple_closure_no_args():
    """
    Tests parsing a simple closure with no arguments that returns a literal.
    Example: let x = || 10;
    """
    source_code = "fn main() { let x = || 10; }"
    ast, errors = parse_source(source_code)
    
    # The test should fail initially, but our goal is to make it pass.
    # We expect no syntax errors for this valid code.
    assert len(errors) == 0
    assert ast is not None

def test_parse_closure_with_args():
    """
    Tests parsing a closure with typed arguments.
    Example: let add = |a: i32, b: i32| a + b;
    """
    source_code = "fn main() { let add = |a: i32, b: i32| a + b; }"
    ast, errors = parse_source(source_code)
    
    assert len(errors) == 0
    assert ast is not None

def test_parse_closure_with_block_body():
    """
    Tests parsing a closure with a full block body.
    Example: let x = || { let a = 1; return a; };
    """
    source_code = "fn main() { let x = || { return 10; }; }"
    ast, errors = parse_source(source_code)
    
    assert len(errors) == 0
    assert ast is not None

def test_parse_closure_with_return_type():
    """
    Tests parsing a closure with an explicit return type.
    Example: let x = || -> i32 { 10 };
    """
    source_code = "fn main() { let x = || -> i32 { return 10; }; }"
    ast, errors = parse_source(source_code)
    
    assert len(errors) == 0
    assert ast is not None

def test_parse_closure_with_untyped_args():
    """
    Tests parsing a closure with untyped arguments.
    Example: let x = |a, b| a + b;
    """
    source_code = "fn main() { let x = |a, b| a + b; }"
    ast, errors = parse_source(source_code)
    
    assert len(errors) == 0
    assert ast is not None

# To run this test: venv/bin/pytest analyzer/tests/test_closures.py
