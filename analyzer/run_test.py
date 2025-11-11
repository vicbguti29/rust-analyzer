#!/usr/bin/env python
# Script para ejecutar el lexer sobre test_lexer.rs

import sys
from ply_lexer import tokenize_source

# Leer el archivo test_lexer.rs
with open('test_lexer.rs', 'r', encoding='utf-8') as f:
    test_code = f.read()

print("Tokenizando archivo test_lexer.rs:")
print("=" * 60)
print(test_code)
print("=" * 60)
print("\nTokens encontrados:")
print("-" * 60)

tokens = tokenize_source(test_code)
if tokens:
    for token in tokens:
        print(f"Token: {token['type']:<15} | Valor: {token['lexeme']:<20} | Línea: {token['line']:<3} | Col: {token['column']}")
else:
    print("No se encontraron tokens.")

print("-" * 60)
print(f"\nTotal de tokens: {len(tokens)}")
