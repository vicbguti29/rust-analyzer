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

    def visit(self, node):
        if node is None: return
        method_name = f'visit_{node[0]}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        for element in node[1:]:
            if isinstance(element, tuple):
                self.visit(element)
            elif isinstance(element, list):
                for item in element:
                    if isinstance(item, tuple):
                        self.visit(item)

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

    # Placeholder para futuro manejo de scope de función
    def visit_fn(self, node):
        _fn, _name, _params, _ret_type, body = node
        for stmt in body:
            self.visit(stmt)

    # ============================================================================
    # REGLA 3: DISCREPANCIA DE TIPOS EN DECLARACIÓN EXPLÍCITA
    # RESPONSABILIDAD: Alvascon
    # ============================================================================
    def visit_let(self, node):
        # AST: ('let', var_name, declared_type, expr_node, line_no)
        _let, var_name, declared_type, expr_node, line_no = node
        
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