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
├── logs/            # Logs generados por análisis
└── docs/            # Documentación del proyecto
```
### Algortimos de prueba

**ubicación:** rust-analyzer/analyzer
```
analyzer/
├── algoritmo_de_prueba.rs   # Algoritmo de prueba de Angello Vasconez
├── test_lexer.rs            # Algortimo de prueba de Victor Borbor
```


## 🛠️ Tecnologías

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Análisis**: PLY (Python Lex-Yacc)
- **Deploy**: Railway/Render + Vercel/Netlify

## 📖 Documentación

- [Propuesta del Proyecto](statement.md)
- [Arquitectura Técnica](docs/arquitectura.md)

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

Ver asignación de tareas en [statement.md](statement.md)

## 📝 Licencia

Proyecto académico - Todos los derechos reservados
