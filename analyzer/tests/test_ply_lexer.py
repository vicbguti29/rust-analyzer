# analyzer/tests/test_ply_lexer.py
# Tests for the PLY-based lexer.

import pytest
from analyzer.ply_lexer import tokenize_source

def assert_token_sequence(tokens, expected):
    """Helper function to compare token sequences, including literals."""
    assert len(tokens) == len(expected)
    for i, token in enumerate(tokens):
        exp_token = expected[i]
        assert token['type'] == exp_token['type']
        assert token['value'] == exp_token['value']
        assert token['line'] == exp_token['line']
        if 'literal' in exp_token:
            assert token['literal'] == exp_token['literal']

def test_let_statement():
    """Tests a simple variable declaration."""
    code = "let x = 5;"
    tokens = tokenize_source(code)
    expected = [
        {'type': 'LET', 'value': 'let', 'line': 1, 'literal': 'let'},
        {'type': 'IDENT', 'value': 'x', 'line': 1, 'literal': 'x'},
        {'type': 'EQUALS', 'value': '=', 'line': 1, 'literal': '='},
        {'type': 'NUMBER', 'value': '5', 'line': 1, 'literal': 5},
        {'type': 'SEMICOLON', 'value': ';', 'line': 1, 'literal': ';'},
    ]
    assert_token_sequence(tokens, expected)

@pytest.mark.parametrize("code, expected_type, expected_literal", [
    ("if", "IF", "if"),
    ("else", "ELSE", "else"),
    ("fn", "FN", "fn"),
    ("struct", "STRUCT", "struct"),
    ("while", "WHILE", "while"),
    ("for", "FOR", "for"),
    ("true", "TRUE", True),
    ("false", "FALSE", False),
    ("return", "RETURN", "return"),
])
def test_keywords(code, expected_type, expected_literal):
    """Tests various keywords."""
    tokens = tokenize_source(code)
    expected = [
        {'type': expected_type, 'value': code, 'line': 1, 'literal': expected_literal},
    ]
    assert_token_sequence(tokens, expected)

@pytest.mark.parametrize("code, expected_type", [
    ("+", "PLUS"),
    ("->", "ARROW"),
    ("==", "EQ"),
    ("!=", "NEQ"),
    (">=", "GTE"),
    ("<=", "LTE"),
    ("&&", "AND"),
    ("||", "OR"),
    ("+=", "PLUS_EQUALS"),
    ("!","NOT"),
])
def test_operators(code, expected_type):
    """Tests various simple and compound operators."""
    tokens = tokenize_source(code)
    expected = [
        {'type': expected_type, 'value': code, 'line': 1, 'literal': code},
    ]
    assert_token_sequence(tokens, expected)

def test_float_and_scientific_notation():
    """Tests floating point and scientific notation numbers."""
    code = "3.14 1.23e-5"
    tokens = tokenize_source(code)
    expected = [
        {'type': 'FLOAT', 'value': '3.14', 'line': 1, 'literal': 3.14},
        {'type': 'FLOAT', 'value': '1.23e-5', 'line': 1, 'literal': 1.23e-5},
    ]
    assert_token_sequence(tokens, expected)

def test_string_literal():
    """Tests a simple string literal."""
    code = '"hello rust"'
    tokens = tokenize_source(code)
    expected = [
        {'type': 'STRING', 'value': '"hello rust"', 'line': 1, 'literal': 'hello rust'},
    ]
    assert_token_sequence(tokens, expected)

def test_string_with_escapes():
    """Tests a string with various escape sequences."""
    code = r'"a \"b\\nc\\td"'
    tokens = tokenize_source(code)
    expected = [
        {'type': 'STRING', 'value': r'"a \"b\\nc\\td"', 'line': 1, 'literal': 'a "b\nc\td'},
    ]
    assert_token_sequence(tokens, expected)

def test_line_comment():
    """Tests that single-line comments are ignored."""
    code = """
let x = 10; // This is a comment
let y = 20;
"""
    tokens = tokenize_source(code)
    expected = [
        {'type': 'LET', 'value': 'let', 'line': 2, 'literal': 'let'},
        {'type': 'IDENT', 'value': 'x', 'line': 2, 'literal': 'x'},
        {'type': 'EQUALS', 'value': '=', 'line': 2, 'literal': '='},
        {'type': 'NUMBER', 'value': '10', 'line': 2, 'literal': 10},
        {'type': 'SEMICOLON', 'value': ';', 'line': 2, 'literal': ';'},
        {'type': 'LET', 'value': 'let', 'line': 3, 'literal': 'let'},
        {'type': 'IDENT', 'value': 'y', 'line': 3, 'literal': 'y'},
        {'type': 'EQUALS', 'value': '=', 'line': 3, 'literal': '='},
        {'type': 'NUMBER', 'value': '20', 'line': 3, 'literal': 20},
        {'type': 'SEMICOLON', 'value': ';', 'line': 3, 'literal': ';'},
    ]
    assert_token_sequence(tokens, expected)

def test_line_counting():
    """Tests that newlines correctly increment the line number."""
    code = """
let a = 1;

let b = 2;
"""
    tokens = tokenize_source(code)
    expected = [
        {'type': 'LET', 'value': 'let', 'line': 2, 'literal': 'let'},
        {'type': 'IDENT', 'value': 'a', 'line': 2, 'literal': 'a'},
        {'type': 'EQUALS', 'value': '=', 'line': 2, 'literal': '='},
        {'type': 'NUMBER', 'value': '1', 'line': 2, 'literal': 1},
        {'type': 'SEMICOLON', 'value': ';', 'line': 2, 'literal': ';'},
        {'type': 'LET', 'value': 'let', 'line': 4, 'literal': 'let'},
        {'type': 'IDENT', 'value': 'b', 'line': 4, 'literal': 'b'},
        {'type': 'EQUALS', 'value': '=', 'line': 4, 'literal': '='},
        {'type': 'NUMBER', 'value': '2', 'line': 4, 'literal': 2},
        {'type': 'SEMICOLON', 'value': ';', 'line': 4, 'literal': ';'},
    ]
    assert_token_sequence(tokens, expected)

def test_multiline_comment_ignored():
    """Tests that multi-line comments are correctly ignored and line counts are updated."""
    code = """
let a = 1; /* This is a
              multi-line
              comment */ let b = 2;
"""
    tokens = tokenize_source(code)
    expected = [
        {'type': 'LET', 'value': 'let', 'line': 2, 'literal': 'let'},
        {'type': 'IDENT', 'value': 'a', 'line': 2, 'literal': 'a'},
        {'type': 'EQUALS', 'value': '=', 'line': 2, 'literal': '='},
        {'type': 'NUMBER', 'value': '1', 'line': 2, 'literal': 1},
        {'type': 'SEMICOLON', 'value': ';', 'line': 2, 'literal': ';'},
        {'type': 'LET', 'value': 'let', 'line': 4, 'literal': 'let'},
        {'type': 'IDENT', 'value': 'b', 'line': 4, 'literal': 'b'},
        {'type': 'EQUALS', 'value': '=', 'line': 4, 'literal': '='},
        {'type': 'NUMBER', 'value': '2', 'line': 4, 'literal': 2},
        {'type': 'SEMICOLON', 'value': ';', 'line': 4, 'literal': ';'},
    ]
    assert_token_sequence(tokens, expected)

def test_macro_call():
    """Tests that a macro call like println! is tokenized as a single token."""
    code = 'println!("Hello");'
    tokens = tokenize_source(code)
    expected = [
        {'type': 'CONSOLE_PRINT', 'value': 'println!', 'line': 1, 'literal': 'println!'},
        {'type': 'LPAREN', 'value': '(', 'line': 1, 'literal': '('},
        {'type': 'STRING', 'value': '"Hello"', 'line': 1, 'literal': 'Hello'},
        {'type': 'RPAREN', 'value': ')', 'line': 1, 'literal': ')'},
        {'type': 'SEMICOLON', 'value': ';', 'line': 1, 'literal': ';'},
    ]
    assert_token_sequence(tokens, expected)

def test_vec_macro():
    """Tests that the vec! macro is tokenized correctly."""
    code = 'vec![1, 2]'
    tokens = tokenize_source(code)
    expected = [
        {'type': 'VEC_CREATE', 'value': 'vec!', 'line': 1, 'literal': 'vec!'},
        {'type': 'LBRACKET', 'value': '[', 'line': 1, 'literal': '['},
        {'type': 'NUMBER', 'value': '1', 'line': 1, 'literal': 1},
        {'type': 'COMMA', 'value': ',', 'line': 1, 'literal': ','},
        {'type': 'NUMBER', 'value': '2', 'line': 1, 'literal': 2},
        {'type': 'RBRACKET', 'value': ']', 'line': 1, 'literal': ']'},
    ]
    assert_token_sequence(tokens, expected)

def test_unrecognized_character():
    """Tests that an unrecognized character generates an ERROR token."""
    code = "let a = #;"
    tokens = tokenize_source(code)
    expected = [
        {'type': 'LET', 'value': 'let', 'line': 1, 'literal': 'let'},
        {'type': 'IDENT', 'value': 'a', 'line': 1, 'literal': 'a'},
        {'type': 'EQUALS', 'value': '=', 'line': 1, 'literal': '='},
        {'type': 'ERROR', 'value': '#', 'line': 1, 'literal': "Illegal character '#'"},
        {'type': 'SEMICOLON', 'value': ';', 'line': 1, 'literal': ';'},
    ]
    assert_token_sequence(tokens, expected)


def test_dotdot_operator():
    """Tests that the range operator '..' is tokenized correctly."""
    code = "0..10"
    tokens = tokenize_source(code)
    expected = [
        {'type': 'NUMBER', 'value': '0', 'line': 1, 'literal': 0},
        {'type': 'DOTDOT', 'value': '..', 'line': 1, 'literal': '..'},
        {'type': 'NUMBER', 'value': '10', 'line': 1, 'literal': 10},
    ]
    assert_token_sequence(tokens, expected)
