# analyzer/ply_lexer.py
# Lexer ágil usando PLY para prototipado y pruebas rápidas
import codecs
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
    # Macros
    "CONSOLE_PRINT", # println!
    "VEC_CREATE",    # vec!
    # Errores
    "ERROR",         # Token para caracteres no reconocidos
    # Operadores y símbolos
    "PLUS",  # +
    "MINUS",  # -
    "TIMES",  # *
    "DIVIDE",  # /
    "MODULO", # %
    "EQUALS",  # =
    "ARROW",  # ->
    "DOTDOT",  # ..
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
    "LBRACKET", # [
    "RBRACKET", # ]
    "SEMICOLON",  # ;
    "COLON",  # :
    "COMMA",  # ,
    # Operadores de referencia
    "AMPERSAND", # &
    # Comentarios
    "COMMENT",  # // comentarios
    "DOC_COMMENT", # /// comentarios
)
# Palabras reservadas de Rust
reserved = {
    "if": "IF", "else": "ELSE", "while": "WHILE", "for": "FOR", "loop": "LOOP", 
    "break": "BREAK", "continue": "CONTINUE", "fn": "FN", "let": "LET", "mut": "MUT", 
    "return": "RETURN", "const": "CONST", "static": "STATIC", "i32": "I32", 
    "i64": "I64", "u32": "U32", "u64": "U64", "f32": "F32", "f64": "F64", 
    "bool": "BOOL", "char": "CHAR", "str": "STR", "String": "STRING_TYPE", 
    "true": "TRUE", "false": "FALSE", "struct": "STRUCT", "enum": "ENUM", 
    "mod": "MOD", "use": "USE", "pub": "PUB", "self": "SELF", "Self": "SELF_TYPE", 
    "trait": "TRAIT", "impl": "IMPL", "where": "WHERE", "Box": "BOX", "Vec": "VEC", 
    "Option": "OPTION", "Some": "SOME", "None": "NONE", "println": "PRINTLN", 
    "input": "INPUT", "in": "IN",
}

# --- Reglas de Tokens ---

# Operadores compuestos (deben ir primero)
def t_ARROW(t): r'->'; t.literal = t.value; return t
def t_DOTDOT(t): r'\.\.'; t.literal = t.value; return t
def t_EQ(t): r'=='; t.literal = t.value; return t
def t_NEQ(t): r'!='; t.literal = t.value; return t
def t_LTE(t): r'<='; t.literal = t.value; return t
def t_GTE(t): r'>='; t.literal = t.value; return t
def t_PLUS_EQUALS(t): r'\+='; t.literal = t.value; return t
def t_MINUS_EQUALS(t): r'-='; t.literal = t.value; return t
def t_TIMES_EQUALS(t): r'\*='; t.literal = t.value; return t
def t_DIVIDE_EQUALS(t): r'/='; t.literal = t.value; return t
def t_AND(t): r'&&'; t.literal = t.value; return t
def t_OR(t): r'\|\|'; t.literal = t.value; return t

# Operadores y delimitadores simples
t_PLUS = r"\+"; t_MINUS = r"-"; t_TIMES = r"\*"; t_DIVIDE = r"/"; t_MODULO = r"%"; t_EQUALS = r"="
t_LPAREN = r"\("; t_RPAREN = r"\)"; t_LBRACE = r"\{"; t_RBRACE = r"\}"
t_LBRACKET = r"\["; t_RBRACKET = r"\]"
t_SEMICOLON = r";"
t_COLON = r":"; t_COMMA = r","; t_NOT = r"!"; t_LT = r"<"; t_GT = r">"; t_AMPERSAND = r"&"

# Reglas para macros específicas (deben ir ANTES de t_identifier)
def t_CONSOLE_PRINT(t):
    r'(println|print|eprintln|eprint)!'
    t.literal = t.value
    return t

def t_VEC_CREATE(t):
    r'vec!'
    t.literal = t.value
    return t

# Identificadores y palabras clave
def t_identifier(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = reserved.get(t.value, "IDENT")
    if t.type == 'TRUE':
        t.literal = True
    elif t.type == 'FALSE':
        t.literal = False
    else:
        t.literal = t.value
    return t

# Literales
def t_float(t):
    r"\d+\.\d+([eE][+-]?\d+)?"
    t.type = "FLOAT"
    t.literal = float(t.value)
    return t

def t_number(t):
    r"\d+"
    t.type = "NUMBER"
    t.literal = int(t.value)
    return t

def t_string(t):
    r"\"([^\\\n]|(\\.))*?\""
    t.type = "STRING"
    # El orden es CRÍTICO. Reemplazar la doble barra PRIMERO.
    s = t.value[1:-1]
    s = s.replace('\\\\', '\\')  # 1. Convertir \\ a \
    s = s.replace('\\"', '"')   # 2. Convertir \" a "
    s = s.replace("\\'", "'")
    s = s.replace('\\n', '\n')   # 3. Convertir \n a newline
    s = s.replace('\\t', '\t')   # 4. Convertir \t a tab
    s = s.replace('\\r', '\r')
    t.literal = s
    return t

def t_char(t):
    r"'([^'\\\n]|\\.)'"
    t.type = "CHAR"
    t.literal = codecs.decode(t.value[1:-1], 'unicode_escape')
    return t

# Comentarios
def t_doc_comment(t):
    r"///.*"
    pass  # Ignorar

def t_comment(t):
    r"//.*"
    pass  # Ignorar

def t_ignore_multiline_comment(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

# Utilidades
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

t_ignore = " \t"

def t_error(t):
    """
    Maneja los caracteres ilegales creando un token de ERROR.
    """
    t.type = "ERROR"
    t.value = t.value[0]
    t.literal = f"Illegal character '{t.value[0]}'"
    t.lexer.skip(1)
    return t

# --- Construcción y Ejecución ---

lexer = lex.lex()

def tokenize_source(source):
    lexer.lineno = 1
    lexer.input(source)
    result = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        
        # Para los tokens simples sin función, el literal no se asigna automáticamente.
        # Lo asignamos aquí si no existe.
        literal = getattr(tok, 'literal', tok.value)

        result.append({
            "type": tok.type,
            "value": tok.value,
            "line": tok.lineno,
            "column": tok.lexpos,
            "literal": literal
        })
    return result

if __name__ == "__main__":
    test_code = 'let message = "Hello \\"Rust\\" world!\\n";'
    tokens = tokenize_source(test_code)
    for token in tokens:
        print(f"Token: type={token['type']}, value='{token['value']}', literal='{token['literal']}' (type: {type(token['literal'])})")