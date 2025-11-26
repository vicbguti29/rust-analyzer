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
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
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
    """let_stmt : LET IDENT EQUALS initializer SEMICOLON
                | LET IDENT COLON type EQUALS initializer SEMICOLON
                | LET MUT IDENT EQUALS initializer SEMICOLON
                | LET MUT IDENT COLON type EQUALS initializer SEMICOLON
                | LET IDENT COLON type SEMICOLON
                | LET MUT IDENT COLON type SEMICOLON"""
    line_no = p.lineno(1)
    
    # Case: let mut ...
    if p[2] == 'mut':
        var_name = p[3]
        # Case: let mut name : type = value ; (len 9)
        if len(p) == 9:
            p[0] = ('let_mut', var_name, p[5], p[7], line_no)
        # Case: let mut name = value ; (len 7)
        elif p[4] == '=':
            p[0] = ('let_mut', var_name, None, p[5], line_no)
        # Case: let mut name : type ; (len 7)
        else: # p[4] must be ':'
            p[0] = ('let_mut', var_name, p[5], None, line_no)
    # Case: let ...
    else:
        var_name = p[2]
        # Case: let name : type = value ; (len 8)
        if len(p) == 8:
            p[0] = ('let', var_name, p[4], p[6], line_no)
        # Case: let name = value ; (len 6)
        elif p[3] == '=':
            p[0] = ('let', var_name, None, p[4], line_no)
        # Case: let name : type ; (len 6)
        else: # p[3] must be ':'
            p[0] = ('let', var_name, p[4], None, line_no)


# Constante
def p_const_stmt(p):
    """const_stmt : CONST IDENT COLON type EQUALS initializer SEMICOLON"""
    p[0] = ('const', p[2], p[4], p[6])


# Variable estática
def p_static_stmt(p):
    """static_stmt : STATIC IDENT COLON type EQUALS initializer SEMICOLON
                   | STATIC MUT IDENT COLON type EQUALS initializer SEMICOLON"""
    if len(p) == 8:  # Without mut
        p[0] = ('static', p[2], p[4], p[6])
    else:  # With mut
        p[0] = ('static_mut', p[3], p[5], p[7])


# Tipos de datos
def p_type(p):
    """type : AMPERSAND base_type
            | base_type"""
    if len(p) == 3:
        p[0] = '&' + p[2]
    else:
        p[0] = p[1]

def p_base_type(p):
    """base_type : I32
                 | I64
                 | U32
                 | U64
                 | F32
                 | F64
                 | BOOL
                 | CHAR
                 | STR
                 | STRING_TYPE
                 | SELF_TYPE
                 | IDENT"""
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
            | expr DIVIDE expr
            | expr MODULO expr"""
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
    # Guardamos el tipo de token junto con el valor literal para
    # poder distinguir entre un IDENT (nombre de variable) y un STRING.
    p[0] = ('literal', p.slice[1].literal, p.slice[1].type)

# Array literal
def p_expr_array_literal(p):
    """expr : LBRACKET exprs RBRACKET
            | LBRACKET RBRACKET"""
    if len(p) == 4:
        p[0] = ('array_literal', p[2])
    else:
        p[0] = ('array_literal', [])

def p_expr_array_repeat_syntax(p):
    """expr : LBRACKET expr SEMICOLON expr RBRACKET"""
    p[0] = ('array_repeat', p[2], p[4])




# ============================================================================
# REGLA 4: ESTRUCTURAS DE CONTROL - if (MÍNIMO 1)
# RESPONSABILIDAD: vicbguti29 (solo if)
# ============================================================================

# If-else simple (RESPONSABILIDAD DE vicbguti29)
def p_stmt_if(p):
    """stmt : IF expr LBRACE opt_stmts RBRACE
            | IF expr LBRACE opt_stmts RBRACE ELSE LBRACE opt_stmts RBRACE"""
    if len(p) == 6:
        p[0] = ('if', p[2], p[4])
    else:
        p[0] = ('if_else', p[2], p[4], p[8])


def p_stmt_println(p):
    """stmt : CONSOLE_PRINT LPAREN STRING RPAREN SEMICOLON
            | CONSOLE_PRINT LPAREN STRING COMMA exprs RPAREN SEMICOLON"""
    if len(p) == 6:
        p[0] = ('println', p[3], [])
    else:
        p[0] = ('println', p[3], p[5])


# While loop
def p_stmt_while(p):
    """stmt : WHILE expr LBRACE opt_stmts RBRACE"""
    p[0] = ('while_loop', p[2], p[4])


# For loop
def p_stmt_for(p):
    """stmt : FOR IDENT IN expr LBRACE opt_stmts RBRACE"""
    p[0] = ('for_loop', p[2], p[4], p[6])


# Infinite loop
def p_stmt_loop(p):
    """stmt : LOOP LBRACE opt_stmts RBRACE"""
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
            | RETURN initializer SEMICOLON"""
    if len(p) == 3:
        p[0] = ('return_stmt', None)  # return;
    else:
        p[0] = ('return_stmt', p[2])  # return <expr>;



# ============================================================================
# REGLA 5: ESTRUCTURA DE DATOS - struct (MÍNIMO 1)
# RESPONSABILIDAD: vicbguti29 (solo definición básica)
# ============================================================================

def p_struct_decl(p):
    """struct_decl : STRUCT IDENT LBRACE opt_fields RBRACE"""
    p[0] = ('struct', p[2], p[4])

def p_opt_fields(p):
    """opt_fields : non_empty_fields
                  | non_empty_fields COMMA
                  | empty"""
    p[0] = p[1] if p[1] else []

def p_non_empty_fields(p):
    """non_empty_fields : field
                       | non_empty_fields COMMA field"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_field(p):
    """field : IDENT COLON type"""
    p[0] = ('field', p[1], p[3])


# Enum declaration
def p_enum_decl(p):
    """enum_decl : ENUM IDENT LBRACE opt_enum_variants RBRACE"""
    p[0] = ('enum_decl', p[2], p[4])

def p_opt_enum_variants(p):
    """opt_enum_variants : non_empty_enum_variants
                         | non_empty_enum_variants COMMA
                         | empty"""
    p[0] = p[1] if p[1] else []

def p_non_empty_enum_variants(p):
    """non_empty_enum_variants : IDENT
                               | non_empty_enum_variants COMMA IDENT"""
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
                    | FN IDENT LPAREN params_list RPAREN ARROW type SEMICOLON
                    | FN IDENT LPAREN RPAREN ARROW type SEMICOLON"""
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
    """impl_block : IMPL IDENT FOR IDENT LBRACE impl_items_opt RBRACE
                  | IMPL IDENT LBRACE impl_items_opt RBRACE"""
    if len(p) == 8:  # impl Trait for Struct
        p[0] = ('impl_block', p[2], p[4], p[6]) # (impl_block, Trait, Struct, items)
    else:  # impl Struct
        p[0] = ('impl_block', p[2], None, p[4]) # (impl_block, Struct, None, items)

def p_impl_items_opt(p):
    """impl_items_opt : impl_items
                      | empty"""
    p[0] = p[1] if p[1] else []

def p_impl_items(p):
    """impl_items : function_decl
                  | impl_items function_decl"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]



# Struct initialization (as a specific initializer, not a general expression)
def p_struct_init(p):
    """struct_init : IDENT LBRACE RBRACE"""
    p[0] = ('struct_init', p[1], [])

def p_initializer(p):
    """initializer : expr
                   | struct_init"""
    p[0] = p[1]

# Input expression
def p_expr_input(p):
    """expr : INPUT LPAREN RPAREN"""
    p[0] = ('input_expr',)

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
    """function_decl : FN IDENT LPAREN params_list RPAREN LBRACE opt_stmts RBRACE
                     | FN IDENT LPAREN RPAREN LBRACE opt_stmts RBRACE
                     | FN IDENT LPAREN params_list RPAREN ARROW type LBRACE opt_stmts RBRACE
                     | FN IDENT LPAREN RPAREN ARROW type LBRACE opt_stmts RBRACE"""
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
    """param : IDENT COLON type
             | AMPERSAND SELF""" # Añadir &self
    if len(p) == 4:
        p[0] = ('param', p[1], p[3])
    else:
        p[0] = ('param', p[1] + p[2], None) # &self, tipo None por ahora

# TODO: Funciones con múltiples parámetros - A CARGO DE COMPAÑERO


# ============================================================================
# REGLA 8: ENTRADA - input
# RESPONSABILIDAD: vicbguti29
# ============================================================================

def p_stmt_assign(p):
    """stmt : IDENT EQUALS initializer SEMICOLON
            | IDENT PLUS_EQUALS expr SEMICOLON
            | IDENT MINUS_EQUALS expr SEMICOLON
            | IDENT TIMES_EQUALS expr SEMICOLON
            | IDENT DIVIDE_EQUALS expr SEMICOLON"""
    p[0] = ('assign', p[1], p[2], p[3], p.lineno(1))


# ============================================================================
# AYUDANTES
# ============================================================================

def p_opt_stmts(p):
    """opt_stmts : stmts
                 | empty"""
    p[0] = p[1] if p[1] else []

def p_stmts(p):
    """stmts : stmt
             | stmts stmt"""
    if len(p) == 2:
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

    # Reiniciar el estado del lexer para cada análisis para asegurar un estado limpio
    lexer.lineno = 1
    
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