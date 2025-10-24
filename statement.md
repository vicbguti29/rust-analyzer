**Implementación de un Analizador Léxico, Sintáctico y Semántico en \[LP\]**

Reemplace el título por su tema de proyecto y LP

Esta plantilla proporciona una estructura completa para escribir una propuesta detallada sobre la implementación de su analizador léxico, sintáctico y semántico, asegurando que se cubran todos los aspectos esenciales del proyecto.

Debe borrar todos los textos resaltados de amarillo. Lo que esté como avance 1, 2, 3 será entregado progresivamente, el informe final igual, no es necesario en esta propuesta ya que no dispone de esta información.

**1\. Introducción**

Rust es un lenguaje de programación de sistemas moderno que enfatiza la seguridad de memoria, el rendimiento y la concurrencia sin comprometer la velocidad de ejecución. Desarrollado originalmente por Mozilla Research y actualmente mantenido por la Rust Foundation, este lenguaje ha experimentado un crecimiento exponencial en su adopción, siendo el primer lenguaje además de C y ensamblador en ser soportado oficialmente en el desarrollo del kernel de Linux. Su diseño sintáctico combina elementos de programación funcional, como inmutabilidad por defecto, funciones de orden superior y pattern matching, con características de programación orientada a objetos mediante structs, enums, traits y métodos. Rust cuenta con características modernas como inferencia de tipos, abstracciones de costo cero, un poderoso sistema de macros y un gestor de paquetes integrado llamado Cargo, lo que lo convierte en una opción atractiva para el desarrollo de aplicaciones que requieren alto rendimiento y confiabilidad.

La curva de aprendizaje de Rust es notablemente pronunciada, especialmente durante los primeros dos meses, donde los desarrolladores deben familiarizarse con conceptos únicos como el sistema de ownership, borrowing y lifetimes. Según estudios recientes, se requieren entre 3 a 6 meses para alcanzar productividad desde un background de programación de sistemas, y de 6 a 12 meses para desarrolladores provenientes de lenguajes de alto nivel. Sin embargo, la comunidad de Rust es reconocida por su excelente documentación oficial, tutoriales detallados y un ecosistema robusto con más de 80,000 crates disponibles en crates.io. En 2025, la adopción de Rust ha penetrado ecosistemas empresariales importantes, con Microsoft, Google y AWS contribuyendo activamente al lenguaje e integrándolo en sus productos, especialmente en componentes de sistemas operativos, navegadores web y aplicaciones cloud-native.

Las aplicaciones de Rust abarcan un amplio espectro tecnológico, destacándose en programación de sistemas, desarrollo web mediante frameworks como Actix Web, Rocket y Warp, infraestructura blockchain, dispositivos IoT, desarrollo de videojuegos, y computación científica. Su capacidad para compilar a WebAssembly (Wasm) ha abierto nuevas posibilidades para construir aplicaciones que se ejecutan nativamente en navegadores con rendimiento cercano a C. Actualmente, el 29.2% de los desarrolladores que no trabajan con Rust expresan interés en adoptarlo, y aproximadamente 709,000 desarrolladores lo consideran su lenguaje principal según encuestas de JetBrains en 2024.

Para el desarrollo de este proyecto de análisis léxico, sintáctico y semántico, se utilizará PLY (Python Lex-Yacc), una implementación 100% Python de las herramientas tradicionales lex y yacc utilizadas comúnmente para escribir analizadores y compiladores. PLY está basado en el mismo algoritmo de parsing LALR(1) utilizado por yacc y proporciona la mayoría de las características estándar incluyendo soporte para producciones vacías, reglas de precedencia, recuperación de errores y manejo de gramáticas ambiguas. Aunque PLY ya no recibe actualizaciones como paquete instalable vía pip, continúa siendo mantenido y modernizado, siendo compatible con todas las versiones modernas de Python sin requerir dependencias externas. Su documentación oficial está disponible en https://ply.readthedocs.io/ y el código fuente en GitHub, proporcionando una base sólida y bien documentada para implementar analizadores sintácticos de manera eficiente y educativa.

**2\. Objetivos del Proyecto**

**Objetivo General**

Desarrollar un analizador léxico, sintáctico y semántico completo para el lenguaje de programación Rust utilizando PLY (Python Lex-Yacc), integrando una interfaz web interactiva que permita a los usuarios analizar código fuente, visualizar tokens identificados, detectar errores de sintaxis y semántica, y generar logs detallados de cada análisis realizado.

**Objetivos Específicos**

1. Implementar un analizador léxico capaz de tokenizar código Rust identificando palabras reservadas, operadores, delimitadores, literales y tipos de datos, generando mensajes personalizados para tokens inválidos y registrando cada análisis en archivos de log con formato estandarizado.

2. Diseñar y construir un analizador sintáctico basado en gramáticas BNF que valide la estructura del código Rust, incluyendo declaraciones de variables, estructuras de control, funciones, expresiones aritméticas y booleanas, generando un árbol sintáctico abstracto (AST) y reportando errores de sintaxis con indicación precisa de línea y descripción del problema.

3. Desarrollar un analizador semántico que verifique reglas del lenguaje como tipos de datos, declaración previa de variables, alcance de variables (scope), mutabilidad, y retorno de funciones, proporcionando mensajes de error semántico categorizados y detallados.

4. Crear una interfaz web moderna y funcional con editor de código integrado, visualización diferenciada por colores de tokens y errores según su tipo (léxico, sintáctico, semántico), y capacidad de exportar resultados y logs de análisis para facilitar la depuración y el aprendizaje del lenguaje Rust.

**3\. Analizador Léxico**

**Descripción General**

El analizador léxico implementado con PLY será capaz de procesar código fuente escrito en Rust y descomponerlo en una secuencia de tokens válidos, identificando cada elemento sintáctico del lenguaje. Las funcionalidades principales incluyen: (1) reconocimiento de palabras reservadas, identificadores, literales numéricos y de cadena, operadores y delimitadores; (2) identificación y marcado de tokens inválidos o no reconocidos con mensajes personalizados que indiquen el tipo de error y la línea donde ocurre; (3) generación de una lista completa de tokens encontrados con información detallada incluyendo tipo, valor y posición en el código; (4) manejo de comentarios de una línea y multilínea ignorándolos durante el análisis; (5) generación automática de archivos de log con formato estandarizado que registren cada análisis realizado, incluyendo desarrollador, fecha, hora, código analizado y tokens identificados. El analizador proporcionará retroalimentación visual diferenciada por colores en la interfaz web, mostrando tokens válidos en verde y errores léxicos en rojo.

**Componentes Principales**

**Variables**

En Rust, los nombres de variables (identificadores) siguen el patrón: `[a-zA-Z_][a-zA-Z0-9_]*`, es decir, deben comenzar con una letra o guión bajo, seguido de letras, dígitos o guiones bajos. Rust utiliza convención snake_case para variables y funciones.

| Tipo de Variable | Sintaxis | Ejemplo |
|-----------------|----------|---------|
| Variable inmutable | `let nombre = valor;` | `let x = 5;` |
| Variable mutable | `let mut nombre = valor;` | `let mut count = 0;` |
| Constante | `const NOMBRE: tipo = valor;` | `const MAX_SIZE: u32 = 100;` |
| Variable estática | `static NOMBRE: tipo = valor;` | `static COUNTER: i32 = 0;` |

**Tipos de Datos**

| Categoría | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| **Primitivos** | | | |
| Enteros con signo | `i8`, `i16`, `i32`, `i64`, `i128` | Enteros con signo de diferentes tamaños | `let n: i32 = -42;` |
| Enteros sin signo | `u8`, `u16`, `u32`, `u64`, `u128` | Enteros positivos de diferentes tamaños | `let age: u8 = 25;` |
| Punto flotante | `f32`, `f64` | Números decimales | `let pi: f64 = 3.14159;` |
| Booleano | `bool` | Valores true o false | `let is_active: bool = true;` |
| Carácter | `char` | Un carácter Unicode | `let letra: char = 'A';` |
| Cadena | `str`, `String` | Cadenas de texto | `let msg: &str = "Hola";` |
| **Estructurados** | | | |
| Vector | `Vec<T>` | Lista dinámica de elementos del mismo tipo | `let nums: Vec<i32> = vec![1, 2, 3];` |
| Array | `[T; N]` | Lista de tamaño fijo | `let arr: [i32; 3] = [1, 2, 3];` |
| Tupla | `(T1, T2, ...)` | Colección de valores de diferentes tipos | `let tuple: (i32, f64) = (5, 3.14);` |
| HashMap | `HashMap<K, V>` | Estructura clave-valor | `let mut map = HashMap::new();` |

**Operadores**

| Categoría | Operador | Significado | Ejemplo |
|-----------|----------|-------------|---------|
| **Aritméticos** | | | |
| | `+` | Suma | `a + b` |
| | `-` | Resta | `a - b` |
| | `*` | Multiplicación | `a * b` |
| | `/` | División | `a / b` |
| | `%` | Módulo (residuo) | `a % b` |
| **Comparación** | | | |
| | `==` | Igual a | `a == b` |
| | `!=` | Diferente de | `a != b` |
| | `<` | Menor que | `a < b` |
| | `<=` | Menor o igual que | `a <= b` |
| | `>` | Mayor que | `a > b` |
| | `>=` | Mayor o igual que | `a >= b` |
| **Lógicos** | | | |
| | `&&` | AND lógico | `a && b` |
| | `||` | OR lógico | `a || b` |
| | `!` | NOT lógico | `!a` |
| **Asignación** | | | |
| | `=` | Asignación simple | `x = 5` |
| | `+=` | Suma y asigna | `x += 3` |
| | `-=` | Resta y asigna | `x -= 2` |
| | `*=` | Multiplica y asigna | `x *= 4` |
| | `/=` | Divide y asigna | `x /= 2` |
| **Otros** | | | |
| | `&` | Referencia | `&x` |
| | `*` | Dereferencia | `*ptr` |
| | `::` | Resolución de ruta | `std::io::stdin()` |
| | `->` | Tipo de retorno | `fn suma() -> i32` |
| | `=>` | Brazo de match | `Some(x) => x` |

**Palabras Reservadas**

| Palabra | Significado | Categoría |
|---------|-------------|-----------|
| `fn` | Declaración de función | Función |
| `let` | Declaración de variable inmutable | Variable |
| `mut` | Modificador de mutabilidad | Variable |
| `const` | Declaración de constante | Variable |
| `static` | Variable estática | Variable |
| `if` | Estructura condicional | Control |
| `else` | Alternativa de condicional | Control |
| `match` | Coincidencia de patrones | Control |
| `while` | Bucle condicional | Control |
| `for` | Bucle iterativo | Control |
| `loop` | Bucle infinito | Control |
| `break` | Salir de bucle | Control |
| `continue` | Siguiente iteración | Control |
| `return` | Retornar valor de función | Control |
| `struct` | Definir estructura | Tipo |
| `enum` | Definir enumeración | Tipo |
| `impl` | Implementar métodos | Tipo |
| `trait` | Definir rasgo (interfaz) | Tipo |
| `type` | Alias de tipo | Tipo |
| `pub` | Modificador de visibilidad pública | Modificador |
| `use` | Importar módulo/elemento | Módulo |
| `mod` | Declarar módulo | Módulo |
| `as` | Renombrar importación/casting | Operador |
| `in` | Pertenencia en iterador | Operador |
| `true` | Valor booleano verdadero | Literal |
| `false` | Valor booleano falso | Literal |

**Comentarios**

| Tipo | Sintaxis | Ejemplo |
|------|----------|---------|
| Comentario de línea | `// comentario` | `// Esto es un comentario` |
| Comentario multilínea | `/* comentario */` | `/* Comentario en<br>múltiples líneas */` |
| Comentario de documentación | `/// comentario` | `/// Documenta la función` |
| Comentario de doc multilínea | `/** comentario **/` | `/** Documentación<br>detallada **/` |

**Delimitadores**

| Símbolo | Nombre | Uso |
|---------|--------|-----|
| `;` | Punto y coma | Terminar declaraciones |
| `{ }` | Llaves | Delimitar bloques de código |
| `( )` | Paréntesis | Agrupar expresiones, parámetros de funciones |
| `[ ]` | Corchetes | Definir arrays, indexar colecciones |
| `,` | Coma | Separar elementos en listas |
| `.` | Punto | Acceder a campos/métodos |
| `:` | Dos puntos | Especificar tipos |
| `::` | Doble dos puntos | Acceder a elementos de módulos/tipos |

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
