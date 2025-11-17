# Analizador Léxico, Sintáctico y Semántico - Rust

Proyecto de análisis de código Rust utilizando PLY (Python Lex-Yacc) con interfaz web moderna.

## 🚀 Características

- **Análisis Léxico**: Tokenización completa del código Rust
- **Análisis Sintáctico**: Validación de estructura gramatical y generación de AST
- **Análisis Semántico**: Verificación de tipos, scope y reglas del lenguaje
- **Interfaz Web**: Editor de código integrado con visualización de resultados
- **Logs Automáticos**: Generación de logs por cada análisis realizado
- **API REST**: Backend con FastAPI para fácil integración

## 📁 Estructura del Proyecto

```
rust-analyzer/
├── frontend/         # Interfaz web (HTML/CSS/JS)
├── backend/          # API REST con FastAPI
├── analyzer/         # Módulos de análisis PLY
├── logs/             # Logs generados por análisis
└── docs/             # Documentación del proyecto
```
### Algortimos de prueba

**ubicación:** rust-analyzer/docs/algoritmos_de_prueba

```
algoritmos_de_prueba/
├── algoritmo_de_prueba.rs     # Algoritmo de prueba de Angello Vasconez
├── test_lexer.rs              # Algortimo de prueba de Victor Borbor
├── test_sintactico.rs         # Algortimo de prueba para el analizador sintáctico
├── prb_sintactico_valido.rs   # Algortimo de prueba para el sintactico, genera correctamente el AST
├── prb_sintactico_errores.rs  # Algortimo de prueba para el sintactico, presenta errores
└── prb_semantico.rs           # Algortimo de prueba para el analizador semantico, presenta casos válidos e inválidos
```

### Ejecución de pruebas del Analizador Sintáctico

1. Primero asigna la ruta del archivo que quiere correr en el archivo **'tests/run_parser_test.py'** tal como se muestra a continuación:
 
```python
def main():
    # Usar la ruta relativa desde la raíz del proyecto
    # OPCIONES PARA PRUEBAS:
    # 'docs/algoritmos_de_prueba/test_sintactico.rs'
    # 'docs/algoritmos_de_prueba/prb_sintactico_valido.rs'
    # 'docs/algoritmos_de_prueba/prb_sintactico_errores.rs'
    test_file = 'docs/algoritmos_de_prueba/prb_sintactico_valido.rs'
```
2. Despues desde el terminal debe ubicarse en la ruta **'rust-analyzer/analyzer/tests'**
3. Asegurese de tener los requerimientos del proyecto (requerimientos.txt) indicados en el backend o un entono virtual con los requerimientos
4. finalmente corra el archivo **'run_parser_test.py'** con el comando: 

```bash
python run_parser_test.py
```

### Ejecución de pruebas del Analizador Semántico

1. Primerp asigna la ruta del archivo que quiere correr en el archivo **'tests/run_semantic_test.py'** tal como se muestra a continuación:
 
```python
def main():
    # Apuntar al nuevo archivo de pruebas semánticas
    # OPCIONES PARA PRUEBAS:
    # ''docs/algoritmos_de_prueba/prb_semantico.rs''
    test_file = 'docs/algoritmos_de_prueba/prb_semantico.rs'
```
2. Despues desde el terminal debe ubicarse en la ruta **'rust-analyzer/analyzer/tests'**
3. Asegurese de tener los requerimientos del proyecto (requerimientos.txt) indicados en el backend o un entono virtual con los requerimientos
4. finalmente corra el archivo **'run_semantic_test.py'** con el comando: 
```bash
python run_semantic_test.py
```


## 🛠️ Tecnologías

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Análisis**: PLY (Python Lex-Yacc)
- **Deploy**: Railway/Render + Vercel/Netlify

## 📖 Documentación

- [Propuesta del Proyecto](docs/statement.md)
- [Arquitectura Técnica](docs/arquitectura.md)
- [Manual del analizador léxico](docs/lexer/ply_lexer_manual.md)
- [Manual del analizador Sintáctico](docs/parser/ply_parser_manual.md)
- [Manual del analizador Semántico](docs/semantic/semantic_analyzer_manual.md)

## 🚦 Inicio Rápido

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
# API disponible en http://localhost:8000
```

### Frontend
```bash
cd frontend
python -m http.server 3000
# Abrir http://localhost:3000
```

## 👥 Equipo

Ver asignación de tareas en [statement.md](docs/statement.md)

## 📝 Licencia

Proyecto académico - Todos los derechos reservados
