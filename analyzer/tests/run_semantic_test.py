#!/usr/bin/env python
# analyzer/tests/run_semantic_test.py
# Script para ejecutar el parser y el analizador semántico.

import sys
import os
from datetime import datetime

# Añadir la raíz del proyecto al sys.path para permitir importaciones absolutas
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from analyzer.ply_parser_final import parse_source
from analyzer.semantic_analyzer import semantic, log_semantic_errors

def main():
    # Apuntar al nuevo archivo de pruebas semánticas
    test_file = 'docs/algoritmos_de_prueba/prb_existencia_scope.rs'
    
    if not os.path.exists(test_file):
        print(f"Error: No se encontró el archivo {test_file}")
        sys.exit(1)
    
    with open(test_file, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    # --- 1. ANÁLISIS SINTÁCTICO ---
    print("=" * 80)
    print("FASE 1: ANÁLISIS SINTÁCTICO")
    print("=" * 80)
    print(f"\nAnalizando archivo: {test_file}\n")
    
    ast, syntax_errors = parse_source(source_code)
    
    if syntax_errors:
        print(f"[ERROR] Se encontraron {len(syntax_errors)} errores sintácticos. El análisis semántico no se ejecutará.")
        # Imprimir errores sintácticos...
        for i, error in enumerate(syntax_errors, 1):
            print(f"\n{i}. Error en línea {error['line']}: {error['message']}")
        return 1
    
    if not ast:
        print("[ERROR] No se pudo generar el AST. El análisis semántico no se ejecutará.")
        return 1

    print("[OK] Análisis sintáctico completado. AST generado.\n")

    # --- 2. ANÁLISIS SEMÁNTICO ---
    print("=" * 80)
    print("FASE 2: ANÁLISIS SEMÁNTICO")
    print("=" * 80)
    
    semantic_errors = semantic(ast)
    
    if not semantic_errors:
        print("\n[OK] Análisis semántico completado. No se encontraron errores.")
    else:
        print(f"\n[ERROR] Se encontraron {len(semantic_errors)} errores semánticos.")
        print("-" * 80)
        for i, error in enumerate(semantic_errors, 1):
            print(f"{i}. {error}")
        print("-" * 80)

    # --- 3. GENERACIÓN DE LOG ---
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%d%m%Y-%Hh%M")
    log_filename = f"semantico-vicbguti29-{timestamp}.txt"
    log_filepath = os.path.join(log_dir, log_filename)
    
    print("\n" + "=" * 80)
    print(f"Generando archivo de log: {log_filepath}")
    
    log_semantic_errors(log_filepath, semantic_errors, source_code, developer="vicbguti29")
    
    print(f"Archivo de log creado exitosamente.")
    print("=" * 80)
    
    return 0 if not semantic_errors else 1


if __name__ == "__main__":
    sys.exit(main())
