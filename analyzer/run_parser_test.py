#!/usr/bin/env python
# analyzer/run_parser_test.py
# Script para ejecutar el parser sintáctico sobre test_sintactico.rs

import sys
import os
from datetime import datetime
from ply_parser_final import parse_source, log_syntax_errors

def main():
    # Leer el archivo test_sintactico.rs
    test_file = 'test_sintactico.rs'
    
    if not os.path.exists(test_file):
        print(f"Error: No se encontró el archivo {test_file}")
        sys.exit(1)
    
    with open(test_file, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    print("=" * 80)
    print("ANALIZADOR SINTÁCTICO - PRUEBA")
    print("=" * 80)
    print(f"\nAnalizando archivo: {test_file}\n")
    
    # Analizar el código
    ast, errors = parse_source(source_code)
    
    print("\n" + "=" * 80)
    print("RESULTADOS DEL ANÁLISIS")
    print("=" * 80)
    
    if ast:
        print(f"\n[OK] Análisis completado (AST generado)")
    else:
        print(f"\n[ERROR] Errores encontrados durante el análisis")
    
    print(f"\nTotal de errores sintácticos: {len(errors)}")
    
    if errors:
        print("\n" + "-" * 80)
        print("DETALLE DE ERRORES:")
        print("-" * 80)
        for i, error in enumerate(errors, 1):
            print(f"\n{i}. Error en línea {error['line']}")
            print(f"   Mensaje: {error['message']}")
            print(f"   Token encontrado: {error['token']}")
            print(f"   Tipo de token: {error['type']}")
    
    # Crear archivo de log
    timestamp = datetime.now().strftime("%d%m%Y-%H%M")
    log_filename = f"sintactico-vicbguti29-{timestamp}.txt"
    
    print(f"\n" + "-" * 80)
    print(f"Generando archivo de log: {log_filename}")
    
    log_syntax_errors(log_filename, errors, source_code)
    
    print(f"Archivo de log creado exitosamente")
    print("=" * 80)
    
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
