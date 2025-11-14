# Arquitectura del Proyecto - Analizador Rust

## Estructura de Directorios

```
rust-analyzer/
├── frontend/                       # Interfaz web del usuario
│   ├── index.html                  # Estructura HTML de la aplicación
│   ├── style.css                   # Estilos y diseño visual
│   └── app.js                      # Lógica del cliente y comunicación con API
│         
├── backend/                        # Servidor API REST
│   ├── main.py                     # FastAPI server con endpoints de análisis
│   └── requirements.txt            # Dependencias Python del backend
│         
├── analyzer/                       # Módulos de análisis (PLY)
│   ├── lexer.py                    # Analizador léxico - Tokenización
│   ├── parser.py                   # Analizador sintáctico - AST
│   ├── semantic.py                 # Analizador semántico - Validaciones
│   └── tests/                      # Casos de prueba de los analizadores
│
├── logs/                           # Logs de análisis generados
│   └── [tipo]-[dev]-[fecha].txt
│
└── docs/                           # Documentación del proyecto
    ├── statement.md                # Propuesta del proyecto
    ├── arquitectura.md             # Este archivo
    ├── algoritmos_de_prueba/                      
    │   └── algoritmo_de_prueba.rs  
    │   └── test_lexer.rs           
    │   └── test_sintactico.rs      
    ├── lexer/                      
    │   └── ply_lexer_manual.md     # Guía del analizador léxico
    ├── parser/                      
    │   └── REGLAS_SINTACTICAS.md   # Reglas con las estructuras sitacticas correctas para Rust    
    └── semantic/                              
```

## Descripción de Archivos

### Frontend (`frontend/`)

**index.html**
- Estructura base de la aplicación web
- Layout de dos columnas (editor + resultados)
- Pestañas para mostrar tokens, errores y AST
- Botones de acción para cargar archivos y ejecutar análisis

**style.css**
- Implementa el diseño visual propuesto en el punto 7
- Paleta de colores Nord Theme (#2E3440, #D8DEE9, #A3BE8C, etc.)
- Layout responsivo con grid CSS
- Estilos para tokens, errores y estado de la aplicación

**app.js**
- Gestión del editor de código y números de línea
- Comunicación con backend via Fetch API
- Visualización de resultados (tokens, errores, AST)
- Actualización de estado y logs en tiempo real

### Backend (`backend/`)

**main.py**
- API REST con FastAPI
- Endpoints:
  - `POST /analyze/lexico` - Análisis léxico del código
  - `POST /analyze/sintactico` - Análisis sintáctico
  - `POST /analyze/semantico` - Análisis semántico
  - `POST /analyze/completo` - Análisis completo
- Generación automática de logs con formato especificado
- Manejo de errores y respuestas JSON

**requirements.txt**
- `fastapi` - Framework web moderno y rápido
- `uvicorn` - Servidor ASGI para FastAPI
- `pydantic` - Validación de datos
- `ply` - Python Lex-Yacc para análisis léxico y sintáctico

### Analyzer (`analyzer/`)

**lexer.py** - Analizador Léxico
- **Propósito**: Convertir código fuente Rust en tokens
- **Componentes a implementar**:
  - Definición de palabras reservadas de Rust (fn, let, if, etc.)
  - Patrones regex para identificadores, números, strings
  - Operadores aritméticos, lógicos y de asignación
  - Delimitadores (paréntesis, llaves, punto y coma)
  - Manejo de comentarios (// y /* */)
- **Salida**: Lista de tokens con tipo, valor y línea
- **Errores**: Tokens no reconocidos marcados como ERROR

**parser.py** - Analizador Sintáctico
- **Propósito**: Validar la estructura gramatical del código
- **Componentes a implementar**:
  - Gramática BNF para Rust
  - Reglas para declaración de variables (let, mut, const)
  - Reglas para estructuras de control (if, while, for, match)
  - Reglas para funciones y sus parámetros
  - Expresiones aritméticas y booleanas con precedencia
  - Estructuras de datos (Vec, arrays, structs)
- **Salida**: Árbol Sintáctico Abstracto (AST)
- **Errores**: Errores de sintaxis con línea y descripción

**semantic.py** - Analizador Semántico
- **Propósito**: Validar reglas semánticas del lenguaje
- **Componentes a implementar**:
  - Tabla de símbolos para variables y funciones
  - Verificación de tipos de datos
  - Validación de variables declaradas antes de usarse
  - Verificación de retorno de funciones
  - Alcance de variables (scope)
  - Uso de variables mutables (mut)
- **Salida**: Lista de errores semánticos o confirmación
- **Errores**: Tipo incorrecto, variable no declarada, etc.

### Logs (`logs/`)

**Formato de archivos**: `[tipo_analisis]-[desarrollador]-[DD-MM-YYYY-HH:MM].txt`

**Ejemplos**:
- `lexico-rodrigosaraguro-24-10-2025-15:30.txt`
- `sintactico-marialopez-25-10-2025-10:45.txt`
- `completo-juanperez-26-10-2025-14:20.txt`

**Contenido del log**:
```
=== ANÁLISIS [TIPO] ===
Desarrollador: [nombre]
Fecha: DD-MM-YYYY HH:MM:SS

CÓDIGO:
[código analizado]

TOKENS: (si aplica)
  TYPE                 | VALUE                         | Línea

ERRORES: (si existen)
  Línea X: [descripción del error]

✓ Estado final del análisis
```

## Flujo de Trabajo

1. **Usuario** escribe o carga código Rust en el editor
2. **Frontend** envía código al backend via POST request
3. **Backend** recibe el código y lo pasa al analizador correspondiente
4. **Analyzer** procesa el código y devuelve tokens/AST/errores
5. **Backend** genera log automáticamente y devuelve respuesta JSON
6. **Frontend** muestra resultados en las pestañas correspondientes

## Tecnologías

- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Análisis**: PLY (Python Lex-Yacc)
- **Deploy**: Railway/Render (backend), Vercel/Netlify (frontend)
- **CI/CD**: GitHub Actions

## API Endpoints

### POST /analyze/lexico
```json
Request:
{
  "code": "fn main() { ... }",
  "developer": "nombre"
}

Response:
{
  "status": "success|error",
  "tokens": [
    {"type": "FN", "value": "fn", "line": 1}
  ],
  "errors": [],
  "log_file": "lexico-nombre-24-10-2025-15:30.txt"
}
```

### POST /analyze/sintactico
Similar al léxico, pero incluye campo `ast` en la respuesta.

### POST /analyze/semantico
Devuelve lista de errores semánticos detectados.

### POST /analyze/completo
Ejecuta los tres análisis en secuencia.

## Asignación de Tareas

Cada integrante del equipo deberá implementar:
- **Analizador Léxico**: Al menos 1 tipo de variable/dato estructurado
- **Analizador Sintáctico**: 1 estructura de control + 1 tipo de función + 1 estructura de datos
- **Analizador Semántico**: Reglas semánticas asignadas según especialización

Ver tabla de asignaciones en `statement.md` sección 5.

## Despliegue

### Local
```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py  # http://localhost:8000

# Frontend
cd frontend
# Abrir index.html en navegador o usar servidor local
python -m http.server 3000  # http://localhost:3000
```

### Producción
- **Backend**: Railway/Render (gratuito con límites)
- **Frontend**: Vercel/Netlify (gratuito)
- **CI/CD**: GitHub Actions automático en cada push

## Próximos Pasos

1. Inicializar repositorio Git
2. Crear repositorio en GitHub
3. Configurar CI/CD con GitHub Actions
4. Asignar tareas específicas a cada integrante
5. Implementar analizadores progresivamente (Avances 1, 2, 3)
6. Realizar pruebas y documentar resultados
