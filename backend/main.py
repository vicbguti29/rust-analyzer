from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import os
import sys

# Agregar el directorio analyzer al path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from analyzer.ply_lexer import tokenize_source
from analyzer.ply_parser_final import parse_source, log_syntax_errors
from analyzer.semantic_analyzer import semantic, log_semantic_errors

app = FastAPI(
    title="Analizador Léxico, Sintáctico y Semántico - Rust",
    description="API para análisis de código Rust usando PLY",
    version="1.0.0",
)

# Configurar CORS
allowed_origins = [
    "http://localhost:3000",  # Desarrollo local
    "http://localhost:8080",  # Desarrollo alternativo
    "https://proj-01-eight.vercel.app",  # Producción Vercel,
    "https://rust-analyzer-api.onrender.com",  # Producción Render
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# Modelos de datos
class CodeInput(BaseModel):
    code: str
    developer: str = (
        "Alvasconv"  # MODIFICAR PARA QUE SE REGISTREN QUIEN REALIZO LAS PRUEBAS
    )


class TokenOutput(BaseModel):
    type: str
    value: str
    line: int


class ErrorOutput(BaseModel):
    type: str
    message: str
    line: Optional[int] = None


class AnalysisResponse(BaseModel):
    status: str
    tokens: list[TokenOutput] = []
    errors: list[ErrorOutput] = []
    ast: Optional[str] = None
    log_file: Optional[str] = None


# Directorio de logs
LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)


def generate_log_filename(analysis_type: str, developer: str) -> str:
    """Genera nombre de archivo de log según el formato especificado"""
    timestamp = datetime.now().strftime("%d-%m-%Y-%H:%M")
    filename = f"{analysis_type}-{developer}-{timestamp}.txt"
    return os.path.join(LOGS_DIR, filename)


def save_log(filename: str, content: str):
    """Guarda el contenido del análisis en un archivo de log"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


@app.get("/")
async def root():
    return {
        "message": "API del Analizador Léxico, Sintáctico y Semántico para Rust",
        "endpoints": {
            "/analyze/lexico": "POST - Análisis léxico",
            "/analyze/sintactico": "POST - Análisis sintáctico",
            "/analyze/semantico": "POST - Análisis semántico",
            "/analyze/completo": "POST - Análisis completo",
        },
    }


@app.post("/analyze/lexico", response_model=AnalysisResponse)
async def analyze_lexico(input_data: CodeInput):
    """Ejecuta análisis léxico del código Rust"""
    try:
        # Usar el nuevo lexer basado en PLY
        tokens = tokenize_source(input_data.code)

        token_list = []
        error_list = []
        log_content = f"=== ANÁLISIS LÉXICO (PLY) ===\n"
        log_content += f"Desarrollador: {input_data.developer}\n"
        log_content += f"Fecha: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n\n"
        log_content += f"CÓDIGO:\n{input_data.code}\n\n"
        log_content += "TOKENS:\n"

        for tok in tokens:
            token_list.append(
                TokenOutput(type=tok["type"], value=str(tok["value"]), line=tok["line"])
            )
            log_content += (
                f"  {tok['type']:20} | {tok['value']:30} | Línea {tok['line']}\n"
            )

            # El nuevo lexer no genera tokens de ERROR, pero se mantiene la lógica por si se añade en el futuro
            if tok["type"] == "ERROR":
                error_list.append(
                    ErrorOutput(
                        type="Error Léxico",
                        message=str(tok.get("literal", tok["value"])),
                        line=tok["line"],
                    )
                )

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
            log_file=os.path.basename(log_filename),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/sintactico", response_model=AnalysisResponse)
async def analyze_sintactico(input_data: CodeInput):
    """Ejecuta análisis sintáctico del código Rust"""
    try:
        tokens = tokenize_source(input_data.code)
        ast, syntax_errors = parse_source(input_data.code)

        token_list = [
            TokenOutput(type=t["type"], value=str(t["value"]), line=t["line"])
            for t in tokens
        ]
        error_list = [
            ErrorOutput(
                type="Error Sintáctico", message=err["message"], line=err["line"]
            )
            for err in syntax_errors
        ]

        # Guardar log
        log_filename = generate_log_filename("sintactico", input_data.developer)
        log_syntax_errors(log_filename, syntax_errors, input_data.code)

        return AnalysisResponse(
            status="success" if not error_list else "error",
            tokens=token_list,
            errors=error_list,
            ast=str(ast) if ast else None,
            log_file=os.path.basename(log_filename),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/semantico", response_model=AnalysisResponse)
async def analyze_semantico(input_data: CodeInput):
    """Ejecuta análisis semántico del código Rust"""
    try:
        # Primero hacer análisis sintáctico para obtener el AST
        ast, syntax_errors = parse_source(input_data.code)

        if syntax_errors or not ast:
            error_list = [
                ErrorOutput(
                    type="Error Sintáctico",
                    message=err.get("message", str(err)),
                    line=err.get("line") if isinstance(err.get("line"), int) else None,
                )
                for err in syntax_errors
            ]
            return AnalysisResponse(status="error", errors=error_list, log_file=None)

        # Luego hacer análisis semántico
        try:
            semantic_errors = semantic(ast) if ast else []
        except Exception as sem_error:
            semantic_errors = [f"Error en análisis semántico: {str(sem_error)}"]

        error_list = [
            ErrorOutput(type="Error Semántico", message=err, line=None)
            for err in semantic_errors
        ]

        # Guardar log
        log_filename = generate_log_filename("semantico", input_data.developer)
        try:
            log_semantic_errors(
                log_filename, semantic_errors, input_data.code, input_data.developer
            )
        except Exception as log_error:
            print(f"Error guardando log: {str(log_error)}")

        return AnalysisResponse(
            status="success" if not error_list else "error",
            errors=error_list,
            log_file=os.path.basename(log_filename),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/completo", response_model=AnalysisResponse)
async def analyze_completo(input_data: CodeInput):
    """Ejecuta análisis completo (léxico + sintáctico + semántico)"""
    try:
        # 1. Análisis léxico
        tokens = tokenize_source(input_data.code)
        token_list = [
            TokenOutput(type=t["type"], value=str(t["value"]), line=t["line"])
            for t in tokens
        ]

        # 2. Análisis sintáctico
        ast, syntax_errors = parse_source(input_data.code)

        if syntax_errors or not ast:
            error_list = [
                ErrorOutput(
                    type="Error Sintáctico",
                    message=err.get("message", str(err)),
                    line=err.get("line") if isinstance(err.get("line"), int) else None,
                )
                for err in syntax_errors
            ]
            return AnalysisResponse(
                status="error", tokens=token_list, errors=error_list, log_file=None
            )

        # 3. Análisis semántico
        try:
            semantic_errors = semantic(ast) if ast else []
        except Exception as sem_error:
            semantic_errors = [f"Error en análisis semántico: {str(sem_error)}"]

        error_list = [
            ErrorOutput(type="Error Semántico", message=err, line=None)
            for err in semantic_errors
        ]

        # Guardar log
        log_filename = generate_log_filename("completo", input_data.developer)
        try:
            log_semantic_errors(
                log_filename, semantic_errors, input_data.code, input_data.developer
            )
        except Exception as log_error:
            print(f"Error guardando log: {str(log_error)}")

        return AnalysisResponse(
            status="success" if not error_list else "error",
            tokens=token_list,
            errors=error_list,
            ast=str(ast) if ast else None,
            log_file=os.path.basename(log_filename),
        )

    except Exception as e:
        print(f"ERROR en /analyze/completo: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
