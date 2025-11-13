# analyzer/ply_lexer.py
# Lexer ágil usando PLY para prototipado y pruebas rápidas
from dataclasses import dataclass
import ply.lex as lex

# Lista de nombres de tokens de Rust
tokens = (
    # Palabras clave de control de flujo
    "IF",
    "ELSE",
    "WHILE",
    "FOR",
    "LOOP",
    "BREAK",
    "CONTINUE",
    # Palabras clave de funciones y variables
    "FN",
    "LET",
    "MUT",
    "RETURN",
    "CONST",
    "STATIC",
    # Palabras clave de tipos
    "I32",
    "I64",
    "U32",
    "U64",
    "F32",
    "F64",
    "BOOL",
    "CHAR",
    "STR",
    "STRING_TYPE",
    "TRUE",
    "FALSE",
    # Palabras clave de estructura y módulos
    "STRUCT",
    "ENUM",
    "MOD",
    "USE",
    "PUB",
    "SELF",
    "SELF_TYPE",
    # Palabras clave de traits e implementación
    "TRAIT",
    "IMPL",
    "WHERE",
    # Palabras clave de control de memoria
    "BOX",
    "VEC",
    "OPTION",
    "SOME",
    "NONE",
    # Palabras clave de I/O
    "PRINTLN",
    "INPUT",
    "IN",
    # Identificadores y literales
    "IDENT",  # identificadores
    "NUMBER",  # números enteros
    "FLOAT",  # números con punto decimal y/o exponente
    "STRING",  # "cadenas"
    # Operadores y símbolos
    "PLUS",  # +
    "MINUS",  # -
    "TIMES",  # *
    "DIVIDE",  # /
    "EQUALS",  # =
    "ARROW",  # ->
    # Operadores de comparación
    "EQ",  # ==
    "NEQ",  # !=
    "LT",  # <
    "LTE",  # <=
    "GT",  # >
    "GTE",  # >=
    # Operadores lógicos
    "AND",  # &&
    "OR",  # ||
    "NOT",  # !
    # Operadores de asignación compuesta
    "PLUS_EQUALS",  # +=
    "MINUS_EQUALS",  # -=
    "TIMES_EQUALS",  # *=
    "DIVIDE_EQUALS",  # /=
    # Delimitadores
    "LPAREN",  # (
    "RPAREN",  # )
    "LBRACE",  # {
    "RBRACE",  # }
    "SEMICOLON",  # ;
    "COLON",  # :
    "COMMA",  # ,
    # Comentarios
    "COMMENT",  # // comentarios
)

# Palabras reservadas de Rust
reserved = {
    # Keywords de control de flujo
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "loop": "LOOP",
    "break": "BREAK",
    "continue": "CONTINUE",
    # Keywords de funciones y variables
    "fn": "FN",
    "let": "LET",
    "mut": "MUT",
    "return": "RETURN",
    "const": "CONST",
    "static": "STATIC",
    # Keywords de tipos
    "i32": "I32",
    "i64": "I64",
    "u32": "U32",
    "u64": "U64",
    "f32": "F32",
    "f64": "F64",
    "bool": "BOOL",
    "char": "CHAR",
    "str": "STR",
    "String": "STRING_TYPE",
    "true": "TRUE",
    "false": "FALSE",
    # Keywords de estructura y módulos
    "struct": "STRUCT",
    "enum": "ENUM",
    "mod": "MOD",
    "use": "USE",
    "pub": "PUB",
    "self": "SELF",
    "Self": "SELF_TYPE",
    # Keywords de traits e implementación
    "trait": "TRAIT",
    "impl": "IMPL",
    "where": "WHERE",
    # Keywords de control de memoria
    "Box": "BOX",
    "Vec": "VEC",
    "Option": "OPTION",
    "Some": "SOME",
    "None": "NONE",
    # Keywords de I/O
    "println": "PRINTLN",
    "input": "INPUT",
    "in": "IN",
}

# Reglas regex para tokens simples (deben definirse antes de otros que usan los mismos caracteres)
def t_ARROW(t):
    r'->'
    return t

def t_EQ(t):
    r'=='
    return t

def t_NEQ(t):
    r'!='
    return t

def t_LTE(t):
    r'<='
    return t

def t_GTE(t):
    r'>='
    return t

def t_PLUS_EQUALS(t):
    r'\+='
    return t

def t_MINUS_EQUALS(t):
    r'-='
    return t

def t_TIMES_EQUALS(t):
    r'\*='
    return t

def t_DIVIDE_EQUALS(t):
    r'/='
    return t

def t_AND(t):
    r'&&'
    return t

def t_OR(t):
    r'\|\|'
    return t

t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_EQUALS = r"="
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"{"
t_RBRACE = r"}"
t_SEMICOLON = r";"
t_COLON = r":"
t_COMMA = r","
t_NOT = r"!"
t_LT = r"<"
t_GT = r">"


# Reglas con código de acción
def t_identifier(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = reserved.get(t.value, "IDENT")  # Check for reserved words
    return t


def t_float(t):
    r"\d+\.\d+([eE][+-]?\d+)?"
    t.value = float(t.value)
    t.type = "FLOAT"
    return t


def t_number(t):
    r"\d+"
    t.value = int(t.value)
    t.type = "NUMBER"
    return t


def t_string(t):
    r"\"([^\\\n]|(\\.))*?\""
    t.type = "STRING"
    return t


def t_char(t):
    r"'([^'\\\n]|\\.)'"
    t.type = "CHAR"
    return t


def t_comment(t):
    r"//.*"
    pass  # No return - ignorar comentarios


# Regla para contar líneas
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Caracteres ignorados
t_ignore = " \t"


# Manejo de errores
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)


# Construir el lexer
lexer = lex.lex()


def tokenize_source(source):
    lexer.input(source)
    result = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        result.append(
            {
                "type": tok.type,
                "lexeme": str(tok.value),
                "line": tok.lineno,
                "column": tok.lexpos,
            }
        )
    return result


if __name__ == "__main__":
    # Código de prueba con sintaxis de Rust
    test_code = """
// Módulo y uso de tipos
mod math {
    pub fn calculate(x: i32) -> i32 {
        return x * 2;
    }
}

use std::vec::Vec;

// Definición de struct y enum
struct Point {
    x: f64,
    y: f64
}

enum Option<T> {
    Some(T),
    None
}

// Implementación de trait
trait Shape {
    fn area(&self) -> f64;
}

// Función principal con control de flujo
fn main() {
    // Variables y tipos
    let mut count: i32 = 0;
    let pi: f64 = 3.14;
    const MAX_POINTS: u32 = 100;
    
    // Estructuras de control
    if count < 10 {
        count += 1;
    } else {
        count = 0;
    }

    // Loop y break
    loop {
        if count >= MAX_POINTS {
            break;
        }
        count += 1;
    }

    // Vector y Option
    let mut numbers: Vec<i32> = Vec::new();
    let maybe_number: Option<i32> = Some(42);
    
    // String con escapes
    let message = "Hello \\"Rust\\" world!\\n";
}
"""
    print("Tokenizando código Rust:")
    print(test_code)
    print("\nTokens encontrados:")
    tokens = tokenize_source(test_code)
    for token in tokens:
        print(
            f"Token: {token['type']}, Valor: {token['lexeme']}, Línea: {token['line']}, Col: {token['column']}"
        )
