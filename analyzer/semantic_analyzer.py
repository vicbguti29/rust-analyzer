# analyzer/semantic_analyzer.py
# Analizador Semántico para el compilador de Rust.
# Autor: Alvascon, vicbguti29

from datetime import datetime

# --- TABLA DE SÍMBOLOS CON GESTIÓN DE SCOPES ---
# Autor: vicbguti29
class SymbolTable:
    """
    Tabla de símbolos con soporte para múltiples niveles de alcance (scopes).
    Permite registrar identificadores con sus tipos, mutabilidad y el alcance en que fueron declarados.
    """
    
    def __init__(self):
        # Pila de scopes: cada elemento es un diccionario de símbolos en ese scope
        self.scopes = [{}]  # Scope global inicial
        self.scope_stack = [0]  # Pila que rastrea índices de scope activos
        
    def enter_scope(self):
        """Entra a un nuevo alcance (bloque de código)."""
        self.scopes.append({})
        self.scope_stack.append(len(self.scopes) - 1)
    
    def exit_scope(self):
        """Sale del alcance actual."""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
    
    def add(self, name, type, is_mutable=False, line_no=None):
        """
        Añade un símbolo al alcance actual.
        El símbolo se registra con su tipo, mutabilidad y línea de declaración.
        """
        current_scope_idx = self.scope_stack[-1]
        self.scopes[current_scope_idx][name] = {
            'type': type,
            'is_mutable': is_mutable,
            'scope_level': len(self.scope_stack) - 1,
            'line_declared': line_no
        }
    
    def lookup(self, name):
        """
        Busca un símbolo en la tabla, comenzando desde el alcance actual
        y subiendo hasta el alcance global.
        Retorna una tupla (symbol_info, scope_level) si lo encuentra,
        o (None, None) si no lo encuentra.
        """
        # Recorrer scopes desde el actual hacia atrás (hacia el global)
        for scope_idx in reversed(self.scope_stack):
            if name in self.scopes[scope_idx]:
                return self.scopes[scope_idx][name], scope_idx
        return None, None
    
    def lookup_current_scope_only(self, name):
        """
        Busca un símbolo solo en el alcance actual.
        Retorna el símbolo si lo encuentra, None si no.
        """
        current_scope_idx = self.scope_stack[-1]
        return self.scopes[current_scope_idx].get(name)

# -------------------------------------------------

class SemanticAnalyzer:
    
    """
    Recorre el Árbol de Sintaxis Abstracta (AST) generado por el parser
    para realizar el análisis semántico, como la comprobación de tipos,
    alcance de variables e identificadores.
    """
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.in_loop = False  # Rastrear si estamos dentro de un loop
        self.in_function = False  # Rastrear si estamos dentro de una función

    def visit(self, node):
        if node is None: return
        method_name = f'visit_{node[0]}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        """Visita todos los sub-nodos de forma recursiva."""
        for element in node[1:]:
            if isinstance(element, tuple):
                self.visit(element)  # Esto llamará al visit_* correcto
            elif isinstance(element, list):
                for item in element:
                    if isinstance(item, tuple):
                        self.visit(item)

    def enter_scope(self):
        """Entra a un nuevo alcance (bloque de código)."""
        self.symbol_table.enter_scope()

    def exit_scope(self):
        """Sale del alcance actual."""
        self.symbol_table.exit_scope()

    # --- LÓGICA DE EVALUACIÓN DE TIPOS Y VALIDACIÓN DE IDENTIFICADORES ---
    def get_expression_type(self, expr_node, line_no=None):
        """
        Evalúa y devuelve el tipo de un nodo de expresión.
        También valida la existencia de identificadores (REGLA 1 - vicbguti29).
        """
        if not expr_node or not isinstance(expr_node, tuple):
            return 'unknown'

        node_type = expr_node[0]
        
        if node_type == 'literal':
            # AST: ('literal', value, token_type)
            value, token_type = expr_node[1], expr_node[2]

            # Si el literal es un IDENT, es una variable. Buscamos su tipo.
            if token_type == 'IDENT':
                symbol, _ = self.symbol_table.lookup(value)
                if symbol:
                    return symbol['type']
                else:
                    # REGLA 1: Validación de Existencia
                    if line_no:
                        error_msg = f"Error Semántico (Línea {line_no}): Identificador no encontrado. La variable '{value}' no ha sido declarada en este alcance."
                        self.errors.append(error_msg)
                    return 'undeclared'
            
            # Para otros literales, determinamos el tipo por su valor en Python.
            if token_type == 'NUMBER': return 'i32'
            if token_type == 'FLOAT': return 'f64'
            if token_type == 'TRUE' or token_type == 'FALSE': return 'bool'
            if token_type == 'STRING': return '&str'

        elif node_type == 'struct_init':
            return expr_node[1]

        elif node_type == 'array_literal':
            elements = expr_node[1]
            if not elements:
                return '[<unknown>; 0]'
            first_elem_type = self.get_expression_type(elements[0], line_no)
            return f'[{first_elem_type}; {len(elements)}]'

        elif node_type == 'tuple_literal':
            elements = expr_node[1]
            if not elements:
                return '()'
            elem_types = [self.get_expression_type(e, line_no) for e in elements]
            return f'({", ".join(elem_types)})'

        return 'unknown'

    # --- LÓGICA PARA REGLAS SEMÁNTICAS ---

    def visit_program(self, node):
        _program, statements = node
        for stmt in statements:
            self.visit(stmt)

    # Manejo de scope de función y verificación de return
    def visit_fn(self, node):
        _fn, _name, _params, _ret_type, body = node
        
        # Entrar en contexto de función
        old_in_function = self.in_function
        self.in_function = True
        
        self.enter_scope()
        for stmt in body:
            self.visit(stmt)
        self.exit_scope()
        
        # Salir del contexto de función
        self.in_function = old_in_function

    # ============================================================================
    # REGLA 3: DISCREPANCIA DE TIPOS EN DECLARACIÓN EXPLÍCITA
    # RESPONSABILIDAD: Alvascon
    # ============================================================================
    def visit_let(self, node):
        # AST: ('let', var_name, declared_type, expr_node, line_no)
        _let, var_name, declared_type, expr_node, line_no = node
        
        # Visitar la expresión para análisis de operaciones
        self.visit(expr_node)
        
        evaluated_type = self.get_expression_type(expr_node)

        if declared_type and evaluated_type != 'unknown' and declared_type != evaluated_type:
            error_msg = f"Error Semántico (Línea {line_no}): Discrepancia de tipos. Se esperaba tipo '{declared_type}' pero se encontró tipo '{evaluated_type}' en la asignación de '{var_name}'."
            self.errors.append(error_msg)
            return

        final_type = declared_type or evaluated_type
        self.symbol_table.add(var_name, final_type, is_mutable=False)

    def visit_let_mut(self, node):
        # AST: ('let_mut', var_name, declared_type, expr_node, line_no)
        _let, var_name, declared_type, expr_node, line_no = node
        
        # Visitar la expresión para análisis de operaciones
        self.visit(expr_node)
        
        evaluated_type = self.get_expression_type(expr_node)

        if declared_type and evaluated_type != 'unknown' and declared_type != evaluated_type:
            error_msg = f"Error Semántico (Línea {line_no}): Discrepancia de tipos. Se esperaba tipo '{declared_type}' pero se encontró tipo '{evaluated_type}' en la asignación de '{var_name}'."
            self.errors.append(error_msg)
            return

        final_type = declared_type or evaluated_type
        self.symbol_table.add(var_name, final_type, is_mutable=True)

    # ============================================================================
    # REGLA 1: VALIDACIÓN DE EXISTENCIA DE IDENTIFICADORES
    # RESPONSABILIDAD: vicbguti29
    # Se aplica en visit_assign para validar que la variable fue declarada
    # antes de ser usada en una asignación.
    # ============================================================================
    
    # ============================================================================
    # REGLA 2: ALCANCE LOCAL (SCOPE ANALYSIS)
    # RESPONSABILIDAD: vicbguti29
    # Se aplica al buscar identificadores: no se puede acceder a variables
    # declaradas en un alcance interno si se accede desde un alcance externo.
    # ============================================================================
    def visit_assign(self, node):
        # AST: ('assign', var_name, operator, expr_node, line_no)
        _assign, var_name, _op, expr_node, line_no = node
        
        # Visitar la expresión para análisis de operaciones
        self.visit(expr_node)

        symbol, symbol_scope_idx = self.symbol_table.lookup(var_name)
        
        # REGLA 1 (Validación de Existencia - vicbguti29)
        if not symbol:
            error_msg = f"Error Semántico (Línea {line_no}): Identificador no encontrado. La variable '{var_name}' no ha sido declarada en este alcance."
            self.errors.append(error_msg)
            return

        # REGLA 2 (Alcance Local - vicbguti29)
        # Validar que la variable fue declarada en el scope actual o en un scope superior
        current_scope_level = len(self.symbol_table.scope_stack) - 1
        var_scope_level = symbol['scope_level']
        
        # Si la variable se declaró en un scope más interno que el actual, no es accesible
        if var_scope_level > current_scope_level:
            error_msg = f"Error Semántico (Línea {line_no}): El identificador '{var_name}' no es accesible. Fue definido en un alcance interno que ya finalizó."
            self.errors.append(error_msg)
            return

        # REGLA 5 (Validación de Mutabilidad - Alvascon)
        if not symbol['is_mutable']:
            error_msg = f"Error Semántico (Línea {line_no}): No se puede asignar a la variable inmutable '{var_name}'. Las variables deben ser declaradas con 'mut' para poder ser reasignadas."
            self.errors.append(error_msg)
            return # Detenemos el análisis para esta línea

        # REGLA 4 (Discrepancia de Tipos en Reasignación - Alvascon)
        new_type = self.get_expression_type(expr_node)
        
        if new_type != 'unknown' and symbol['type'] != new_type:
            error_msg = f"Error Semántico (Línea {line_no}): Discrepancia de tipos en la reasignación. La variable '{var_name}' tiene el tipo '{symbol['type']}', pero se intentó asignar un valor de tipo '{new_type}'."
            self.errors.append(error_msg)

    # ============================================================================
    # REGLA 6: COMPATIBILIDAD DE TIPOS EN OPERACIONES ARITMÉTICAS
    # RESPONSABILIDAD: vicbguti29
    # ============================================================================
    def visit_binop(self, node):
        # AST: ('binop', left_expr, operator, right_expr)
        _binop, left_expr, operator, right_expr = node
        
        left_type = self.get_expression_type(left_expr)
        right_type = self.get_expression_type(right_expr)
        
        # Ambos deben ser numéricos
        numeric_types = {'i32', 'i64', 'u32', 'u64', 'f32', 'f64'}
        
        if left_type not in numeric_types and left_type != 'unknown':
            error_msg = f"Error Semántico: Operador aritmético '{operator}' no puede aplicarse a tipo '{left_type}'. Se esperaba un tipo numérico."
            self.errors.append(error_msg)
            return
        
        if right_type not in numeric_types and right_type != 'unknown':
            error_msg = f"Error Semántico: Operador aritmético '{operator}' no puede aplicarse a tipo '{right_type}'. Se esperaba un tipo numérico."
            self.errors.append(error_msg)
            return
        
        # Los tipos deben coincidir
        if left_type != 'unknown' and right_type != 'unknown' and left_type != right_type:
            error_msg = f"Error Semántico: Operador aritmético '{operator}' no puede aplicarse a tipos '{left_type}' y '{right_type}'. No existe una implementación para esta operación."
            self.errors.append(error_msg)

    # ============================================================================
    # REGLA 7: RESTRICCIÓN DE TIPO EN OPERADORES LÓGICOS
    # RESPONSABILIDAD: vicbguti29
    # ============================================================================
    def visit_and(self, node):
        # AST: ('and', left_expr, right_expr)
        _and, left_expr, right_expr = node
        
        left_type = self.get_expression_type(left_expr)
        right_type = self.get_expression_type(right_expr)
        
        if left_type != 'bool' and left_type != 'unknown':
            error_msg = f"Error Semántico: Operador lógico '&&' no puede aplicarse al tipo '{left_type}'. Se esperaba 'bool'."
            self.errors.append(error_msg)
        
        if right_type != 'bool' and right_type != 'unknown':
            error_msg = f"Error Semántico: Operador lógico '&&' no puede aplicarse al tipo '{right_type}'. Se esperaba 'bool'."
            self.errors.append(error_msg)

    def visit_or(self, node):
        # AST: ('or', left_expr, right_expr)
        _or, left_expr, right_expr = node
        
        left_type = self.get_expression_type(left_expr)
        right_type = self.get_expression_type(right_expr)
        
        if left_type != 'bool' and left_type != 'unknown':
            error_msg = f"Error Semántico: Operador lógico '||' no puede aplicarse al tipo '{left_type}'. Se esperaba 'bool'."
            self.errors.append(error_msg)
        
        if right_type != 'bool' and right_type != 'unknown':
            error_msg = f"Error Semántico: Operador lógico '||' no puede aplicarse al tipo '{right_type}'. Se esperaba 'bool'."
            self.errors.append(error_msg)

    def visit_not(self, node):
        # AST: ('not', expr)
        _not, expr = node
        
        expr_type = self.get_expression_type(expr)
        
        if expr_type != 'bool' and expr_type != 'unknown':
            error_msg = f"Error Semántico: Operador lógico '!' no puede aplicarse al tipo '{expr_type}'. Se esperaba 'bool'."
            self.errors.append(error_msg)

    # ============================================================================
    # VERIFICACIÓN DE FLUJO DE CONTROL
    # RESPONSABILIDAD: vicbguti29
    # Verifica que break y return se usen en contextos válidos
    # ============================================================================
    def visit_while_loop(self, node):
        # AST: ('while_loop', condition, body)
        _while, _condition, body = node
        
        old_in_loop = self.in_loop
        self.in_loop = True
        
        for stmt in body:
            self.visit(stmt)
        
        self.in_loop = old_in_loop

    def visit_for_loop(self, node):
        # AST: ('for_loop', var, range_expr, body)
        _for, _var, _range_expr, body = node
        
        old_in_loop = self.in_loop
        self.in_loop = True
        
        for stmt in body:
            self.visit(stmt)
        
        self.in_loop = old_in_loop

    def visit_infinite_loop(self, node):
        # AST: ('infinite_loop', body)
        _loop, body = node
        
        old_in_loop = self.in_loop
        self.in_loop = True
        
        for stmt in body:
            self.visit(stmt)
        
        self.in_loop = old_in_loop

    def visit_break_stmt(self, node):
        # AST: ('break_stmt',)
        if not self.in_loop:
            error_msg = "Error Semántico: 'break' solo puede usarse dentro de un bucle (while, for, loop)."
            self.errors.append(error_msg)

    def visit_continue_stmt(self, node):
        # AST: ('continue_stmt',)
        if not self.in_loop:
            error_msg = "Error Semántico: 'continue' solo puede usarse dentro de un bucle (while, for, loop)."
            self.errors.append(error_msg)

    def visit_return_stmt(self, node):
        # AST: ('return_stmt', expr_or_none)
        if not self.in_function:
            error_msg = "Error Semántico: 'return' solo puede usarse dentro de una función."
            self.errors.append(error_msg)

    def visit_if(self, node):
        # AST: ('if', condition, body)
        _if, _condition, body = node
        
        self.enter_scope()
        for stmt in body:
            self.visit(stmt)
        self.exit_scope()

    def visit_if_else(self, node):
        # AST: ('if_else', condition, if_body, else_body)
        _if_else, _condition, if_body, else_body = node
        
        self.enter_scope()
        for stmt in if_body:
            self.visit(stmt)
        self.exit_scope()
        
        self.enter_scope()
        for stmt in else_body:
            self.visit(stmt)
        self.exit_scope()

    def visit_comparison(self, node):
        # AST: ('comparison', left_expr, operator, right_expr)
        # Procesar normalmente, comparaciones pueden ser de cualquier tipo que soporte el operador
        _comparison, left_expr, _operator, right_expr = node
        self.visit(left_expr)
        self.visit(right_expr)

    def visit_range(self, node):
        # AST: ('range', start, end)
        # Verificar que inicio y fin sean numéricos
        _range, start, end = node
        start_type = self.get_expression_type(start)
        end_type = self.get_expression_type(end)
        
        numeric_types = {'i32', 'i64', 'u32', 'u64', 'f32', 'f64'}
        if start_type not in numeric_types and start_type != 'unknown':
            error_msg = f"Error Semántico: Rango debe tener inicio numérico, se encontró '{start_type}'."
            self.errors.append(error_msg)
        if end_type not in numeric_types and end_type != 'unknown':
            error_msg = f"Error Semántico: Rango debe tener fin numérico, se encontró '{end_type}'."
            self.errors.append(error_msg)


# Punto de entrada para el análisis semántico (FUNCION PRINCIPAL).
# Toma un AST y devuelve una lista de errores semánticos encontrados.
def semantic(ast):
    analyzer = SemanticAnalyzer()
    analyzer.visit(ast)
    return analyzer.errors

# Genera archivo de log con los errores semánticos encontrados
def log_semantic_errors(filename, errors, source_code, developer="vicbguti29"):
    """
    Genera un archivo de log con los resultados del análisis semántico.
    
    Args:
        filename: Ruta del archivo de log
        errors: Lista de errores semánticos encontrados
        source_code: Código fuente analizado
        developer: Nombre del desarrollador (default: vicbguti29)
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("REPORTE DE ANÁLISIS SEMÁNTICO\n")
        f.write("=" * 80 + "\n")
        f.write("Fecha y Hora: {}".format(datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + "\n")
        f.write(f"Desarrollador: {developer}" + "\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("REGLAS SEMÁNTICAS IMPLEMENTADAS:\n")
        f.write("-" * 80 + "\n")
        f.write("1. Validación de Existencia de Identificadores (REGLA 1)\n")
        f.write("   - Verifica que toda variable/función sea declarada antes de usarse\n")
        f.write("   - Busca el identificador desde el alcance actual hasta el global\n")
        f.write("\n2. Alcance Local (REGLA 2)\n")
        f.write("   - Verifica que variables no sean accedidas fuera de su alcance\n")
        f.write("   - No se puede acceder a variables de alcances internos finalizados\n")
        f.write("-" * 80 + "\n\n")
        
        f.write("CÓDIGO FUENTE ANALIZADO:\n")
        f.write("-" * 80 + "\n")
        f.write(source_code)
        f.write("\n" + "-" * 80 + "\n\n")
        
        if errors:
            f.write(f"ERRORES SEMÁNTICOS ENCONTRADOS: {len(errors)}" + "\n")
            f.write("-" * 80 + "\n")
            for i, error in enumerate(errors, 1):
                f.write(f"\n{i}. {error}" + "\n")
        else:
            f.write("ANÁLISIS SEMÁNTICO COMPLETADO SIN ERRORES" + "\n")