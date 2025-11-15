# analyzer/ply_parser_final.py
# Parser sintáctico final para Rust - Versión simplificada y robusta
# Desarrollador: vicbguti29
#
# RESPONSABILIDADES ASIGNADAS:
# - Impresión (println!)
# - Ingreso de datos (input)
# - Expresiones aritméticas con uno o más operadores
# - Condiciones con uno o más conectores lógicos
# - Asignación de variables con todos los tipos
# - Mínimo: 1 estructura de datos, 1 estructura de control, 1 función

import ply.yacc as yacc
from .ply_lexer import tokens, lexer
from datetime import datetime
import logging # Usaremos logging para la salida de debug

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

# Precedencia de operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ', 'LT', 'LTE', 'GT', 'GTE'),
    ('left', 'DOTDOT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'NOT'),
)

# Lista para almacenar errores sintácticos
syntax_errors = []

# ============================================================================
# REGLAS SINTACTICAS - VERSIÓN SIMPLE Y ROBUSTA
# ============================================================================

# Programa: lista de items (funciones, structs, constantes, etc.)
def p_program(p):
    """program : items
               | empty"""
    p[0] = ('program', p[1] if p[1] else [])


def p_items(p):
    """items : item
             | items item"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]


# Items top-level
def p_item(p):
    """item : function_decl
            | struct_decl
            | const_stmt
            | static_stmt
            | enum_decl
            | trait_decl
            | impl_block""" # Añadir impl_block aquí
    p[0] = p[1]


# ============================================================================
# REGLA 1: ASIGNACIÓN DE VARIABLES - Let, Const, Static
# RESPONSABILIDAD: vicbguti29
# ============================================================================

# Variable let (mutable o no)
def p_let_stmt(p):
    """let_stmt : LET IDENT EQUALS expr SEMICOLON
                | LET IDENT COLON TYPE EQUALS expr SEMICOLON
                | LET MUT IDENT EQUALS expr SEMICOLON
                | LET MUT IDENT COLON TYPE EQUALS expr SEMICOLON"""
    if len(p) == 6:
        p[0] = ('let', p[2], None, p[4])
    elif len(p) == 8 and p[3] == ':':
        p[0] = ('let', p[2], p[4], p[6])
    elif len(p) == 8:
        p[0] = ('let_mut', p[3], None, p[5])
    else:
        p[0] = ('let_mut', p[3], p[5], p[7])


# Constante
def p_const_stmt(p):
    """const_stmt : CONST IDENT COLON TYPE EQUALS expr SEMICOLON"""
    p[0] = ('const', p[2], p[4], p[6])


# Variable estática
def p_static_stmt(p):
    """static_stmt : STATIC IDENT COLON TYPE EQUALS expr SEMICOLON"""
    p[0] = ('static', p[2], p[4], p[6])


# Tipos de datos
def p_type(p):
    """TYPE : I32
            | I64
            | U32
            | U64
            | F32
            | F64
            | BOOL
            | CHAR
            | STR
            | STRING_TYPE"""
    p[0] = p[1]


# ============================================================================
# REGLA 2: EXPRESIONES ARITMETICAS
# RESPONSABILIDAD: vicbguti29
# ============================================================================

# Expresión aritmética
def p_expr_arithmetic(p):
    """expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr"""
    p[0] = ('binop', p[1], p[2], p[3])


# Comparación
def p_expr_comparison(p):
    """expr : expr EQ expr
            | expr NEQ expr
            | expr LT expr
            | expr LTE expr
            | expr GT expr
            | expr GTE expr"""
    p[0] = ('comparison', p[1], p[2], p[3])


# Expresión de rango
def p_expr_range(p):
    """expr : expr DOTDOT expr"""
    p[0] = ('range', p[1], p[3])


# ============================================================================
# REGLA 3: CONECTORES LOGICOS
# RESPONSABILIDAD: vicbguti29
# ============================================================================

def p_expr_and(p):
    """expr : expr AND expr"""
    p[0] = ('and', p[1], p[3])


def p_expr_or(p):
    """expr : expr OR expr"""
    p[0] = ('or', p[1], p[3])


def p_expr_not(p):
    """expr : NOT expr"""
    p[0] = ('not', p[2])


# Parentesis
def p_expr_paren(p):
    """expr : LPAREN expr RPAREN"""
    p[0] = p[2]



# Literales
def p_expr_literal(p):
    """expr : IDENT
            | NUMBER
            | FLOAT
            | STRING
            | TRUE
            | FALSE"""
    # p.slice[1] es el objeto Token completo. Usamos su campo 'literal'
    # que ya fue procesado por el lexer (ej. convirtió '5' a 5).
    p[0] = ('literal', p.slice[1].literal)

# Array literal
def p_expr_array_literal(p):
    """expr : LBRACKET exprs RBRACKET
            | LBRACKET RBRACKET"""
    if len(p) == 4:
        p[0] = ('array_literal', p[2])
    else:
        p[0] = ('array_literal', [])




# ============================================================================
# REGLA 4: ESTRUCTURAS DE CONTROL - if (MÍNIMO 1)
# RESPONSABILIDAD: vicbguti29 (solo if)
# ============================================================================

# If-else simple (RESPONSABILIDAD DE vicbguti29)
def p_stmt_if(p):
    """stmt : IF expr LBRACE stmts RBRACE
            | IF expr LBRACE stmts RBRACE ELSE LBRACE stmts RBRACE"""
    if len(p) == 6:
        p[0] = ('if', p[2], p[4])
    else:
        p[0] = ('if_else', p[2], p[4], p[8])



# While loop
def p_stmt_while(p):
    """stmt : WHILE expr LBRACE stmts RBRACE"""
    p[0] = ('while_loop', p[2], p[4])


# For loop
def p_stmt_for(p):
    """stmt : FOR IDENT IN expr LBRACE stmts RBRACE"""
    p[0] = ('for_loop', p[2], p[4], p[6])


# Infinite loop
def p_stmt_loop(p):
    """stmt : LOOP LBRACE stmts RBRACE"""
    p[0] = ('infinite_loop', p[3])


# Break statement
def p_stmt_break(p):
    """stmt : BREAK SEMICOLON"""
    p[0] = ('break_stmt',)


# Continue statement
def p_stmt_continue(p):
    """stmt : CONTINUE SEMICOLON"""
    p[0] = ('continue_stmt',)


# Return statement
def p_stmt_return(p):
    """stmt : RETURN SEMICOLON
            | RETURN expr SEMICOLON"""
    if len(p) == 3:
        p[0] = ('return_stmt', None)  # return;
    else:
        p[0] = ('return_stmt', p[2])  # return <expr>;



# ============================================================================
# REGLA 5: ESTRUCTURA DE DATOS - struct (MÍNIMO 1)
# RESPONSABILIDAD: vicbguti29 (solo definición básica)
# ============================================================================

def p_struct_decl(p):
    """struct_decl : STRUCT IDENT LBRACE fields RBRACE
                   | STRUCT IDENT LBRACE RBRACE"""
    p[0] = ('struct', p[2], p[4] if len(p) == 6 else [])


def p_fields(p):
    """fields : field
              | fields COMMA field"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]


def p_field(p):
    """field : IDENT COLON TYPE"""
    p[0] = ('field', p[1], p[3])


# Enum declaration
def p_enum_decl(p):
    """enum_decl : ENUM IDENT LBRACE enum_variants RBRACE
                 | ENUM IDENT LBRACE RBRACE"""
    p[0] = ('enum_decl', p[2], p[4] if len(p) == 6 else [])

def p_enum_variants(p):
    """enum_variants : IDENT
                     | enum_variants COMMA IDENT"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# Trait declaration
def p_trait_decl(p):
    """trait_decl : TRAIT IDENT LBRACE trait_items RBRACE
                  | TRAIT IDENT LBRACE RBRACE"""
    p[0] = ('trait_decl', p[2], p[4] if len(p) == 6 else [])

def p_trait_items(p):
    """trait_items : fn_signature
                   | trait_items fn_signature"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

def p_fn_signature(p):
    """fn_signature : FN IDENT LPAREN params_list RPAREN SEMICOLON
                    | FN IDENT LPAREN RPAREN SEMICOLON
                    | FN IDENT LPAREN params_list RPAREN ARROW TYPE SEMICOLON
                    | FN IDENT LPAREN RPAREN ARROW TYPE SEMICOLON"""
    if len(p) == 7: # Con parámetros, sin retorno
        p[0] = ('fn_signature', p[2], p[4], None)
    elif len(p) == 6: # Sin parámetros, sin retorno
        p[0] = ('fn_signature', p[2], [], None)
    elif len(p) == 10: # Con parámetros, con retorno
        p[0] = ('fn_signature', p[2], p[4], p[7])
    else: # Sin parámetros, con retorno
        p[0] = ('fn_signature', p[2], [], p[6])

# Impl block
def p_impl_block(p):
    """impl_block : IMPL IDENT LBRACE impl_items RBRACE
                  | IMPL IDENT LBRACE RBRACE"""
    p[0] = ('impl_block', p[2], p[4] if len(p) == 6 else [])

def p_impl_items(p):

    """impl_items : function_decl

                  | impl_items function_decl"""

    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]



# Struct initialization (as an expression)

def p_expr_struct_init(p):

    """expr : IDENT LBRACE RBRACE"""

    p[0] = ('struct_init', p[1], [])

# Tuple literal
def p_expr_tuple_literal(p):
    """expr : LPAREN RPAREN
            | LPAREN exprs COMMA RPAREN
            | LPAREN exprs RPAREN"""
    if len(p) == 3: # Empty tuple () or single parenthesized expression (expr)
        if p[2] == ')': # Empty tuple
            p[0] = ('tuple_literal', [])
        else: # This case should ideally be handled by p_expr_paren, but adding for completeness
            p[0] = p[2] # Parenthesized expression
    elif len(p) == 5: # Single element tuple (expr,) or multi-element tuple (expr, expr, ...)
        p[0] = ('tuple_literal', p[2])
    else: # Multi-element tuple (expr, expr, ...)
        p[0] = ('tuple_literal', p[2])




# TODO: Otras estructuras de datos (impl) - A CARGO DE COMPAÑERO


# ============================================================================
# REGLA 6: FUNCIONES (MÍNIMO 1)
# RESPONSABILIDAD: vicbguti29 (solo función simple sin parámetros)
# ============================================================================

# Función simple sin parámetros y sin retorno
def p_function_decl(p):
    """function_decl : FN IDENT LPAREN params_list RPAREN LBRACE stmts RBRACE
                     | FN IDENT LPAREN RPAREN LBRACE stmts RBRACE
                     | FN IDENT LPAREN params_list RPAREN ARROW TYPE LBRACE stmts RBRACE
                     | FN IDENT LPAREN RPAREN ARROW TYPE LBRACE stmts RBRACE"""
    if len(p) == 9: # Con parámetros, sin retorno
        p[0] = ('fn', p[2], p[4], None, p[7])
    elif len(p) == 8: # Sin parámetros, sin retorno
        p[0] = ('fn', p[2], [], None, p[6])
    elif len(p) == 11: # Con parámetros, con retorno
        p[0] = ('fn', p[2], p[4], p[7], p[9])
    else: # Sin parámetros, con retorno
        p[0] = ('fn', p[2], [], p[6], p[8])

def p_params_list(p):
    """params_list : param
                   | params_list COMMA param"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_param(p):
    """param : IDENT COLON TYPE
             | AMPERSAND SELF""" # Añadir &self
    if len(p) == 4:
        p[0] = ('param', p[1], p[3])
    else:
        p[0] = ('param', p[1] + p[2], None) # &self, tipo None por ahora

# TODO: Funciones con múltiples parámetros - A CARGO DE COMPAÑERO


# ============================================================================
# REGLA 7: IMPRESION - println!
# RESPONSABILIDAD: vicbguti29
# ============================================================================

def p_stmt_println(p):
    """stmt : CONSOLE_PRINT LPAREN STRING RPAREN SEMICOLON
            | CONSOLE_PRINT LPAREN STRING COMMA exprs RPAREN SEMICOLON"""
    if len(p) == 6:
        p[0] = ('println', p[3], [])
    else:
        p[0] = ('println', p[3], p[5])


# ============================================================================
# REGLA 8: ENTRADA - input
# RESPONSABILIDAD: vicbguti29
# ============================================================================

def p_stmt_input(p):
    """stmt : LET IDENT EQUALS INPUT LPAREN RPAREN SEMICOLON
            | LET MUT IDENT EQUALS INPUT LPAREN RPAREN SEMICOLON"""
    p[0] = ('input', p[2] if len(p) == 8 else p[3])


# ============================================================================
# REGLA 9: REASIGNACION
# RESPONSABILIDAD: vicbguti29
# ============================================================================

def p_stmt_assign(p):
    """stmt : IDENT EQUALS expr SEMICOLON
            | IDENT PLUS_EQUALS expr SEMICOLON
            | IDENT MINUS_EQUALS expr SEMICOLON
            | IDENT TIMES_EQUALS expr SEMICOLON
            | IDENT DIVIDE_EQUALS expr SEMICOLON"""
    p[0] = ('assign', p[1], p[2], p[3])


# ============================================================================
# AYUDANTES
# ============================================================================

def p_stmts(p):
    """stmts : stmt
             | stmts stmt
             | empty"""
    if p[1] is None:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_stmt_with_var(p):
    """stmt : let_stmt"""
    p[0] = p[1]


def p_exprs(p):
    """exprs : expr
             | exprs COMMA expr"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]


def p_empty(p):
    """empty :"""
    p[0] = None


# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

def p_error(p):
    if p:
        msg = "Syntax error at line {}: unexpected token '{}' ({})".format(
            p.lineno, p.value, p.type
        )
        syntax_errors.append({
            'line': p.lineno,
            'message': msg,
            'token': str(p.value),
            'type': p.type
        })
    else:
        msg = "Syntax error at EOF"
        syntax_errors.append({
            'line': 'EOF',
            'message': msg,
            'token': None,
            'type': None
        })


# Construir el parser
parser = yacc.yacc(debug=False, write_tables=False)


def parse_source(source):
    """Analiza código fuente Rust"""
    global syntax_errors
    syntax_errors = []
    
    try:
        result = parser.parse(source, lexer=lexer, debug=False)
        return result, syntax_errors
    except Exception as e:
        syntax_errors.append({
            'line': 'error',
            'message': str(e),
            'token': None,
            'type': None
        })
        return None, syntax_errors


def log_syntax_errors(filename, errors, source_code):
    """Genera archivo de log con los errores encontrados"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("REPORTE DE ANALISIS SINTACTICO\n")
        f.write("=" * 80 + "\n")
        f.write("Fecha y Hora: {}\n".format(datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
        f.write("Desarrollador: Alvasconv\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("CODIGO FUENTE ANALIZADO:\n")
        f.write("-" * 80 + "\n")
        f.write(source_code)
        f.write("\n" + "-" * 80 + "\n\n")
        
        if errors:
            f.write("ERRORES ENCONTRADOS: {}\n".format(len(errors)))
            f.write("-" * 80 + "\n")
            for i, error in enumerate(errors, 1):
                f.write("\n{}. Error en Linea {}\n".format(i, error.get('line', '?')))
                f.write("   Mensaje: {}\n".format(error.get('message', '?')))
                if error.get('token'):
                    f.write("   Token: {}\n".format(error['token']))
        else:
            f.write("ANALISIS COMPLETADO SIN ERRORES\n")