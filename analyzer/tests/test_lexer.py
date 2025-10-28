import pytest
from analyzer.lexer import Lexer
from analyzer.token import Token


def test_tokenize_simple():
    source = "a = 1 + 2"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert tokens[-1].type == "EOF"
    # TODO: Añadir asserts para los tokens esperados
