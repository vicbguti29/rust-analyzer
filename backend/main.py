from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os
import sys

# Agregar el directorio analyzer al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from analyzer.lexer import Lexer
# from analyzer.parser import RustParser
# from analyzer.semantic import SemanticAnalyzer

app = FastAPI(
    title="Analizador Léxico, Sintáctico y Semántico - Rust",
    description="API para análisis de código Rust usando PLY",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class CodeInput(BaseModel):
    code: str
    developer: str = "anonymous"

class TokenOutput(BaseModel):
    type: str
    value: str
    line: int

class ErrorOutput(BaseModel):
    type: str
    message: str
    line: int = None

class AnalysisResponse(BaseModel):
    status: str
    tokens: list[TokenOutput] = []
    errors: list[ErrorOutput] = []
    ast: dict = None
    log_file: str = None

# Directorio de logs
LOGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

def generate_log_filename(analysis_type: str, developer: str) -> str:
    """Genera nombre de archivo de log según el formato especificado"""
    timestamp = datetime.now().strftime("%d-%m-%Y-%H:%M")
    filename = f"{analysis_type}-{developer}-{timestamp}.txt"
    return os.path.join(LOGS_DIR, filename)

def save_log(filename: str, content: str):
    """Guarda el contenido del análisis en un archivo de log"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

@app.get("/")
async def root():
    return {
        "message": "API del Analizador Léxico, Sintáctico y Semántico para Rust",
        "endpoints": {
            "/analyze/lexico": "POST - Análisis léxico",
            "/analyze/sintactico": "POST - Análisis sintáctico",
            "/analyze/semantico": "POST - Análisis semántico",
            "/analyze/completo": "POST - Análisis completo"
        }
    }

@app.post("/analyze/lexico", response_model=AnalysisResponse)
async def analyze_lexico(input_data: CodeInput):
    """Ejecuta análisis léxico del código Rust"""
    try:
        lexer = Lexer(input_data.code)
        tokens = lexer.tokenize()

        token_list = []
        error_list = []
        log_content = f"=== ANÁLISIS LÉXICO ===\n"
        log_content += f"Desarrollador: {input_data.developer}\n"
        log_content += f"Fecha: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n\n"
        log_content += f"CÓDIGO:\n{input_data.code}\n\n"
        log_content += "TOKENS:\n"

        for tok in tokens:
            token_list.append(TokenOutput(
                type=tok.type,
                value=str(tok.lexeme),
                line=tok.line
            ))
            log_content += f"  {tok.type:20} | {tok.lexeme:30} | Línea {tok.line}\n"

            # Detectar tokens de error
            if tok.type == 'ERROR':
                error_list.append(ErrorOutput(
                    type="Error Léxico",
                    message=str(tok.literal) if tok.literal else f"Token no reconocido: '{tok.lexeme}'",
                    line=tok.line
                ))

        if error_list:
            log_content += f"\nERRORES ENCONTRADOS: {len(error_list)}\n"
            for err in error_list:
                log_content += f"  Línea {err.line}: {err.message}\n"
        else:
            log_content += "\n✓ Análisis léxico completado sin errores\n"

        # Guardar log
        log_filename = generate_log_filename("lexico", input_data.developer)
        save_log(log_filename, log_content)

        return AnalysisResponse(
            status="success" if not error_list else "error",
            tokens=token_list,
            errors=error_list,
            log_file=os.path.basename(log_filename)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/sintactico", response_model=AnalysisResponse)
async def analyze_sintactico(input_data: CodeInput):
    """Ejecuta análisis sintáctico del código Rust"""
    try:
        # Primero hacer análisis léxico
        lexer = RustLexer()
        tokens = list(lexer.tokenize(input_data.code))

        # TODO: Implementar parser
        # parser = RustParser()
        # ast = parser.parse(input_data.code)

        log_content = f"=== ANÁLISIS SINTÁCTICO ===\n"
        log_content += f"Desarrollador: {input_data.developer}\n"
        log_content += f"Fecha: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n\n"
        log_content += "⚠ Parser en desarrollo\n"

        log_filename = generate_log_filename("sintactico", input_data.developer)
        save_log(log_filename, log_content)

        return AnalysisResponse(
            status="pending",
            tokens=[TokenOutput(type=t.type, value=str(t.value), line=t.lineno) for t in tokens],
            errors=[ErrorOutput(type="Info", message="Análisis sintáctico en desarrollo")],
            ast={"message": "En desarrollo"},
            log_file=os.path.basename(log_filename)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/semantico", response_model=AnalysisResponse)
async def analyze_semantico(input_data: CodeInput):
    """Ejecuta análisis semántico del código Rust"""
    try:
        log_content = f"=== ANÁLISIS SEMÁNTICO ===\n"
        log_content += f"Desarrollador: {input_data.developer}\n"
        log_content += f"Fecha: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n\n"
        log_content += "⚠ Análisis semántico en desarrollo\n"

        log_filename = generate_log_filename("semantico", input_data.developer)
        save_log(log_filename, log_content)

        return AnalysisResponse(
            status="pending",
            errors=[ErrorOutput(type="Info", message="Análisis semántico en desarrollo")],
            log_file=os.path.basename(log_filename)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/completo", response_model=AnalysisResponse)
async def analyze_completo(input_data: CodeInput):
    """Ejecuta análisis completo (léxico + sintáctico + semántico)"""
    try:
        # Por ahora solo ejecutar análisis léxico
        result = await analyze_lexico(input_data)
        result.log_file = result.log_file.replace("lexico", "completo")
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)