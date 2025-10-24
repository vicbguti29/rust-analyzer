**Implementación de un Analizador Léxico, Sintáctico y Semántico en \[LP\]**

Reemplace el título por su tema de proyecto y LP

Esta plantilla proporciona una estructura completa para escribir una propuesta detallada sobre la implementación de su analizador léxico, sintáctico y semántico, asegurando que se cubran todos los aspectos esenciales del proyecto.

Debe borrar todos los textos resaltados de amarillo. Lo que esté como avance 1, 2, 3 será entregado progresivamente, el informe final igual, no es necesario en esta propuesta ya que no dispone de esta información.

**1\. Introducción**

- Debe redactar una introducción de 3-4 párrafos que incluyan los siguientes temas
  - Describa el lenguaje de programación asignado (dart, ruby, php, go, c#, lua, kotlin, etc) y sus características en diseño de sintaxis, curva de aprendizaje, comunidad y tipos de aplicaciones. Utilice la documentación oficial del LP.
  - Describa la herramienta PLY (Lex y Yacc). Utilice la documentación oficial.
- Debe leerse como una introducción de proyecto. **No enliste cada párrafo**.

**2\. Objetivos del Proyecto**

- Lista detallada de las funcionalidades de su proyecto, utilizando el formato \[Verbo\] + \[Objeto\] + \[Condición\] (Ejemplo: "El sistema permitirá a un usuario crear una denuncia adjuntando evidencia fotográfica").
- Un objetivo general y 3 objetivos específicos serían suficientes.

**3\. Analizador Léxico**

**Descripción General**

- Describir las funcionalidades de su analizador léxico. Como requerimiento mínimo debe devolver los tokens válidos y de error, mensajes personalizados de errores encontrados.

**Componentes Principales**

Para este apartado pueden usar diferentes tablas para establecer un orden adecuado de la información.

- **Variables**: Cómo se escribe el nombre de las variables (patrón). Si en su LP existen otras variables, colocar todas las posibilidades.
- **Tipos de datos**: Tipos primitivos que se soportan (enteros, flotantes, cadenas, booleanos, etc.), estructurados (elegir al menos 1 estructura de datos por cada integrante).
- **Operadores**: Listado de operadores aritméticos, lógicos, de asignación, conectores lógicos, y su significado.
- **Palabras Reservadas**: Listado de palabras reservadas del lenguaje (if, else, while, for, etc.) y su significado.
- **Comentarios**: Especificar cómo se escriben los comentarios de una línea y múltiples líneas.
- **Delimitadores**: Símbolos usados para delimitar bloques de código (puntos y comas, llaves, paréntesis, identación, etc).

**4\. Analizador Sintáctico**

**Descripción General**

- Describir las funcionalidades de su analizador sintáctico. Agregar una breve evaluación de la sintaxis de su lenguaje de programación (simplicidad, tipado, diseño de sintaxis, ortogonalidad). El requerimiento mínimo es indicar un mensaje personalizado del error de sintaxis.

**Reglas Gramaticales**

Debe colocar ejemplos de sintaxis para cada una de las reglas:

- **Declaración de Variables:** Reglas que especifiquen las diferentes formas de definir variables (asignar valor). (Cada integrante debe elegir al menos 1 forma).
- **Expresiones Aritméticas**: Reglas para suma, resta, multiplicación, división y otras operaciones aritméticas, indicar la precedencia.
- **Expresiones Booleanas**: Reglas para comparar, conectar dos o más condiciones.
- **Estructuras de Control**: Reglas para if, else, while, for, switch, etc. (Cada integrante debe elegir una estructura de control)
- **Estructuras de Datos (ED)**: Reglas para definir: arreglos, listas, tuplas, diccionarios, conjuntos, etc.; en caso de que su LP asignado no posea muchas ED podrá definir clases para nuevas ED. (Cada integrante debe definir al menos una estructura de control)
- **Declaraciones de Funciones**: Regla para la declaración y llamada de funciones. Existen funciones con retorno, lambda, n argumentos, parámetros opcionales, etc. (Cada integrante debe definir al menos 1 tipo de función)
- **Impresión y solicitud de datos:** Regla para imprimir: cadenas, valores, variables, etc. Regla para solicitar datos por teclado.

**IMPORTANTE**: No olvide colocar ejemplos de sintaxis, sin fondos oscuros y que sea legible. Intente no usar imágenes sino escribirlas en el documento usando la fuente **Montserrat**. Así:

print("Hola Mundo")

**5\. Analizador Semántico**

**Descripción General**

- Describir las funcionalidades del analizador. Solo deberán agregar las reglas semánticas que evaluará su analizador semántico. El requerimiento mínimo es indicar el mensaje de error semántico según la categoría o tipo.
- Herramientas de desarrollo y test, crear una tabla con el nombre y la descripción de la herramienta.
- Recursos humanos (desarrolladores). Definir en este apartado qué integrante desarrollaría las reglas léxicas, sintácticas y semánticas. Puede ser una tabla de asignaciones de reglas, debe ser equitativa. Agregar una columna con su usuario de github para poder identificarlos en cada avance.

**7\. Diseño Preliminar**

**Funcionalidades a Implementar**

El MVP del analizador léxico, sintáctico y semántico de Rust incluirá las siguientes funcionalidades principales:

- **Editor de código integrado**: Área de texto donde el usuario puede escribir o pegar código Rust para analizar.
- **Selector de tipo de análisis**: Opciones para ejecutar análisis léxico, sintáctico o semántico de forma individual o completa.
- **Panel de tokens**: Visualización de todos los tokens identificados por el analizador léxico, mostrando tipo de token y valor.
- **Panel de errores**: Visualización detallada de errores encontrados durante el análisis, con mensajes personalizados que indiquen la línea, tipo de error y descripción.
- **Generación automática de logs**: El sistema generará archivos de log automáticamente con el formato [tipo_analisis]-[desarrollador]-[fecha]-[hora].txt en cada ejecución.
- **Botones de acción**: Opciones para cargar archivos .rs, limpiar el editor, ejecutar análisis y exportar resultados.
- **Indicadores visuales**: Código de colores para identificar rápidamente tokens válidos (verde), errores léxicos (rojo), errores sintácticos (naranja) y errores semánticos (morado).

**Prototipo Visual**

El diseño de la interfaz gráfica sigue un layout de dos columnas para optimizar el espacio y facilitar la visualización simultánea del código y los resultados:

**Estructura del Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│  Analizador Léxico, Sintáctico y Semántico - Rust          │
│  [Archivo] [Análisis] [Ayuda]                               │
├──────────────────────────┬──────────────────────────────────┤
│  Editor de Código        │  Panel de Resultados             │
│                          │  ┌────────────────────────────┐  │
│  1  fn main() {          │  │ [Tokens] [Errores] [AST]  │  │
│  2      let x = 5;       │  └────────────────────────────┘  │
│  3      println!("{}", x)│                                  │
│  4  }                    │  Tokens encontrados:             │
│                          │  ┌────────────────────────────┐  │
│  [Cargar .rs] [Limpiar] │  │ FN | fn                    │  │
│                          │  │ IDENTIFIER | main          │  │
│  [▶ Análisis Léxico]    │  │ LPAREN | (                 │  │
│  [▶ Análisis Sintáctico]│  │ ...                        │  │
│  [▶ Análisis Semántico] │  └────────────────────────────┘  │
│  [▶ Análisis Completo]  │                                  │
│                          │  Estado: ✓ Análisis completado   │
└──────────────────────────┴──────────────────────────────────┘
```

**Descripción de componentes:**

- **Barra superior**: Contiene el título de la aplicación y menú con opciones básicas.
- **Panel izquierdo (50%)**: Editor de código con numeración de líneas, syntax highlighting básico y botones de acción.
- **Panel derecho (50%)**: Área tabulada que alterna entre vista de tokens, errores y árbol sintáctico abstracto (AST).
- **Barra de estado inferior**: Muestra el estado actual del análisis y logs generados.

**Paleta de colores:**
- Fondo editor: #2E3440 (oscuro)
- Texto código: #D8DEE9 (claro)
- Tokens válidos: #A3BE8C (verde)
- Errores: #BF616A (rojo)
- Advertencias: #EBCB8B (amarillo)
- Panel resultados: #ECEFF4 (claro)

**Tecnologías para la GUI:**
- Frontend: HTML5, CSS3, JavaScript (interfaz web)
- Backend: FastAPI + Python para API REST
- Análisis: PLY (Python Lex-Yacc)
- Deploy: Railway/Render (backend), Vercel/Netlify (frontend)

**Nota:** Para detalles completos de la arquitectura del proyecto, estructura de archivos y propósito de cada módulo, consultar docs/arquitectura.md

**8\. Pruebas y Validación (En cada avance)**

**Casos de Prueba**

- Cada integrante deberá crear un algoritmo en su LP asignado con la mayoría de tokens. Estos algoritmos se utilizarán como entrada para su fase de test. Puede generarlos con IA Generativa.
- Su analizador deberá generar logs del análisis realizado (**Avance 1, 2 y 3**), por cada prueba deberá generarse un log que incluya el nombre del análisis - desarrollador - fecha-hora. Por ejemplo lexico-rodrigosaraguro-03-07-2025-17:30.txt o semantico-luisperez-10-11-2025-14:23.txt. Estos logs solo se deberán actualizar en su repositorio de proyecto.

**Resultados**

Cada semana se irán subiendo en esta sección los Avances 1, 2, 3 y deberá agregar capturas de las pruebas realizadas en su interfaz gráfica.

Recuerde que cada integrante deberá probar su propio algoritmo y presentar al menos una captura con error léxico, sintáctico o semántico, según el avance actual.

**9\. Conclusiones y Recomendaciones (al final del proyecto)**

**Resumen**

- Las conclusiones deben tener 3 enfoques: una conclusión hacia el lenguaje asignado, otra conclusión hacia la experiencia de desarrollar los analizadores, una conclusión hacia la herramienta PLY utilizada.

**Recomendaciones y trabajos futuros**

- Cada integrante deberá responder las siguientes preguntas:
  - ¿Cómo evaluaría su solución actual según las funcionalidades desarrolladas y la arquitectura?
  - ¿Cómo podría mejorar su proyecto? Nuevas funcionalidades, correcciones.
- De preferencia crear una tabla con el nombre del integrante y sus respuestas. Por cada respuesta de integrante pueden usar una fila.
- Este apartado no influirá en su calificación de proyecto, es para utilizarlo en una medición para ABET.

**10\. Referencias**

- Documentos, libros y recursos en línea consultados para la propuesta.
- Formato IEEE o APA. **No olvide colocar citas dentro del documento**.
