# DroneScript Grammar (DroneScript.g4)

## Descripción

El archivo `DroneScript.g4` contiene la **especificación formal** del lenguaje DroneScript usando la sintaxis ANTLR4. Esta gramática define todos los tokens (símbolos léxicos) que el analizador debe reconocer.

## Estructura de la Gramática

### 1. Canales (Channels)
Define canales para agrupar tokens que se ignoran automáticamente:
- `WHITESPACE_CHANNEL`: espacios en blanco
- `COMMENTS_CHANNEL`: comentarios

### 2. Whitespace y Comentarios
- `WS`: espacios, tabs, saltos de línea → se ignoran
- `LINE_COMMENT`: comentarios `// ... \n`
- `BLOCK_COMMENT`: comentarios `/* ... */`

### 3. Palabras Clave por Categoría

La gramática organiza las palabras clave en 14 categorías semánticas:

| Categoría | Ejemplos | Cantidad |
|-----------|----------|----------|
| **CONTROL** | despegar, aterrizar, emergencia | 11 |
| **MOVEMENT** | mover, rotar, avanzar, bajar | 11 |
| **DIRECTION** | norte, sur, este, oeste, arriba, abajo | 12 |
| **GPS** | coordenada, gps, navegar, waypoint | 11 |
| **SENSOR** | escanear, lidar, giroscopio | 12 |
| **CAMERA** | activar_camara, tomar_foto, zoom | 10 |
| **BATTERY** | bateria, cargar, nivel_bateria | 6 |
| **CONDITIONAL** | si, mientras, para, fin | 12 |
| **COMMUNICATION** | conectar, wifi, bluetooth, radio | 9 |
| **SECURITY** | autenticar, bloquear, zona_segura | 7 |
| **ENVIRONMENT** | viento, lluvia, temperatura | 6 |
| **AI** | modo_autonomo, explorar, mapear | 8 |
| **DATA_TYPE** | entero, texto, booleano, verdadero | 6 |
| **EVENT** | al_detectar, al_colisionar | 6 |

**Total: ~127 palabras clave reservadas**

### 4. Operadores

#### Aritméticos
- `+`, `-`, `*`, `/`, `%`

#### Comparación
- `<`, `>`, `<=`, `>=`, `==`, `!=`

#### Lógicos
- `&&`, `||`, `!`

#### Asignación
- `=`

### 5. Delimitadores
- Paréntesis: `(`, `)`
- Llaves: `{`, `}`
- Corchetes: `[`, `]`
- Puntuación: `;`, `,`, `:`

### 6. Literales

#### Strings
- Formato: `"texto"`
- Soporta escapes: `\"`, `\\`, `\n`, `\t`, `\r`
- Ejemplo: `"Nueva York"`, `"Coordenada: (40.7, -74.0)"`

#### Números Flotantes
- Formato: `[0-9]+ '.' [0-9]+`
- Ejemplos: `3.14`, `40.7128`, `0.5`

#### Números Enteros
- Formato: `[0-9]+`
- Ejemplos: `10`, `90`, `100`

#### Identificadores
- Formato: `[a-zA-Z_][a-zA-Z0-9_]*`
- Ejemplos: `motor_1`, `_sensor`, `altura123`
- Notas: No puede empezar con dígito

## Reglas Léxicas Importantes

### Precedencia de Tokens
La orden en el archivo `.g4` define precedencia. El lexer intenta coincidencias en orden:

1. **Palabras clave primero** (más específicas): `despegar`, `aterrizar`, etc.
2. **Operadores multi-carácter** antes de single: `==` antes que `=`
3. **Números flotantes** antes que enteros: `3.14` vs `3`
4. **Identificadores** último (más general)

### No Diferencia Mayúsculas
Las palabras clave son case-insensitive (por diseño académico). `DESPEGAR`, `Despegar`, `despegar` son equivalentes.

### Strings y Escapes
- Los strings entre comillas dobles (`"..."`)
- Los escapes válidos: `\"` (comilla), `\\` (barra invertida), `\n` (newline)
- Strings no cerrados generan error léxico

## Compilación con ANTLR (Opcional)

Para compilar la gramática a código Python:

```bash
# Instalar ANTLR (si no está instalado)
# En Windows: choco install antlr4
# En Mac: brew install antlr
# En Linux: apt-get install antlr4

# Compilar la gramática
antlr4 -Dlanguage=Python3 -visitor -listener grammar/DroneScript.g4
```

Esto genera:
- `DroneScriptLexer.py`: Lexer compilado
- `DroneScriptParser.py`: Parser compilado (futuro)
- `DroneScriptListener.py`: Listener para recorrer el árbol (futuro)
- `DroneScriptVisitor.py`: Visitor para procesar el árbol (futuro)

## Fases Futuras

Este archivo `.g4` está diseñado para ser extensible:

1. **Fase Actual (Lexer)**: Solo tokens (reglas de lexer)
2. **Fase Parser**: Agregar reglas de sintaxis (parser rules)
3. **Fase AST**: Agregar acciones y anotaciones semánticas
4. **Fase Transpilador**: Procesamiento del AST para generar Python

Para pasar a la siguiente fase, simplemente agrega las reglas de parser:

```antlr
// Ejemplo para fase parser
program: statement+;
statement: command SEMICOLON;
command: KEYWORD_CONTROL (expression)*;
expression: IDENTIFIER | NUMBER | FLOAT | STRING;
```

## Relación con la Implementación Python

El archivo `DroneScript.g4` es una **especificación formal**. La implementación actual usa un **lexer manual en Python** que sigue exactamente esta gramática.

Cada token en el lexer manual corresponde a una regla en `DroneScript.g4`:
- Palabras clave → `KW_*` tokens
- Operadores → tokens de operador
- Delimitadores → tokens de delimitador
- Números → `INTEGER`, `FLOAT`
- Strings → `STRING`
- Identificadores → `IDENTIFIER`

## Referencias

- [ANTLR4 Documentation](https://antlr.org/)
- [ANTLR4 Python Runtime](https://github.com/antlr/antlr4/tree/master/runtime/Python3)
- DroneScript Lexer Specification (este proyecto)

