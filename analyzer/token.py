from dataclasses import dataclass

class TokenType:
    # Keywords & Identifiers
    IDENT = "IDENT"
    LET = "LET"
    FN = "FN"
    MUT = "MUT"
    
    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"

    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"

    # Delimiters
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    COMMA = ","
    SEMICOLON = ";"

    # Control
    EOF = "EOF"
    ERROR = "ERROR"


@dataclass
class Token:
    type: str
    lexeme: str
    line: int
    column: int
    # Opcional: literal, end_line, end_column
    literal: object = None
    end_line: int = None
    end_column: int = None