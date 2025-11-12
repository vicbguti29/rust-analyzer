from dataclasses import dataclass

class TokenType:
    # Control Flow
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    LOOP = "LOOP"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    RETURN = "RETURN"
    
    # Functions and Variables
    FN = "FN"
    LET = "LET"
    MUT = "MUT"
    CONST = "CONST"
    STATIC = "STATIC"

    # Types
    I32 = "I32"
    I64 = "I64"
    U32 = "U32"
    U64 = "U64"
    F32 = "F32"
    F64 = "F64"
    BOOL = "BOOL"
    CHAR = "CHAR"
    STR = "STR"
    STRING_TYPE = "STRING_TYPE"

    # Structs and Modules
    STRUCT = "STRUCT"
    ENUM = "ENUM"
    MOD = "MOD"
    USE = "USE"
    PUB = "PUB"
    SELF = "SELF"
    SELF_TYPE = "SELF_TYPE"

    # Traits and Implementation
    TRAIT = "TRAIT"
    IMPL = "IMPL"
    WHERE = "WHERE"

    # Memory and Collections
    BOX = "BOX"
    VEC = "VEC"
    OPTION = "OPTION"
    SOME = "SOME"
    NONE = "NONE"

    # Identifiers and Literals
    IDENT = "IDENT"
    NUMBER = "NUMBER"
    STRING = "STRING"

    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    ARROW = "->"
    AMPERSAND = "&"
    LT = "<"
    GT = ">"
    SCOPE = "::"

    # Delimiters
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    COMMA = ","
    SEMICOLON = ";"
    COLON = ":"

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