# analyzer/semantic_analyzer.py
# Analizador Semántico para el compilador de Rust.
# Autor: Alvascon

from datetime import datetime

# --- ¡VERSIÓN MOCK/FALSA para desarrollo!---
# ELIMINAR UNA VEZ SE CREE LA TABLA REAL
class MockSymbolTable:
    
    #Una tabla de símbolos falsa (mock) para permitir el desarrollo independiente
    #de las reglas de análisis semántico. Simula la adición y búsqueda de
    #símbolos en un diccionario simple.
    
    def __init__(self):
        self.symbols = {}
        print("ADVERTENCIA: Usando MockSymbolTable. La gestión de scopes y existencia real no está implementada.")

    def add(self, name, type, is_mutable=False):
        #Simula añadir un símbolo a la tabla.
        print(f"[MockTable] Símbolo añadido: {name} (Tipo: {type}, Mutable: {is_mutable})")
        self.symbols[name] = {'type': type, 'is_mutable': is_mutable}

    def lookup(self, name):
        #Simula buscar un símbolo en la tabla.
        print(f"[MockTable] Buscando símbolo: {name}")
        return self.symbols.get(name)

# -------------------------------------------------

class SemanticAnalyzer:
    
    #Recorre el Árbol de Sintaxis Abstracta (AST) generado por el parser
    #para realizar el análisis semántico, como la comprobación de tipos.
    
    def __init__(self):
        self.symbol_table = MockSymbolTable()
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

    # --- LÓGICA DE EVALUACIÓN DE TIPOS ---
    def get_expression_type(self, expr_node):
        
        #Evalúa y devuelve el tipo de un nodo de expresión
        if not expr_node or not isinstance(expr_node, tuple):
            return 'unknown'

        node_type = expr_node[0]
        
        if node_type == 'literal':
            # AST: ('literal', value, token_type)
            value, token_type = expr_node[1], expr_node[2]

            # Si el literal es un IDENT, es una variable. Buscamos su tipo.
            if token_type == 'IDENT':
                symbol = self.symbol_table.lookup(value)
                if symbol:
                    return symbol['type']
                else:
                    # El error de "variable no encontrada" lo gestionará otra regla.
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
            first_elem_type = self.get_expression_type(elements[0])
            return f'[{first_elem_type}; {len(elements)}]'

        elif node_type == 'tuple_literal':
            elements = expr_node[1]
            if not elements:
                return '()'
            elem_types = [self.get_expression_type(e) for e in elements]
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
    # REGLA 1: VALIDACIÓN DE EXISTENCIA
    # REGLA 2: ALCANCE LOCAL
    # RESPONSABILIDAD: vicbguti29
    # (La lógica de estas reglas se implementará principalmente en SymbolTable
    # y se usará aquí, en visit_assign y otros lugares).
    # ============================================================================

    # ============================================================================
    # REGLA 4: DISCREPANCIA DE TIPOS EN REASIGNACIÓN
    # REGLA 5: VALIDACIÓN DE MUTABILIDAD EN REASIGNACIÓN
    # RESPONSABILIDAD: Alvascon
    # ============================================================================
    def visit_assign(self, node):
        # AST: ('assign', var_name, operator, expr_node, line_no)
        _assign, var_name, _op, expr_node, line_no = node

        symbol = self.symbol_table.lookup(var_name)
        
        # REGLA 1 (Validación de Existencia - vicbguti29) se aplica aquí.
        if not symbol:
            # El error "variable no declarada" se generará aquí cuando
            # la SymbolTable real esté implementada.
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
def log_semantic_errors(filename, errors, source_code):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("REPORTE DE ANÁLISIS SEMÁNTICO\n")
        f.write("=" * 80 + "\n")
        f.write("Fecha y Hora: {}".format(datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + "\n")
        f.write("Desarrollador: Alvasconv" + "\n")
        f.write("=" * 80 + "\n\n")
        
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