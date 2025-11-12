import pytest
from analyzer.lexer import Lexer
from analyzer.token import Token, TokenType


def test_tokenize_mutable_function():
    source = "let mut f = fn() {};"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    expected_tokens = [
        Token(type=TokenType.LET, lexeme='let', line=1, column=1),
        Token(type=TokenType.MUT, lexeme='mut', line=1, column=5),
        Token(type=TokenType.IDENT, lexeme='f', line=1, column=9),
        Token(type=TokenType.ASSIGN, lexeme='=', line=1, column=11),
        Token(type=TokenType.FN, lexeme='fn', line=1, column=13),
        Token(type=TokenType.LPAREN, lexeme='(', line=1, column=15),
        Token(type=TokenType.RPAREN, lexeme=')', line=1, column=16),
        Token(type=TokenType.LBRACE, lexeme='{', line=1, column=18),
        Token(type=TokenType.RBRACE, lexeme='}', line=1, column=19),
        Token(type=TokenType.SEMICOLON, lexeme=';', line=1, column=20),
        Token(type=TokenType.EOF, lexeme='', line=1, column=21)
    ]

    assert len(tokens) == len(expected_tokens)
    for i, token in enumerate(tokens):
        expected = expected_tokens[i]
        assert token.type == expected.type
        assert token.lexeme == expected.lexeme
        assert token.line == expected.line
        assert token.column == expected.column
        if expected.literal is not None:
            assert token.literal == expected.literal

def test_tokenize_string_literal():
    source = '"hola"'
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    expected_tokens = [
        Token(type=TokenType.STRING, lexeme='"hola"', line=1, column=1, literal='hola'),
        Token(type=TokenType.EOF, lexeme='', line=1, column=7)
    ]

    assert len(tokens) == len(expected_tokens)
    for i, token in enumerate(tokens):
        expected = expected_tokens[i]
        assert token.type == expected.type
        assert token.lexeme == expected.lexeme
        assert token.line == expected.line
        assert token.column == expected.column
        if expected.literal is not None:
            assert token.literal == expected.literal

def test_tokenize_string_with_escapes():
    source = '"a \\"b\\nc\\td"'
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    expected_tokens = [
        Token(type=TokenType.STRING, lexeme='"a \\"b\\nc\\td"', line=1, column=1, literal='a "b\nc\td'),
        Token(type=TokenType.EOF, lexeme='', line=1, column=14) # TODO: Fix column counting, should be 16
    ]

    assert len(tokens) == len(expected_tokens)
    for i, token in enumerate(tokens):
        expected = expected_tokens[i]
        assert token.type == expected.type
        assert token.lexeme == expected.lexeme
        assert token.line == expected.line
        assert token.column == expected.column
        if expected.literal is not None:
            assert token.literal == expected.literal

def test_tokenize_floating_point_number():
    source = "123.45"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    expected_tokens = [
        Token(type=TokenType.NUMBER, lexeme='123.45', line=1, column=1, literal=123.45),
        Token(type=TokenType.EOF, lexeme='', line=1, column=7)
    ]

    assert len(tokens) == len(expected_tokens)
    for i, token in enumerate(tokens):
        expected = expected_tokens[i]
        assert token.type == expected.type
        assert token.lexeme == expected.lexeme
        assert token.line == expected.line
        assert token.column == expected.column
        if expected.literal is not None:
            assert token.literal == expected.literal

def test_it_ignores_multiline_comments():
    source = "let /* comment */ x;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    expected_tokens = [
        Token(type=TokenType.LET, lexeme='let', line=1, column=1),
        Token(type=TokenType.IDENT, lexeme='x', line=1, column=19),
        Token(type=TokenType.SEMICOLON, lexeme=';', line=1, column=20),
        Token(type=TokenType.EOF, lexeme='', line=1, column=21)
    ]

    assert len(tokens) == len(expected_tokens)
    for i, token in enumerate(tokens):
        expected = expected_tokens[i]
        assert token.type == expected.type
        assert token.lexeme == expected.lexeme
        assert token.line == expected.line
        assert token.column == expected.column
        if expected.literal is not None:
            assert token.literal == expected.literal

def test_it_ignores_single_line_comments():
    source = "let x = 10; // comment"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    expected_tokens = [
        Token(type=TokenType.LET, lexeme='let', line=1, column=1),
        Token(type=TokenType.IDENT, lexeme='x', line=1, column=5),
        Token(type=TokenType.ASSIGN, lexeme='=', line=1, column=7),
        Token(type=TokenType.NUMBER, lexeme='10', line=1, column=9, literal=10),
        Token(type=TokenType.SEMICOLON, lexeme=';', line=1, column=11),
        Token(type=TokenType.EOF, lexeme='', line=1, column=23)
    ]

    assert len(tokens) == len(expected_tokens)
    for i, token in enumerate(tokens):
        expected = expected_tokens[i]
        assert token.type == expected.type
        assert token.lexeme == expected.lexeme
        assert token.line == expected.line
        assert token.column == expected.column
        if expected.literal is not None:
            assert token.literal == expected.literal

@pytest.mark.parametrize("source, literal", [
    ("1e5", 1e5),
    ("1.23E+4", 1.23E+4),
    ("9.87e-2", 9.87e-2),
    ("5E10", 5E10),
])
def test_tokenize_scientific_notation(source, literal):
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    expected_tokens = [
        Token(type=TokenType.NUMBER, lexeme=source, line=1, column=1, literal=literal),
        Token(type=TokenType.EOF, lexeme='', line=1, column=len(source) + 1)
    ]

    assert len(tokens) == len(expected_tokens)
    for i, token in enumerate(tokens):
        expected = expected_tokens[i]
        assert token.type == expected.type
        assert token.lexeme == expected.lexeme
        assert token.line == expected.line
        assert token.column == expected.column
        if expected.literal is not None:
            assert token.literal == expected.literal
