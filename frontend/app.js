// API Base URL - cambiar según el entorno
const API_BASE_URL = 'http://localhost:8000';

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
    lineNumbers.scrollTop = codeEditor.scrollTop;
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
            errorDiv.className = 'error-item';
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
    alert('Menú Archivo: Funcionalidad en desarrollo');
});

document.getElementById('menuAnalisis').addEventListener('click', () => {
    alert('Menú Análisis: Funcionalidad en desarrollo');
});

document.getElementById('menuAyuda').addEventListener('click', () => {
    alert('Analizador Léxico, Sintáctico y Semántico para Rust\nDesarrollado con FastAPI + PLY');
});

// Inicializar
updateLineNumbers();
updateStatus('Listo');
