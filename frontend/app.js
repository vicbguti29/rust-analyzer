// API Base URL - cambiar según el entorno
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://rust-analyzer-api.onrender.com'; 

// Modo demo con datos mock
const DEMO_MODE = false; // Cambiar a false cuando el backend esté disponible

// Datos mock para demostración
const MOCK_DATA = {
    lexico: {
        status: 'success',
        tokens: [
            { type: 'FN', value: 'fn', line: 1 },
            { type: 'IDENTIFIER', value: 'main', line: 1 },
            { type: 'LPAREN', value: '(', line: 1 },
            { type: 'RPAREN', value: ')', line: 1 },
            { type: 'LBRACE', value: '{', line: 1 },
            { type: 'LET', value: 'let', line: 2 },
            { type: 'IDENTIFIER', value: 'x', line: 2 },
            { type: 'ASSIGN', value: '=', line: 2 },
            { type: 'NUMBER', value: '5', line: 2 },
            { type: 'SEMICOLON', value: ';', line: 2 },
            { type: 'IDENTIFIER', value: 'println', line: 3 },
            { type: 'MACRO', value: '!', line: 3 },
            { type: 'LPAREN', value: '(', line: 3 },
            { type: 'STRING', value: '"Hola, mundo!"', line: 3 },
            { type: 'RPAREN', value: ')', line: 3 },
            { type: 'SEMICOLON', value: ';', line: 3 },
            { type: 'RBRACE', value: '}', line: 4 }
        ],
        errors: [],
        log_file: 'lexico-demo-24-10-2025-15:30.txt'
    },
    sintactico: {
        status: 'success',
        tokens: [
            { type: 'FN', value: 'fn', line: 1 },
            { type: 'IDENTIFIER', value: 'main', line: 1 }
        ],
        errors: [],
        ast: {
            type: 'Program',
            body: [
                {
                    type: 'FunctionDeclaration',
                    name: 'main',
                    params: [],
                    body: {
                        type: 'BlockStatement',
                        statements: [
                            {
                                type: 'VariableDeclaration',
                                name: 'x',
                                value: 5
                            },
                            {
                                type: 'MacroCall',
                                name: 'println',
                                args: ['"Hola, mundo!"']
                            }
                        ]
                    }
                }
            ]
        },
        log_file: 'sintactico-demo-24-10-2025-15:31.txt'
    },
    semantico: {
        status: 'success',
        tokens: [],
        errors: [],
        ast: null,
        log_file: 'semantico-demo-24-10-2025-15:32.txt'
    },
    completo: {
        status: 'success',
        tokens: [
            { type: 'FN', value: 'fn', line: 1 },
            { type: 'IDENTIFIER', value: 'main', line: 1 },
            { type: 'LPAREN', value: '(', line: 1 },
            { type: 'RPAREN', value: ')', line: 1 }
        ],
        errors: [],
        ast: {
            type: 'Program',
            body: []
        },
        log_file: 'completo-demo-24-10-2025-15:33.txt'
    },
    error_example: {
        status: 'error',
        tokens: [
            { type: 'FN', value: 'fn', line: 1 },
            { type: 'ERROR', value: '@', line: 2 }
        ],
        errors: [
            {
                type: 'Error Léxico',
                category: 'lexico',
                message: 'Token no reconocido: \'@\'',
                line: 2
            },
            {
                type: 'Error Sintáctico',
                category: 'sintactico',
                message: 'Se esperaba punto y coma al final de la declaración',
                line: 3
            },
            {
                type: 'Error Semántico',
                category: 'semantico',
                message: 'Variable \'y\' no declarada antes de su uso',
                line: 4
            }
        ],
        log_file: 'error-demo-24-10-2025-15:34.txt'
    }
};

// Elementos del DOM
const codeEditor = document.getElementById('codeEditor');
const lineNumbers = document.getElementById('lineNumbers');
const fileInput = document.getElementById('fileInput');
const status = document.getElementById('status');
const logInfo = document.getElementById('logInfo');

// Botones
const btnCargar = document.getElementById('btnCargar');
const btnLimpiar = document.getElementById('btnLimpiar');
const btnLexico = document.getElementById('btnLexico');
const btnSintactico = document.getElementById('btnSintactico');
const btnSemantico = document.getElementById('btnSemantico');
const btnCompleto = document.getElementById('btnCompleto');

// Tabs
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');

// Resultados
const tokensList = document.getElementById('tokensList');
const errorsList = document.getElementById('errorsList');
const astView = document.getElementById('astView');

// ========== GESTIÓN DE TABS ==========
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.getAttribute('data-tab');

        // Desactivar todas las tabs
        tabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(tc => tc.classList.remove('active'));

        // Activar tab seleccionada
        tab.classList.add('active');
        document.getElementById(`${tabName}Tab`).classList.add('active');
    });
});

// ========== EDITOR DE CÓDIGO ==========
// Actualizar números de línea
function updateLineNumbers() {
    const lines = codeEditor.value.split('\n').length;
    lineNumbers.innerHTML = Array.from({ length: lines }, (_, i) => i + 1).join('\n');
}

codeEditor.addEventListener('input', updateLineNumbers);
codeEditor.addEventListener('scroll', () => {
    lineNumbers.style.transform = `translateY(-${codeEditor.scrollTop}px)`;
});

// ========== MANEJO DE ARCHIVOS ==========
btnCargar.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            codeEditor.value = event.target.result;
            updateLineNumbers();
            updateStatus('Archivo cargado: ' + file.name, 'success');
        };
        reader.readAsText(file);
    }
});

btnLimpiar.addEventListener('click', () => {
    codeEditor.value = '';
    updateLineNumbers();
    clearResults();
    updateStatus('Editor limpio', 'success');
});

// ========== ANÁLISIS ==========
async function executeAnalysis(type) {
    const code = codeEditor.value.trim();

    if (!code) {
        updateStatus('Error: El editor está vacío', 'error');
        return;
    }

    updateStatus(`Ejecutando análisis ${type}...`, 'loading');

    // Si está en modo demo (y no es 'lexico'), usar datos mock
    if (DEMO_MODE && type !== 'lexico') {
        await simulateDelay(800); // Simular tiempo de procesamiento
        const data = MOCK_DATA[type];
        displayResults(data, type);
        updateStatus(`✓ Análisis ${type} completado (MODO DEMO)`, 'success');
        updateLogInfo(data.log_file);
        return;
    }

    // Modo producción: llamar al backend real
    try {
        const response = await fetch(`${API_BASE_URL}/analyze/${type}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayResults(data, type);
        updateStatus(`✓ Análisis ${type} completado`, 'success');
        updateLogInfo(data.log_file);

    } catch (error) {
        console.error('Error:', error);
        updateStatus(`Error al ejecutar análisis: ${error.message}`, 'error');
        displayError(error.message);
    }
}

// Simular delay para modo demo
function simulateDelay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

btnLexico.addEventListener('click', () => executeAnalysis('lexico'));
btnSintactico.addEventListener('click', () => executeAnalysis('sintactico'));
btnSemantico.addEventListener('click', () => executeAnalysis('semantico'));
btnCompleto.addEventListener('click', () => executeAnalysis('completo'));

// ========== VISUALIZACIÓN DE RESULTADOS ==========
function displayResults(data, type) {
    clearResults();

    // Mostrar tokens
    if (data.tokens && data.tokens.length > 0) {
        tokensList.innerHTML = '';
        data.tokens.forEach(token => {
            const tokenDiv = document.createElement('div');
            tokenDiv.className = 'token-item';
            tokenDiv.innerHTML = `<strong>${token.type}</strong> | ${token.value}`;
            if (token.line) {
                tokenDiv.innerHTML += ` <span style="color: #666; font-size: 0.9rem;">(Línea ${token.line})</span>`;
            }
            tokensList.appendChild(tokenDiv);
        });
    }

    // Mostrar errores
    if (data.errors && data.errors.length > 0) {
        errorsList.innerHTML = '';
        data.errors.forEach(error => {
            const errorDiv = document.createElement('div');
            // Aplicar clase según categoría de error
            const category = error.category || 'lexico';
            errorDiv.className = `error-item error-${category}`;
            errorDiv.innerHTML = `
                <div class="error-type">${error.type || 'Error'}</div>
                <div class="error-line">Línea ${error.line || 'N/A'}: ${error.message}</div>
            `;
            errorsList.appendChild(errorDiv);
        });

        // Cambiar a tab de errores si hay errores
        document.querySelector('[data-tab="errors"]').click();
    } else {
        errorsList.innerHTML = '<p class="placeholder">No hay errores detectados</p>';
    }

    // Mostrar AST
    if (data.ast) {
        astView.innerHTML = `<pre style="background: #f8f9fa; padding: 1rem; border-radius: 4px; overflow-x: auto;">${JSON.stringify(data.ast, null, 2)}</pre>`;
    }
}

function displayError(message) {
    errorsList.innerHTML = `
        <div class="error-item">
            <div class="error-type">Error de Conexión</div>
            <div class="error-line">${message}</div>
        </div>
    `;
    document.querySelector('[data-tab="errors"]').click();
}

function clearResults() {
    tokensList.innerHTML = '<p class="placeholder">Ejecute un análisis léxico para ver los tokens</p>';
    errorsList.innerHTML = '<p class="placeholder">No hay errores detectados</p>';
    astView.innerHTML = '<p class="placeholder">Ejecute un análisis sintáctico para ver el AST</p>';
}

// ========== UTILIDADES ==========
function updateStatus(message, type = '') {
    status.textContent = 'Estado: ' + message;
    status.className = type;

    if (type === 'loading') {
        status.classList.add('loading');
    }
}

function updateLogInfo(logFile) {
    if (logFile) {
        logInfo.textContent = `Logs: ${logFile}`;
    }
}

// ========== MENÚ ==========
document.getElementById('menuArchivo').addEventListener('click', () => {
    const option = prompt(
        'Menú Archivo:\n' +
        '1 - Cargar ejemplo básico\n' +
        '2 - Cargar ejemplo con errores\n' +
        '3 - Limpiar editor\n\n' +
        'Ingrese opción:'
    );

    if (option === '1') {
        codeEditor.value = `fn main() {
    let x = 5;
    println!("Hola, mundo!");
}`;
        updateLineNumbers();
        updateStatus('Ejemplo básico cargado', 'success');
    } else if (option === '2') {
        codeEditor.value = `fn main() {
    let x = 5
    let @ = invalid;
    println!("{}", y);
}`;
        updateLineNumbers();
        updateStatus('Ejemplo con errores cargado - Ejecuta análisis para verlos', 'success');

        // Automáticamente mostrar los errores de ejemplo
        setTimeout(() => {
            displayResults(MOCK_DATA.error_example, 'completo');
        }, 500);
    } else if (option === '3') {
        codeEditor.value = '';
        updateLineNumbers();
        clearResults();
        updateStatus('Editor limpio', 'success');
    }
});

document.getElementById('menuAnalisis').addEventListener('click', () => {
    alert(
        '🎨 Indicadores Visuales:\n\n' +
        '🔴 Rojo - Errores Léxicos\n' +
        '🟡 Amarillo - Errores Sintácticos\n' +
        '🟣 Morado - Errores Semánticos\n' +
        '🟢 Verde - Tokens válidos\n\n' +
        'Usa "Archivo > Cargar ejemplo con errores" para ver los indicadores en acción'
    );
});

document.getElementById('menuAyuda').addEventListener('click', () => {
    alert(
        'Analizador Léxico, Sintáctico y Semántico para Rust\n' +
        'Desarrollado con FastAPI + PLY\n\n' +
        '📌 MODO DEMO ACTIVO\n' +
        'Los resultados son simulados con datos mock\n\n' +
        '💡 Prueba "Archivo > Cargar ejemplo con errores"\n' +
        'para ver los indicadores visuales de colores'
    );
});

// Inicializar
updateLineNumbers();

// Cargar código de ejemplo en modo demo
if (DEMO_MODE) {
    codeEditor.value = `fn main() {
    let x = 5;
    println!("Hola, mundo!");
}`;
    updateLineNumbers();
    updateStatus('Listo - MODO DEMO (Datos de ejemplo)', 'success');
} else {
    updateStatus('Listo');
}
