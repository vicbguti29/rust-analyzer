# Implementación de un Analizador Léxico, Sintáctico y

# Semántico en Rust

## 1. Introducción

Rust es un lenguaje de programación utilizado por su alto rendimiento y seguridad de
memoria, además de ser usado en aplicaciones concurrentes ( _Rust Programming Language_ ,
s.funciones f.). Su diseñode orden de sintaxissuperior se (caracteriza _Funciones_ por _De_ ser _Orden_ inmutable _Superior_ por _En_ defecto _Rust_ (Bayhan, _| Programación_ 2024),
_Funcional | LabEx_ , n.d.); además cuenta con structs ( _Defining and Instantiating Structs -
the Rust Programming Language_ , n.d.), enums ( _Enums and Pattern Matching - the Rust
Programming Language_ , n.d.), traits ( _Traits: Defining Shared Behavior - the Rust_

_ProgrammingProgramación_ (^) _RustLanguage_ , n.d.), acogiendon.d.) y métodosciertas características ( _Sintaxis De_ de (^) _Métodos_ una programación _- El Lenguaje_ orientada _De_ a (^)
objetos y una programación funcional.
Rust se caracteriza por tener una curva de aprendizaje relativamente pronunciada por la
introducción de nuevos conceptos como borrowing o lifetimes (Zepeda, 2025). A pesar de
ello,de frameworks es utilizado como para programaciónactix-web o rocket de sistemas (Blandon, (Stevewhims, n.d.), blockchain n.d.), desarrollo (Obregon, web 2024), a través IoT (^)
( _Rust: Bridging the Gap in High-Level Language IoT Innovation | IoT for All_ , n.d.), y
desarrollo de videojuegos (Efixty, n.d.). Aunque su comunidad no desestima su aprendizaje
continuo expresado en foros y tutoriales ( _La Comunidad De Rust · El Lenguaje De
Programación Rust_ , n.d.).
El proyecto hará uso de PLY, que permite la construcción de analizadores y compiladores
haciendo uso de las herramientas lex y yacc en Python ( _PLY (Python Lex-YaCc)_ , n.d.). PLY
está basado en el algoritmo de parsing LALR (1) incluyendo soporte de producciones
vacías, reglas de precedencia, recuperación de errores y manejo de gramáticas ambiguas
( _PLY (Python Lex-Yacc) — Ply 4.0 Documentation_ , n.d.).

## 2. Objetivos del Proyecto

**Objetivo General**

DesarrollarRust utilizando un analizador PLY, integrando léxico, unasintáctico interfaz y semánticoweb que permitepara el lenguajea los usuarios de programación a partir de (^)
ingresar su código fuente visualizar tokens identificados y detectar errores de sintaxis y
semántica.
**Objetivos Específicos**

1. Desarrollarla identificación un analizador de palabras léxico reservadas, que se encargue operadores, de tokenizar delimitadores, código literales Rust mediante y tipos
    de datos, dando al usuario mensajes de advertencia a tokens inválidos.


2. Desarrollar un analizador sintáctico basado en gramáticas BNF que verifique la
    estructura del código Rust, teniendo en cuenta declaración de variables, estructuras
    desintaxis. control, funciones, expresiones aritméticas y booleanas, y reportando errores de
3. Desarrollar un analizador semántico que valide las reglas del lenguaje como tipos de
    datos, declaración previa de variables, alcance de variables, mutabilidad, y retorno
    de funciones, proporcionado mensajes de error semántico.

4. Construirdiferenciada una por interfaz colores web de funcional tokens ycon errores editor según de código su tipo integrado, (léxico, visualización sintáctico y (^)
semántico).

## 3. Analizador Léxico

**Descripción General**
El analizador léxico será capaz de recibir el código en Rust y descomponerlo en tokens
válidos. Las funcionalidades se describen en:

1. Reconocimiento de palabras reservadas, identificadores, literales numéricos y de
    cadena, operadores y delimitadores.
2. Reconocimientode error. de tokens inválidos para ser marcados por un mensaje con el tipo
3. Obtener una lista de tokens reconocidos como válidos.
4. Reconocimiento de comentarios.
Se diferenciará por colores, mostrando tokens válidos en color verde y errores léxicos en
color rojo.
**Componentes Principales**
● **Variables**
En Rust, los nombres de variables deben empezar con una letra o un guión bajo,
seguido de letras, dígitos o guiones bajos (Hiwarale, 2024). Es decir sigue el patrón
[a-zA-Z_][a-zA-Z0-9_]*

```
Tipo de Variable Sintaxis Ejemplo
Variable inmutable
( Variables and Mutability -
theLanguage Rust Programming , n.d.)
```
```
let nombre = valor; let x = 5;
```
Variable mutable (^) let mut nombre =
valor;
let mut count = 0;


```
Constante const NOMBRE: tipo =
valor;
```
```
const MAX_SIZE: u32 =
100;
```
Variable _Items - the_ estática _Rust Refer_ ( _Staticence_ (^) ,
n.d.)
static NOMBRE: tipo =
valor;
static COUNTER: i32 =
0;
● **Tipos de datos**
(^) **Primitivos
Categoría Tipo Descripción Ejemplo**
Enteros con signo
( _Tipos De Datos - El
LenguajeProgramación De_ (^) _Rust_ ,
n.d.)
i8, i16, i32, i64,
i
Enteros con signo
de diferentes
tamaños
let n: i32 = -42;
Enteros sin signo (^) u8, u16, u32,
u64, u
Enteros positivos de
diferentes tamaños let^ age:^ u8^ =^ 25;^
Punto flotante f32, f64 Números decimales let pi: f64 =
3.14159;
Booleano (^) bool Valores true o
false
let is_active:
bool = true;
Carácter char Un carácter Unicode let letra: char =
‘A’;
Cadena ( _String En
Rust_ , n.d.) str,^ String^
Cadenas de texto (^) let msg: &str =
“Hola”;
(^) **Estructurados
Categoría Tipo Descripción Ejemplo**
Vector ( _Vectors -
Rust by Example_ ,
n.d.)
Vec<T> Lista dinámica de
elementos del
mismo tipo.
let nums:
Vec<i32> =
vec![1,2,3];
Array ( _Arrays and
Slices - Rust by_ [T;^ N]^
Lista de tamaño fijo (^) let arr: [i32; 3] =
[1,2,3];


```
Example , n.d.)
Tupla (Hiwarale,
2024) (T1,^ T2,^ ...)^
```
```
Colección de
valores de diferentes
tipos
```
```
let tuple: (i32,
f64) = (5, 3.14);
Hashmap ( HashMap
```
_-_ n.d.) _Rust by Example_ ,

```
HashMap<K,V> Estructura
clave-valor
```
```
let mut map =
Hashmap::new()
;
```
(^) ● **Operadores
Categoría Operador Significado Ejemplo**
Aritméticos ( _B -
Operadores Y
SímbolosLenguaje - De El
Programación Rust_ ,
n.d.)
+ Suma a + b

- Resta a - b
* Multiplicación a * b
/ División a / b
% Módulo a % b

Comparación (^) == Igual a (^) a == b
!= Diferente^ a != b
< Menor^ que^ a < b
<= Menor^ o^ igual^ que^ a <= b
> Mayor que a > b
>= Mayor o igual que a >= b
Lógicos && AND Lógico a && b
|| OR Lógico a || b
! NOT^ Lógico^ !a
Asignación (^) = Asignación simple (^) x = 5
+= Suma^ y^ asigna^ x += 3
-= Resta^ y^ asigna^ x -= 2


*= Multiplica y asigna x *= 4
/= Divide y asigna x /= 2
Otros & Referencia &x
* Dereferencia *ptr
:: Resolución de ruta std::io::stdin()
-> Tipo^ de^ retorno^ fn suma() -> i
=> Brazo^ de^ match^ Some(x) => x
● **Palabras Reservadas**

**Palabra Significado Categoría**
fn Declaración _Palabras Claves_^ de^ función _- El_^ ( _A_^ _-_^
_Lenguaje De Programación
Rust_ , n.d.)

```
Función
```
let Declaración de variable
inmutable

```
Variable
```
mut Modificador de mutabilidad Variable
const Declaración de constante Variable
static Variable^ estática^ Variable^
if Estructura^ condicional^ Control^
else Alternativa^ de^ condicional^ Control^
match Coincidencia de patrones Control
while Bucle condicional Control
for Bucle iterativo Control
loop Bucle infinito Control
break Salir de bucle Control
continue Siguiente^ iteración^ Control^


return Retornar valor de función Control
struct Definir estructura Tipo
enum Definir enumeración Tipo
impl Implementar métodos Tipo
trait Definir interfaz Tipo
type Alias^ de^ tipo^ Tipo^
pub Modificadorpública de^ visibilidad^ Modificador^

use Importar^ módulo,^ elemento^ Módulo^
mod Declarar módulo Módulo
as Renombrar importación /
casting

```
Operador
```
in Pertenencia en iterador Operador
true Valor booleano verdadero Literal
false Valor booleano falso Literal

```
● Comentarios
```
**Tipo Sintaxis Ejemplo**

Comentario( _Comentarios_ de _-_ (^) línea _El Lenguaje_ (^)
_De Programación Rust_ ,
n.d.)
// comentario // Esto es un
comentario
Comentario multilínea
( _Comentarios - Tutorial
Rust_ , n.d.)
/* comentario */ /* Comentario en
múltiples líneas */
Comentariodocumentación de (^)
( _Comentarios Y
Documentación -
manuel.cillero.es_ , 2020)
/// comentario /// Documenta la
función


```
● Delimitadores
Símbolo Nombre Uso
; (De Tinchicus, 2022) Punto y coma Terminar declaraciones
{ } ( Funciones - El
Lenguaje De Programación
Rust , n.d.)
```
```
Llaves Delimitar bloques de código
```
```
( ) ( Sintaxis De Métodos -
El Lenguaje De
Programación Rust , n.d.)
```
```
Paréntesis Agrupar expresiones,
parámetros de funciones
[ ] ( Tipos Colección - Rust
En Español Fácil , n.d.)
```
```
Corchetes Definir arrays, indexar
colecciones
, Coma^ Separar^ elementos^ en^ listas^
```
. ( _Sintaxis De Métodos - El
Lenguaje De Programación
Rust_ , n.d.)

```
Punto Acceder a campos/métodos
```
```
: (De Tinchicus, 2022) Dos puntos Especificar tipos
:: ( ¿Qué Es El Ownership? -
El Lenguaje De
Programación Rust , n.d.)
```
```
Doble dos puntos Accedermódulos/tipos a elementos de
```
## 4. Analizador Sintáctico

**Descripción General**
● El analizador sintáctico será capaz de convertir los token generados por el
analizador léxico en un árbol sintáctico abstracto (AST) representando la estructura
jerárquicaTorczon, 2011). del código, detecta errores sintácticos y reporta problemas (Cooper y

**Reglas Gramaticales**

```
● Declaración de variables
```

A continuación, se mostrará la sintaxis general en estructura BNF (The Rust Project
Developers, s. f.) que el analizador considera válido para cada tipo de variable y
patrón estructural:
**Variables locales ‘let’ mutables e inmutables**
El analizador sintáctico posee una estructura flexible para las variables locales,
siendo opcionales la declaración explícita del tipo y la inicialización de la variable.
_<DeclaracionLet> ::= “let” [“mut”] <Identificador> [“:” <Tipo>] [“=”
<Expresion>] “;”_

**Sin tipo y sin valor** (^) Ej: let x; o let mut x;
**Sin tipo y con valor** Ej: let x: i32; o let mut x: i32;
**Con tipo y sin valor** Ej: let x = 5; o let mut x = 5;
**Con tipo y con valor** Ej: let x: i32 = 5; o let mut x: i32 = 5;
**Variables Constantes ‘const’**
A diferencia de las variables locales, las variables constantes poseen una estructura
sintácticamente correcta más rígida y no posee campos opcionales, la omisión de
cualquier campo se considera un error de sintaxis.
_<DeclaracionConst> ::= “const” <Identificador> “;” <Tipo> “=”
<Expresion> “;”_
Ejemplo:
const X: u32 = 5;
**Variables estáticas**
Ely que analizador tengan inicializadoconsidera válido algún las valor. declaraciones que indiquen explícitamente el tipo
_<DeclaracionStatic> ::= “static” [“must”] <Identificador> “:” <Tipo>
“=” <Expresion> “;”_
Ejemplo:


```
static X: u32 = 5;
```
**● Expresiones Aritméticas**

Elanalizador analizador léxico tiene en que un (^) árboltransformar de expresiones la secuencia jerárquicas, de tokens el quecual vienen debe representar del (^)
con fidelidad el orden en que se ejecutan las operaciones, respetando la precedencia
organizada por niveles de menor a mayor.
A continuación, se mostrarán las reglas que de forma recursiva se organizan los
valores numéricos de acuerdo al tipo de operación aritmética involucrada.
**Reglas para la suma y resta (Nivel 1)**
<Expresion> ::= <Termino>
| <Expresion> “+” <Expresion>
| <Expresion> “-” <Expresion>
**Regla para la Multiplicación, división y módulo (Nivel 2)**
<Termino> ::= <Factor>
| <Termino> “*” <Factor>
| <Termino> “/” <Factor>
| <Termino> “%” <Factor>
**Regla para la negación (Nivel 3)**
<Factor> ::= <Primario>
| “-” <Factor>
**Reglas de las unidades básicas (Nivel 4)**


```
<Primario> ::= <Numero>
| <Identificador>
| “(” <Expresion> “)”
Ejemplo:
let resultado = -a * (2 + b);
```
**● Expresiones Booleanas**
En analizador realiza un proceso parecido que con las expresiones aritméticas, ya
que los tokens se van organizando en niveles para asegurar la precedencia de los
operadores lógicos y de comparación.
En las expresiones de comparación, dos expresiones son comparadas entre sí, en las
expresiones lógicas las expresiones booleanas se combinan mediante operadores
lógicos.
**Jerarquía de precedencia booleana:**

```
OR Logico “||” (Nivel 1)
<ExpresionBooleana> ::= <TerminoLogico>
| <ExpresionBooleana> “||” <TerminoLogico>
```
```
AND Lógico (Nivel 2)
<TerminoLogico> ::= <FactorLogico>
| <TerminoLogico> “||” <FactorLogico>
```
```
Operadores de Comparación y NOT Lógico (Nivel 3)
<FactorLogico> ::= <ExpresionComparacion>
```

```
| “!” <PrimarioBooleano> //NOT Logico
<ExpresionComparacion> ::=
<ExpresionAritmetica><OperadorComparacion><ExpresionAritmeti
ca>
| < ́PrimarioBooleano>
<OperadorComparacion> ::= “==” | “!=” | “<” | “>” | “<=” | “>=”
```
```
Unidades Básicas (Nivel 4)
<PrimarioBooleano> ::= “true”
| “false”
| <Identificador> //Variables booleanas
| “(” <ExpresionBooleana> “)”
```
```
Ejemplo
let es_valido = x > 5 && !bloqueado || es_admin;
```
**● Estructuras de Control**
El analizador se enfoca en encontrar las palabras claves que inician una estructura
dela estructuracontrol (if, BNF else, que while, define etc) la y plantillavalida la correcta secuencia de decómo tokens se estructuran que le sigue. de Esta forma es
sintácticamente correcta las estructuras de control:

```
Condicional IF-ELSE
Ejecuta un bloque de código si se cumple la condición.
Estructura BNF:
<IfElse> ::= “if ” <Expresion> “{” <BloqueCodigo> “}”
```

```
[ “else” ”{” ( <IfElse> | <BloqueCodigo> ) “}” ]
```
**Ejemplo:**
if x>0 {

println!(“x mayor que 0”);
} else{

println!(“X no es mayor que 0”);
}

**Bucle While**
Repite el código mientras se cumpla la condición.
**Estructura BNF:**
<While> ::= “while” <Expresion> “{” <BloqueCodigo> “}”
**Ejemplo:**

let x = 0;
while (x<5){

x++;

}

**Bucle for**
Itera sobre un rango o una colección de elementos.
**Estructura BNF**
<For> ::= “for” <Identifiacador> “in” <Expresion> “{” <BloqueCodigo> “}”
**Ejemplo:**


for num in 0..5 {
println!(“imprimiendo el número: {}”,num);
}

**Bucle loop**
Crea un bucle infinito hasta que se ejecuta el la palabra clave break.
**Estructura BNF**
<Loop> ::= “loop” “{” <BloqueCodigo> “}”
Ejemplo:
loop{

println!(“Estoy dentro del loop..”);
break;

}

**Estructuras de Datos**
El analizador debe reconocer la sintaxis al declarar instancias de una estructura de
datos prestando especial atención a los delimitadores y las palabras claves.
**Array**
Colección de tamaño fijo que alberga elementos del mismo tipo.
**Estructura BNF**
<LiteralArray> ::= “[” <ContenidoArray> “]”

<ContenidoArray> ::= <ListaExpresiones>

| <Expresion> “;” <Expresion>
| “ ” // Vacío


```
Ejemplo
let mi_array = []; //vacio
let mi_array = [1,2,3];
```
```
Tuplas
Es un tipo de estructura compuesta de tamaño fijo, en la cual se pueden guardar
elementosdebe agregar de unadiferentes “,” al finaltipos. para En casodiferenciarla de guardar de ununa solo declaración elemento de en variable la tupla se
normal.
Estructura BNF
<LiteralTupla> ::= “(” [ <ListaExpresiones> ] “)” “;”
<ListaExpresiones> ::= <Expresion> {“,” <Expresion> }[“,”]
Ejemplo
let mi_tupla(i32, f64, &str) = (50, 3.14, “hola”);
```
**● Declaraciones de funciones
Funciones con N parametros
Estructura BNF**
<DeclaracionFuncion> ::= "fn" <Identificador> "(" [ <ListaParametros>
] ")"
[ "->" <Tipo> ] "{" <BloqueCodigo> "}"
<ListaParametros> ::= <Parametro> { "," <Parametro> }
<Parametro> ::= ["mut"] <Identificador> ":" <Tipo>
Ejemplo:
fn procesar_usuario (id: u32, nombre: &str, activo: bool) -> bool {


```
println!("Procesando a {}: {}", id, nombre);
activo
}
```
```
Funciones lambda
Estructura BNF
<Closure> ::= "|" [ <ParametrosClosure> ] "|" <CuerpoClosure>
<ParametrosClosure> ::= <Identificador> [":" <Tipo>]
{ "," <Identificador> [":" <Tipo>] }
<CuerpoClosure> ::= ( [ "->" <Tipo> ] ( <BloqueCodigo> | <Expresion> )
)
Ejemplo:
let sumar = |a: i32, b: i32| -> i32 {
a + b
};
let resultado = sumar(5, 10);
```
**● Impresión y solicitud de datos
Regla para imprimir**
La impresión se madeja con macros manteniendo la siguiente estructura:
**Estructura BNF**
<MacroImpresion> ::= <IdentificadorMacro> "!" "(" [
<ListaArgumentos> ] ")" ";"
<IdentificadorMacro> ::= "println" | "print" | "eprintln" | "eprint"


```
<ListaArgumentos> ::= <Expresion> { "," <Expresion> }
Ejemplo
println!("Hola, mundo!");
```
```
Regla para Solicitar Datos por Teclado
Se realiza mediante el uso de las funciones de la biblioteca st::io. Es por ello que el
analizador no tendra una unica regla sino que
Estructura BNF
<Ruta> ::= <Identificador> { "::" <Identificador> }
<LlamadaFuncion> ::= <Ruta> "(" [ <ListaArgumentos> ] ")"
<LlamadaMetodo> ::= <Expresion> "." <Identificador> "(" [
<ListaArgumentos> ] ")" ";"
Ejemplo
let mut buffer = String::new();
io::stdin().read_line(&mut buffer);
```
## 5. Analizador Semántico

**Descripción General**
● El analizador semántico se encarga de verificar la coherencia lógica del código

fuente.comoanterior. En esta entrada etapa (^) serecibe comprueba el árbol el (^) cumplimientosintáctico abstracto de las reglasgenerado de tipo, en (^) alcancela etapa y (^)
contexto del lenguaje Rust. Para lograr esto se mantendrá el uso de una tabla de
símbolos (Aho et al., 2007), que por lo general es una piña hashmap en donde se
registrará información clave de los identificadores declarados.
● Las principales funcionalidades del analizador semántico son:
o **Type Checking::** Asegura compatibilidad entre los tipos de datos dentro de
una operación.


```
o Scope Analysis: Verifica que todas las variables y funciones sean declaradas
previo su uso y accesibles desde donde son invocadas.
o Valida inmutables la mutabilidad: o constantes. Verifica que se cumpla la naturaleza de las variables
```
```
o Verificación de flujo de control: asegura que las palabras claves como
“ break ” o “ return ”no se usen en contextos inadecuados.
```
**Reglas Semánticas
● Identificadores
Regla de validación de Existencia**
Esta es la regla semántica más fundamental, el analizador al encontrar una función
siendo usada en una expresión, busca que haya sido declarada en la tabla de

símbolossuperiores. la Si búsquedano la encuentra la realiza significa desde que el noalcance fue declarada actual (^) ohasta que (^) nolos esalcances visible (^)
desde ese punto.
**Mensaje de error semántico:** Error Semántico (Línea X): Identificador no
encontrado. La variable '{nombre_variable}' no ha sido declarada en este alcance.
**Regla de alcance Local**
Esta regla se enfoca en limitar el alcance de una variable descarada dentro de un
bloque de código, asegurándose que solo viva dentro de ese bloque de código. Si se
busca acceder a esta variable desde fuera del bloque de código la búsqueda en la
tabla de símbolos fallará, ya que esa variable no existe en ese contexto.
Osea que no se puede acceder a variables declaradas en un alcance menor con
respecto al alcance local de donde se hace el acceso.
**Mensaje de error semántico:** Error Semántico (Línea X): El identificador
'{nombre_variable}' no es accesible. Fue definido en un alcance interno que ya
finalizó.
**● Asignación de tipo**


```
Regla de discrepancia de Tipos en la Declaración Explícita
Al declarar una variable en donde se especifica su tipo explícitamente, el analizador
debecaso: validar que coincida con el tipo del valor ingresado. Osea que para el siguiente
```
```
let <identificador> ”:” <Tipo> “=” <Expresion> “:”
El tipo de <Expresion> debe ser del mismo tipo de dato que el que fue especificado
en <Tipo>
Mensaje de error semántico: Error Semántico (Línea X): Discrepancia de tipos.
Se esperaba tipo '{Tipo_Declarado}' pero se encontró tipo '{Tipo_Evaluado}' en la
asignación de '{id}'.
Regla de discrepancia de tipos en la reasignación
Estauna variableregla es queaplicable ya fue en inicializada, variables mutables, debe ser el exactamente tipo de dato del que mismo se quiere tipo asignar de dato a
que el valor asignado anteriormente.
Mensaje de error semántico: Error Semántico (Línea X): Discrepancia de tipos en
la reasignación. La variable '{id}' tiene el tipo '{Tipo_Original}', pero se intentó
asignar un valor de tipo '{Tipo_Nuevo}
```
**● Operaciones permitidas
Regla de compatibilidad de tipos en operaciones aritméticas**
Para cualquier expresión aritmética _<Operando> <Operador> <Operando>_ es
válida si y solo si el tipo de dato de ambos _<Operando>_ sean iguales, de no serlo se
arrojará un error semántico.
**Mensaje de error semántico:** Error Semántico (Línea X): Operador aritmético
'{operador}' no puede aplicarse a tipos '{Tipo_LHS}' y '{Tipo_RHS}'. No existe
una implementación para esta operación.

```
Regla: Restricción de Tipo en Operadores Lógicos
Los operadores lógicos, tales como: && (AND Lógico) y || (OR Lógico) sólo
pueden ser usados entre dos valores de tipo “boolean”, así mismo, el operador
```

```
lógico! (NOT Lógico) sólo puede ser usado con un único valor de tipo “boolean”.
De querer usar este tipo de operador con otro tipo de dato salta error.
```
**Mensaje** '<OperadorLogico>' **de error** (^) no **semántico:** puede aplicarse Error al Semánticotipo '{Tipo_RHS}'. (Línea X):Se esperaba Operador 'bool'. lógico

## 6. Plan de Implementación

```
Herramientas de desarrollo y test.
Herramienta Descripción
Python Lenguajeusar PLY. de programación en el backend, requerido para
PLY Biblioteca de python, necesaria en la construcción del
analizador léxico (Lex) y del analizador sintáctico (Yacc)
FastAPI Framework web ligero usado para crear la API que conecta
el frontend con el backend.
HTML / CSS Lenguaje de marcado y estilo para construir la interfaz web
JS Lenguaje de programación usado en el frontend para el
manejo de la interactividad
PyTest Framework de testing para Python. Crea y ejecuta casos de
prueba validando el correcto funcionamiento de los
analizadores.
```
```
Tabla de asignación de reglas
Integrante Usuario de
Github
```
```
Tareas
Victor
Borbor
```
@vicbguti29 (^) Analizador léxico con su test, API REST y Interfaz
Web
Angello
Vasconez
@Alvasconv (^) Analizador sintáctico, analizador semántico con sus
test

## 7. Diseño Preliminar


El proyecto incluirá un panel izquierdo con un editor de código. Un panel izquierdo con
vista de tokens y errores.

El objetivo de la interfaz propuesta es que se pueda realizar análisis léxico, análisis
semántico y análisis semántico por separado o en conjunto.
● Visualización de tokens identificados por el analizador léxico.
● Visualización de errores identificados.

Indicadores visuales
● Tokens válidos (verdes).
● Errores léxicos (rojo).
● Errores sintácticos (naranja).
● Errores semánticos (morado).


## 8. Pruebas y Validación (En cada avance)

**Casos de Prueba**
● Cada integrante deberá crear un algoritmo en su LP asignado con la mayoría de
tokens. Estos algoritmos se utilizarán como entrada para su fase de test. Puede
generarlos con IA Generativa.

● Suprueba analizador deberá deberágenerarse generar un log logs que del incluya análisis el realizadonombre del ( **Avance** análisis **1,** (^) - (^2) desarrollador **y 3** ), por cada - (^)
fecha-hora. Por ejemplo lexico-rodrigosaraguro-03-07-2025-17:30.txt o
semantico-luisperez-10-11-2025-14:23.txt. Estos logs solo se deberán actualizar en
su repositorio de proyecto.
**Resultados**
Cada semana se irán subiendo en esta sección los Avances 1, 2, 3 y deberá agregar
capturas de las pruebas realizadas en su interfaz gráfica.
Recuerde que cada integrante deberá probar su propio algoritmo y presentar al
menos una captura con error léxico, sintáctico o semántico, según el avance actual.

## 9. Conclusiones y Recomendaciones (al final del proyecto)

**Resumen**
● Las conclusiones deben tener 3 enfoques: una conclusión hacia el lenguaje
asignado,conclusión otra hacia conclusión la herramienta hacia PLYla experiencia utilizada. de desarrollar los analizadores, una

**Recomendaciones y trabajos futuros**
● Cada integrante deberá responder las siguientes preguntas:
o ¿Cómo evaluaría su solución actual según las funcionalidades desarrolladas
o y¿Cómo^ la^ arquitectura? podría mejorar^ su proyecto? Nuevas funcionalidades, correcciones.
● De preferencia crear una tabla con el nombre del integrante y sus respuestas. Por
cada respuesta de integrante pueden usar una fila.
● Este apartado no influirá en su calificación de proyecto, es para utilizarlo en una
medición para ABET.

## 10. Referencias

_Rust Programming Language_. (s. f.). https://rust-lang.org/


Bayhan, B. B. (2024, 22 enero). Lenguaje de programación Rust: Guía para principiantes -
Apiumhub. _Apiumhub_.
https://apiumhub.com/es/tech-blog-barcelona/lenguaje-de-programacion-rust/#:~:te
xt=En%20Rust%2C%20el%20comportamiento%20por,expl%C3%ADcitamente%2
0mut%20despu%C3%A9s%20de%20let.
_Funciones de Orden Superior en Rust | Programación Funcional | LabEx_. (n.d.). LabEx.
https://labex.io/es/tutorials/exploring-rust-s-functional-capabilities-99330
_Defining and instantiating structs - the Rust programming language_. (n.d.).
https://doc.rust-lang.org/book/ch05-01-defining-structs.html
_Enums and pattern matching - the Rust programming language_. (n.d.).
https://doc.rust-lang.org/book/ch06-00-enums.html
_Traits: Defining shared behavior - the Rust programming language_. (n.d.).
https://doc.rust-lang.org/book/ch10-02-traits.html
_Sintaxis de Métodos - El Lenguaje de Programación Rust_. (n.d.).
https://book.rustlang-es.org/ch05-03-method-syntax
Zepeda, E. (2025, October 20). ¿Qué hace al lenguaje Rust tan difícil de aprender? _Coffee
bytes_.
https://coffeebytes.dev/es/rust/que-hace-al-lenguaje-rust-tan-dificil-de-aprender/
Stevewhims. (n.d.). _Información general sobre el desarrollo en Windows con Rust_.
Microsoft Learn.
https://learn.microsoft.com/es-es/windows/dev-environment/rust/overview
Blandon, J. (n.d.). _Desarrollo web con Rust - Introducción a Actix Web_. Rusty Full Stack.
https://rustyfullstack.com/blog/desarrollo-web-con-rust---introduccion-a-actix-web


Obregon, A. (2024, 28 abril). _The Rise of Rust in Blockchain Development_. Medium.
https://medium.com/@AlexanderObregon/the-rise-of-rust-in-blockchain-developme
nt-eddbad0d9424
_Rust: Bridging the Gap in High-Level Language IoT Innovation | IoT For All_. (n.d.). IoT
for All.
https://www.iotforall.com/rust-bridging-the-gap-in-high-level-language-iot-innovati
on
Efixty. (n.d.). _Motores de desarrollo de juegos para Rust : r/rust_.
https://www.reddit.com/r/rust/comments/198d70i/game_dev_engines_for_rust/?tl=e
s-419
_La comunidad de Rust · El lenguaje de programación Rust_. (n.d.).
https://prev.rust-lang.org/es-ES/community.html
_PLY (Python Lex-YaCc)_. (n.d.). https://www.dabeaz.com/ply/
_PLY (Python Lex-Yacc) — ply 4.0 documentation_. (n.d.). https://ply.readthedocs.io/en/latest/
Hiwarale, U. (2024, 18 noviembre). _Understanding Variables and Data Mutability in Rust:
A Beginner’s Guide_. Medium.
https://medium.com/rustycrab/understanding-variables-and-data-mutability-in-rust-
a-beginners-guide-1fb80fc8446f
_Variables and mutability - the Rust programming language_. (n.d.).
https://doc.rust-lang.org/book/ch03-01-variables-and-mutability.html
_Static items - The Rust Reference_. (n.d.).
https://doc.rust-lang.org/reference/items/static-items.html
_Tipos de Datos - El Lenguaje de Programación Rust_. (n.d.).
https://book.rustlang-es.org/ch03-02-data-types


_String en Rust_. (n.d.). Blog De Rust Lang En Español 2025.
https://blog.rustlang-es.org/articles/strings
_Vectors - rust by example_. (n.d.). https://doc.rust-lang.org/rust-by-example/std/vec.html
_Arrays and slices - rust by example_. (n.d.).
https://doc.rust-lang.org/rust-by-example/primitives/array.html
_Estructuras de Tupla - Tutorial Rust_. (n.d.).
https://ferestrepoca.github.io/paradigmas-de-programacion/progconcurrente/tutorial
es/Libro_Rust_2022_1/tutorial/estructuras/tupla.html
_HashMap - Rust by example_. (n.d.). https://doc.rust-lang.org/rust-by-example/std/hash.html
_B - Operadores y Símbolos - El Lenguaje de Programación Rust_. (n.d.).
https://book.rustlang-es.org/appendix-02-operators
_A - Palabras claves - El Lenguaje de Programación Rust_. (n.d.).
https://book.rustlang-es.org/appendix-01-keywords
_Comentarios - El Lenguaje de Programación Rust_. (n.d.).
https://book.rustlang-es.org/ch03-04-comments
_Comentarios - Tutorial Rust_. (n.d.).
https://ferestrepoca.github.io/paradigmas-de-programacion/progconcurrente/tutorial
es/Libro_Rust_2022_1/tutorial/generalidades/comentarios.html
_Comentarios y documentación - manuel.cillero.es_. (2020, December 16). manuel.cillero.es.
https://manuel.cillero.es/doc/apuntes-tic/rustlang/el-lenguaje-rust/comentarios-y-doc
umentacion/
De Tinchicus, V. T. L. E. (2022, May 16). _Rust / Punto y coma_. El Blog De Tinchicus.
https://tinchicus.com/2022/07/06/rust-punto-y-coma/


_Funciones - El Lenguaje de Programación Rust_. (n.d.).
https://book.rustlang-es.org/ch03-03-how-functions-work
_Tipos colección - Rust en español fácil_. (n.d.).
https://www.jmgaguilera.com/rust_facil/17.html
De Tinchicus, V. T. L. E. (2022, July 4). _Rust / Herencia en trait_. El Blog De Tinchicus.
https://tinchicus.com/2022/08/04/rust-herencia-en-trait/
_¿Qué es el Ownership? - El Lenguaje de Programación Rust_. (n.d.).
https://book.rustlang-es.org/ch04-01-what-is-ownership
_El libro clásico de Compiladores (El "Dragon Book") Aho, A. V., Lam, M. S., Sethi, R., &
Ullman, J. D. (2007). Compilers: Principles, Techniques, & Tools (2nd Edition).
Pearson.
https://www.pearson.com/us/higher-education/program/Aho-Compilers-Principles-
Techniques-and-Tools-2nd-Edition/PGM153552.html_

_La Referencia oficial de Rust (para la gramática) The Rust Project Developers. (s. f.). The
Rust Reference. https://doc.rust-lang.org/reference/
CooperKaufmann., K. D., & Torczon, L. (2011). Engineering a Compiler (2nd Edition). Morgan
https://www.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-088478-0_


