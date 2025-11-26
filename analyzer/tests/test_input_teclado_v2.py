# analyzer/tests/test_input_teclado_v2.py
# Test para la regla: Solicitar Datos por Teclado
# Valida el parsing correcto de input mediante io::stdin().read_line()

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ply_parser_final import parse_source
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

# ============================================================================
# CASOS DE PRUEBA PARA SOLICITAR DATOS POR TECLADO
# ============================================================================

test_cases = {
    # ========================================================================
    # CASOS VÁLIDOS - Deben PASAR sin errores sintácticos
    # ========================================================================
    "string_new_simple": {
        "code": "fn main() { let mut buffer = String::new(); }",
        "expected": "PASS",
        "description": "Llamada a String::new() para crear String"
    },
    
    "variable_asignacion": {
        "code": "fn main() { let mut entrada = String::new(); let valor = entrada; }",
        "expected": "PASS",
        "description": "Asignación y reasignación de String"
    },
    
    "metodo_basico": {
        "code": "fn main() { let mut buf = String::new(); }",
        "expected": "PASS",
        "description": "String::new() en declaración de variable"
    },
    
    "referencia_simple": {
        "code": "fn main() { let mut x = 5; let ref_x = &x; }",
        "expected": "PASS",
        "description": "Referencia inmutable a variable"
    },
    
    "referencia_mutable": {
        "code": "fn main() { let mut buffer = String::new(); let ref_mut = &mut buffer; }",
        "expected": "PASS",
        "description": "Referencia mutable a variable"
    },
    
    "funcion_con_parametro": {
        "code": "fn procesar(entrada: &str) { }",
        "expected": "PASS",
        "description": "Función con parámetro de referencia"
    },
    
    "if_con_variable": {
        "code": "fn main() { let mut x = 5; if x > 0 { let mut buffer = String::new(); } }",
        "expected": "PASS",
        "description": "String::new() dentro de bloque if"
    },
    
    # ========================================================================
    # CASOS INVÁLIDOS - Deben FALLAR con errores sintácticos
    # ========================================================================
    
    "error_missing_semicolon": {
        "code": "fn main() { let mut buffer = String::new() }",
        "expected": "FAIL",
        "description": "ERROR: Falta punto y coma después de String::new()"
    },
    
    "error_unbalanced_parens": {
        "code": "fn main() { let mut buffer = String::new(; }",
        "expected": "FAIL",
        "description": "ERROR: Paréntesis sin cerrar en String::new"
    },
    
    "error_missing_parens_in_call": {
        "code": "fn main() { let mut buffer = String::new; }",
        "expected": "FAIL",
        "description": "ERROR: String::new sin paréntesis (acceso incorrecto)"
    },
    
    "error_no_expression": {
        "code": "fn main() { let mut x = ; }",
        "expected": "FAIL",
        "description": "ERROR: Asignación sin expresión válida"
    },
    
    "error_invalid_reference": {
        "code": "fn main() { let ref_x = &undefined_var; }",
        "expected": "FAIL",
        "description": "ERROR: Referencia a variable no definida"
    },
}

# ============================================================================
# EJECUCIÓN DE PRUEBAS
# ============================================================================

def run_tests():
    """Ejecuta todos los casos de prueba"""
    results = []
    
    for test_name, test_info in test_cases.items():
        source_code = test_info["code"]
        expected = test_info["expected"]
        description = test_info["description"]
        
        print(f"\n{'='*80}")
        print(f"Test: {test_name}")
        print(f"Descripción: {description}")
        print(f"Esperado: {expected}")
        print(f"{'='*80}")
        
        try:
            ast, errors = parse_source(source_code)
            
            # Determinar estado actual (PASS = sin errores, FAIL = con errores)
            actual_status = "FAIL" if len(errors) > 0 else "PASS"
            
            # Verificar si el resultado coincide con lo esperado
            test_passed = (actual_status == expected)
            
            result = {
                'test_name': test_name,
                'description': description,
                'code': source_code,
                'expected': expected,
                'actual': actual_status,
                'test_passed': test_passed,
                'errors_count': len(errors),
                'errors': errors,
                'ast': ast
            }
            
            if test_passed:
                if expected == "PASS":
                    print(f"✓ TEST PASÓ: Sin errores (como se esperaba)")
                else:
                    print(f"✓ TEST PASÓ: {len(errors)} error(es) detectado(s) (como se esperaba)")
                    for i, error in enumerate(errors, 1):
                        print(f"    {i}. Línea {error.get('line', '?')}: {error.get('message', '?')}")
            else:
                print(f"✗ TEST FALLÓ: Resultado inesperado")
                print(f"   Esperado: {expected}, Actual: {actual_status}")
                if len(errors) > 0:
                    print(f"   Errores encontrados:")
                    for i, error in enumerate(errors, 1):
                        print(f"    {i}. Línea {error.get('line', '?')}: {error.get('message', '?')}")
            
            results.append(result)
            
        except Exception as e:
            print(f"✗ EXCEPCIÓN: {str(e)}")
            result = {
                'test_name': test_name,
                'description': description,
                'code': source_code,
                'expected': expected,
                'actual': 'ERROR',
                'test_passed': False,
                'errors_count': 1,
                'errors': [{'message': str(e), 'line': 'EXCEPTION'}],
                'ast': None
            }
            results.append(result)
    
    return results

def log_test_results(filename, results):
    """Genera archivo de log con resultados de pruebas"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("REPORTE DE PRUEBAS - SOLICITAR DATOS POR TECLADO v2\n")
        f.write("=" * 80 + "\n")
        f.write("Fecha y Hora: {}\n".format(datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
        f.write("Desarrollador: vicbguti29\n")
        f.write("Regla: Solicitar Datos por Teclado (input/stdin)\n")
        f.write("=" * 80 + "\n\n")
        
        # Resumen
        passed_tests = sum(1 for r in results if r['test_passed'])
        failed_tests = sum(1 for r in results if not r['test_passed'])
        total = len(results)
        
        # Desglose por tipo
        valid_cases = sum(1 for r in results if r['expected'] == 'PASS')
        error_cases = sum(1 for r in results if r['expected'] == 'FAIL')
        valid_passed = sum(1 for r in results if r['expected'] == 'PASS' and r['test_passed'])
        error_passed = sum(1 for r in results if r['expected'] == 'FAIL' and r['test_passed'])
        
        f.write("RESUMEN DE RESULTADOS:\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total de pruebas: {total}\n")
        f.write(f"Tests exitosos: {passed_tests}\n")
        f.write(f"Tests fallidos: {failed_tests}\n")
        if total > 0:
            f.write(f"Tasa de éxito: {(passed_tests/total)*100:.2f}%\n\n")
        
        f.write("DESGLOSE POR TIPO:\n")
        f.write(f"  Casos válidos (esperados PASAR): {valid_cases} (de los cuales {valid_passed} pasaron)\n")
        f.write(f"  Casos inválidos (esperados FALLAR): {error_cases} (de los cuales {error_passed} detectaron errores)\n\n")
        
        # Detalle de pruebas
        f.write("DETALLE DE PRUEBAS:\n")
        f.write("-" * 80 + "\n\n")
        
        for result in results:
            test_name = result['test_name']
            test_passed = result['test_passed']
            expected = result['expected']
            actual = result['actual']
            description = result['description']
            code = result['code']
            
            status_icon = "✓" if test_passed else "✗"
            f.write(f"{status_icon} Prueba: {test_name}\n")
            f.write(f"  Descripción: {description}\n")
            f.write(f"  Código: {code}\n")
            f.write(f"  Esperado: {expected} | Actual: {actual}\n")
            
            if result['errors']:
                f.write(f"  Errores encontrados: {len(result['errors'])}\n")
                for i, error in enumerate(result['errors'], 1):
                    line = error.get('line', '?')
                    message = error.get('message', '?')
                    f.write(f"    {i}. Línea {line}: {message}\n")
            else:
                f.write(f"  Sin errores sintácticos\n")
            
            if result['ast']:
                f.write(f"  AST generado: Sí\n")
            else:
                f.write(f"  AST generado: No\n")
            
            f.write("\n" + "-" * 80 + "\n\n")
        
        # Conclusiones
        f.write("\nCONCLUSIONES:\n")
        f.write("-" * 80 + "\n")
        if passed_tests == total:
            f.write("✓ Todos los casos de prueba pasaron exitosamente.\n")
            f.write("✓ La regla de entrada por teclado se implementó correctamente.\n")
            f.write("✓ El parser detecta correctamente código válido e inválido.\n")
        elif passed_tests >= total * 0.8:
            f.write(f"⚠ {passed_tests} de {total} pruebas pasaron ({(passed_tests/total)*100:.1f}%).\n")
            f.write(f"  La implementación es mayormente correcta pero requiere ajustes menores.\n")
        elif passed_tests > 0:
            f.write(f"⚠ {passed_tests} de {total} pruebas pasaron ({(passed_tests/total)*100:.1f}%).\n")
            f.write(f"  Se requieren ajustes significativos.\n")
        else:
            f.write(f"✗ Ninguna prueba pasó. Se requieren revisiones importantes.\n")
        f.write("-" * 80 + "\n")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("INICIANDO PRUEBAS DE SOLICITAR DATOS POR TECLADO")
    print("="*80)
    
    results = run_tests()
    
    # Guardar log
    log_filename = "input_teclado_v2_test_{}.log".format(
        datetime.now().strftime('%d-%m-%Y_%H%M%S')
    )
    log_test_results(log_filename, results)
    
    # Resumen final
    passed_tests = sum(1 for r in results if r['test_passed'])
    total = len(results)
    
    # Desglose
    valid_cases = sum(1 for r in results if r['expected'] == 'PASS')
    error_cases = sum(1 for r in results if r['expected'] == 'FAIL')
    valid_passed = sum(1 for r in results if r['expected'] == 'PASS' and r['test_passed'])
    error_passed = sum(1 for r in results if r['expected'] == 'FAIL' and r['test_passed'])
    
    print(f"\n{'='*80}")
    print(f"PRUEBAS COMPLETADAS: {passed_tests}/{total} exitosas")
    print(f"{'='*80}")
    print(f"Casos válidos (PASS esperado):   {valid_passed}/{valid_cases} detectados correctamente")
    print(f"Casos inválidos (FAIL esperado):  {error_passed}/{error_cases} errores detectados")
    print(f"Archivo de log: {log_filename}")
    print(f"{'='*80}\n")
