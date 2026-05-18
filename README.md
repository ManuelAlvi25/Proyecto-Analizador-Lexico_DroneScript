# DroneScript Lexer - Analizador Léxico Académico

<img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python 3.8+">
<img src="https://img.shields.io/badge/License-Academic-green" alt="Academic Project">
<img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Active">

## 📋 Descripción del Proyecto

**DroneScript Lexer** es un **analizador léxico completo** para un lenguaje personalizado de control de drones y robots autónomos llamado **DroneScript**. Este proyecto fue desarrollado como parte de un curso de **Compiladores/Análisis Léxico** con un enfoque académico y profesional.

El proyecto implementa:
- ✅ **Análisis léxico robusto** que convierte código fuente en tokens
- ✅ **Reconocimiento de 127+ palabras clave** organizadas semánticamente
- ✅ **Manejo avanzado de errores** con línea y columna precisas
- ✅ **Soporte de comentarios** (línea y bloque)
- ✅ **Procesamiento de strings** con escapes
- ✅ **Operadores** simples y multi-carácter
- ✅ **Salida estructurada** (tabla ASCII, JSON, simple)
- ✅ **Arquitectura modular** preparada para fases futuras (parser, AST, transpilador)

## 🎯 Características Principales

### 1. Reconocimiento de Tokens
- **Palabras clave**: 127 palabras reservadas categorizadas semánticamente
- **Identificadores**: Válidos e inválidos con validación de formato
- **Números**: Enteros y flotantes
- **Strings**: Con soporte de escapes (`\"`, `\\`, `\n`, `\t`, `\r`)
- **Operadores**: Aritméticos, comparación, lógicos, asignación
- **Delimitadores**: Paréntesis, llaves, corchetes, puntuación
- **Comentarios**: De línea (`//`) y bloque (`/* */`)

### 2. Categorización Semántica
Los tokens se clasifican en **categorías semánticas** que reflejan su rol en el lenguaje:

```
CONTROL           → despegar, aterrizar, emergencia, etc.
MOVEMENT          → mover, rotar, avanzar, bajar, etc.
DIRECTION         → norte, sur, este, oeste, arriba, abajo
GPS               → coordenada, navegar, waypoint, etc.
SENSOR            → escanear, lidar, giroscopio, etc.
CAMERA            → activar_camara, tomar_foto, zoom, etc.
BATTERY           → bateria, cargar, nivel_bateria, etc.
CONDITIONAL       → si, mientras, para, fin, etc.
COMMUNICATION     → conectar, wifi, bluetooth, etc.
SECURITY          → autenticar, bloquear, zona_segura, etc.
ENVIRONMENT       → viento, lluvia, temperatura, etc.
AI                → modo_autonomo, explorar, mapear, etc.
DATA_TYPE         → entero, decimal, texto, booleano, etc.
EVENT             → al_detectar, al_colisionar, etc.
```

### 3. Manejo Robusto de Errores
- Detección de **caracteres desconocidos**
- Detección de **strings no cerrados**
- Detección de **comentarios no cerrados**
- Detección de **secuencias de escape inválidas**
- **Recuperación de errores**: Continúa analizando sin detener en el primer error
- **Reportes precisos**: Línea, columna, contexto visual

Ejemplo de reporte de error:
```
[ERROR] UNKNOWN_CHARACTER
Line 1, Column 9
Character: '#'
Message: Símbolo desconocido '#'

Context:
  1 | despegar#;
      |         ^
```

### 4. Salida Flexible
**Tres formatos de salida disponibles**:

#### Tabla ASCII (default)
```
TOKEN ANALYSIS REPORT
================================================================================
File: tests/valid/simple.drs
Total tokens: 4
Status: ✓ OK (no errors)

TYPE      | LEXEME    | LINE | COL | CATEGORY
----------|-----------|------|-----|------------------
KEYWORD   | despegar  | 1    | 1   | CONTROL
DELIMITER | ;         | 1    | 9   | DELIMITER_PUNCTUATION
KEYWORD   | aterrizar | 2    | 1   | CONTROL
DELIMITER | ;         | 2    | 10  | DELIMITER_PUNCTUATION
```

#### JSON (para procesamiento automático)
```json
{
  "file": "tests/valid/simple.drs",
  "status": "success",
  "tokens": [
    {
      "type": "KEYWORD",
      "category": "CONTROL",
      "lexeme": "despegar",
      "literal_value": null,
      "line": 1,
      "column": 1
    },
    ...
  ],
  "error_count": 0,
  "errors": []
}
```

#### Simple (compatible con scripts)
```
(KEYWORD, despegar)
(DELIMITER, ;)
(KEYWORD, aterrizar)
(DELIMITER, ;)
```

## 🚀 Instalación

### Requisitos
- **Python 3.8 o superior**
- No requiere dependencias externas (usa librería estándar)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd DroneScript-Lexer
   ```

2. **Verificar requisitos** (opcional)
   ```bash
   pip install -r requirements.txt
   ```
   Nota: El archivo `requirements.txt` está vacío (solo documentación), no se requieren instalaciones.

3. ¡Listo! El proyecto está en Python puro sin dependencias.

## 📚 Uso

### Uso Básico

```bash
# Analizar un archivo simple
python src/main.py tests/valid/simple.drs

# Salida en formato JSON
python src/main.py tests/valid/simple.drs --format json

# Salida simple
python src/main.py tests/valid/simple.drs --format simple
```

### Opciones Avanzadas

```bash
# Ver solo errores
python src/main.py tests/invalid/unknown_chars.drs --errors-only

# Ver solo tokens
python src/main.py tests/valid/complex.drs --tokens-only

# Modo verbose (información detallada)
python src/main.py tests/valid/complex.drs --verbose

# Guardar salida en archivo
python src/main.py tests/valid/simple.drs --output output/tokens.txt

# Combinaciones
python src/main.py tests/valid/complex.drs --format json --output output/tokens.json
```

### Ayuda de CLI

```bash
python src/main.py --help
```

## 📁 Estructura del Proyecto

```
DroneScript-Lexer/
├── 📄 README.md                          # Este archivo
├── 📄 requirements.txt                   # Dependencias (vacío, no se requieren)
├── 📄 .gitignore                         # Configuración Git
│
├── 📁 src/
│   ├── __init__.py                       # Inicialización del módulo
│   ├── tokens.py                         # Definición de TokenType y TokenCategory
│   ├── errors.py                         # Clases de error y recolector
│   ├── utils.py                          # Utilidades, mapeos, validadores
│   ├── lexer.py                          # Clase DroneLexer (motor principal)
│   └── main.py                           # Interfaz CLI (punto de entrada)
│
├── 📁 grammar/
│   ├── DroneScript.g4                    # Gramática ANTLR4 (especificación formal)
│   └── README.md                         # Documentación de la gramática
│
├── 📁 tests/
│   ├── valid/                            # Casos de prueba válidos
│   │   ├── simple.drs                    # Ejemplo mínimo
│   │   ├── movement.drs                  # Comandos de movimiento
│   │   ├── complex.drs                   # Ejemplo complejo
│   │   └── all_keywords.drs              # Todas las palabras clave
│   │
│   └── invalid/                          # Casos de prueba con errores
│       ├── unknown_chars.drs             # Caracteres desconocidos
│       ├── broken_strings.drs            # Strings no cerrados
│       ├── broken_comments.drs           # Comentarios no cerrados
│       └── mixed_errors.drs              # Múltiples errores
│
├── 📁 output/                            # Salida de tokens (generada)
│   └── tokens_output.txt
│
└── 📁 docs/                              # Documentación adicional (opcional)
```

## 🔍 Ejemplos de Uso

### Ejemplo 1: Análisis Simple

**Archivo: `test.drs`**
```dronescript
despegar;
mover norte 10;
aterrizar;
```

**Comando:**
```bash
python src/main.py test.drs
```

**Salida:**
```
TOKEN ANALYSIS REPORT
================================================================================
File: test.drs
Total tokens: 6
Status: ✓ OK (no errors)

TYPE      | LEXEME    | LINE | COL | CATEGORY
----------|-----------|------|-----|------------------
KEYWORD   | despegar  | 1    | 1   | CONTROL
DELIMITER | ;         | 1    | 9   | DELIMITER_PUNCTUATION
KEYWORD   | mover     | 2    | 1   | MOVEMENT
KEYWORD   | norte     | 2    | 7   | DIRECTION
NUMBER    | 10        | 2    | 13  | LITERAL_NUMBER
DELIMITER | ;         | 2    | 15  | DELIMITER_PUNCTUATION
KEYWORD   | aterrizar | 3    | 1   | CONTROL
DELIMITER | ;         | 3    | 10  | DELIMITER_PUNCTUATION
```

### Ejemplo 2: Manejo de Errores

**Archivo: `error.drs`**
```dronescript
despegar#;
nombre = "Mexico;
```

**Comando:**
```bash
python src/main.py error.drs
```

**Salida:**
```
TOKEN ANALYSIS REPORT
================================================================================
File: error.drs
Total tokens: 4
Status: ✗ ERRORS DETECTED

TYPE      | LEXEME    | LINE | COL | CATEGORY
----------|-----------|------|-----|------------------
KEYWORD   | despegar  | 1    | 1   | CONTROL
DELIMITER | ;         | 1    | 10  | DELIMITER_PUNCTUATION
IDENTIFIER| nombre    | 2    | 1   | LITERAL_IDENTIFIER
OPERATOR  | =         | 2    | 8   | OPERATOR_ASSIGNMENT

==================================================
LEXICAL ERRORS DETECTED (2)
==================================================

[ERROR 1] UNKNOWN_CHARACTER
Line 1, Column 9
Character: '#'
Message: Símbolo desconocido '#'

[ERROR 2] UNTERMINATED_STRING
Line 2, Column 11
Character: '"'
Message: String no cerrado (fin de archivo)
```

## 🏗️ Arquitectura y Modularidad

### Diseño Modular
El proyecto está dividido en **módulos independientes** que pueden reutilizarse sin acoplamiento:

```
tokens.py (TokenType, TokenCategory, Token)
    ↓
errors.py (ErrorType, LexerError, ErrorCollector) — utiliza tokens
    ↓
utils.py (mapeos, validadores) — usa tokens
    ↓
lexer.py (DroneLexer) — orquesta tokens, errors, utils
    ↓
main.py (CLI) — utiliza lexer
```

### Preparado para Futuras Fases

La arquitectura está diseñada para soportar extensiones futuras sin refactorización:

1. **Parser Sintáctico**: Consumirá `tokens` del lexer
2. **Análisis Semántico**: Usará categorías de tokens para tomar decisiones
3. **Constructor de AST**: Procesará información completa de cada token
4. **Transpilador a Python**: Recorrerá el AST y generará código Python

**Interfaz estable:**
```python
lexer = DroneLexer(source_code, filename)
tokens, errors = lexer.tokenize()

# El parser futuro hará:
parser = DroneParser(tokens)
ast = parser.parse()

# El transpilador futuro hará:
transpiler = DroneTranspiler(ast)
python_code = transpiler.transpile()
```

## 🧪 Pruebas

### Ejecutar Casos de Prueba Válidos

```bash
# Ejemplo simple
python src/main.py tests/valid/simple.drs

# Ejemplo con movimiento
python src/main.py tests/valid/movement.drs

# Ejemplo complejo
python src/main.py tests/valid/complex.drs

# Todas las palabras clave
python src/main.py tests/valid/all_keywords.drs
```

### Ejecutar Casos de Prueba Inválidos (con errores)

```bash
# Caracteres desconocidos
python src/main.py tests/invalid/unknown_chars.drs

# Strings no cerrados
python src/main.py tests/invalid/broken_strings.drs

# Comentarios no cerrados
python src/main.py tests/invalid/broken_comments.drs

# Múltiples errores
python src/main.py tests/invalid/mixed_errors.drs
```

### Verificación de Cobertura

Para verificar que el lexer funciona correctamente:

1. ✅ Todos los tokens válidos generan tokens correctos
2. ✅ Todos los errores léxicos se detectan y reportan
3. ✅ La información de línea/columna es precisa
4. ✅ Múltiples errores se acumulan correctamente
5. ✅ Los escapes en strings se procesan correctamente

## 📊 Especificación de Tokens

### Categorías de Tokens

| Categoría | Tipo Léxico | Ejemplos |
|-----------|------------|----------|
| CONTROL | KEYWORD | despegar, aterrizar |
| MOVEMENT | KEYWORD | mover, rotar |
| DIRECTION | KEYWORD | norte, sur |
| GPS | KEYWORD | coordenada, navegar |
| SENSOR | KEYWORD | escanear, lidar |
| CAMERA | KEYWORD | activar_camara, zoom |
| BATTERY | KEYWORD | bateria, cargar |
| CONDITIONAL | KEYWORD | si, mientras |
| COMMUNICATION | KEYWORD | conectar, wifi |
| SECURITY | KEYWORD | autenticar, bloquear |
| ENVIRONMENT | KEYWORD | viento, lluvia |
| AI | KEYWORD | modo_autonomo, explorar |
| DATA_TYPE | KEYWORD | entero, decimal |
| EVENT | KEYWORD | al_detectar, al_colisionar |
| OPERATOR_ARITHMETIC | OPERATOR | +, -, *, /, % |
| OPERATOR_COMPARISON | OPERATOR | <, >, <=, >=, ==, != |
| OPERATOR_LOGICAL | OPERATOR | &&, \|\|, ! |
| OPERATOR_ASSIGNMENT | OPERATOR | = |
| DELIMITER_PAREN | DELIMITER | (, ) |
| DELIMITER_BRACE | DELIMITER | {, } |
| DELIMITER_BRACKET | DELIMITER | [, ] |
| DELIMITER_PUNCTUATION | DELIMITER | ;, ,, : |
| LITERAL_NUMBER | NUMBER | 10, 999 |
| LITERAL_FLOAT | FLOAT | 3.14, 0.5 |
| LITERAL_STRING | STRING | "texto" |
| LITERAL_IDENTIFIER | IDENTIFIER | motor_1, _sensor |

### Palabras Clave por Categoría

**Total: 127 palabras clave reservadas**

- CONTROL (11): despegar, aterrizar, iniciar_mision, finalizar_mision, pausar_mision, reanudar_mision, regresar_base, apagar, reiniciar, detener, emergencia
- MOVEMENT (11): mover, avanzar, retroceder, subir, bajar, rotar, acelerar, frenar, mantener_altura, orbitar, seguir_objetivo
- DIRECTION (12): norte, sur, este, oeste, noreste, noroeste, sureste, suroeste, arriba, abajo, izquierda, derecha
- GPS (11): coordenada, gps, latitud, longitud, destino, ruta, waypoint, navegar, ir_a, guardar_ruta, cargar_ruta
- SENSOR (12): escanear, sensor_distancia, sensor_temperatura, sensor_humedad, sensor_gas, sensor_ultrasonico, sensor_proximidad, sensor_luz, lidar, camara_termica, giroscopio, acelerometro
- CAMERA (10): activar_camara, desactivar_camara, tomar_foto, grabar_video, detener_video, zoom, enfocar, reconocer_objeto, detectar_persona, seguir_movimiento
- BATTERY (6): bateria, energia, cargar, nivel_bateria, ahorro_energia, temperatura_motor
- CONDITIONAL (12): si, entonces, sino, fin, mientras, hacer, repetir, veces, para, desde, hasta, incrementar
- COMMUNICATION (9): conectar, desconectar, transmitir, recibir, enviar_datos, recibir_datos, wifi, bluetooth, radio
- SECURITY (7): autenticar, bloquear, desbloquear, activar_alarma, desactivar_alarma, zona_segura, evitar_colision
- ENVIRONMENT (6): viento, lluvia, temperatura, humedad, presion, detectar_obstaculo
- AI (8): modo_autonomo, aprendizaje, objetivo, patrullar, explorar, mapear, reconocer_rostro, evitar_obstaculo
- DATA_TYPE (6): entero, decimal, texto, booleano, verdadero, falso
- EVENT (6): al_detectar, al_colisionar, al_bateria_baja, al_perder_senal, al_iniciar, al_aterrizar

## 🔄 Flujo de Procesamiento

```
Código fuente (.drs)
        ↓
   [DroneLexer]
        ↓
   Análisis carácter a carácter
   - Reconoce tokens
   - Registra línea/columna
   - Acumula errores
        ↓
   [Tokenización]
        ↓
   Lista de Token objects + ErrorCollector
        ↓
   [Formateo]
        ↓
   Salida (Tabla / JSON / Simple)
```

## 🎓 Propósito Académico

Este proyecto fue desarrollado como **proyecto de laboratorio** para un curso de **Compiladores e Análisis Léxico** con los siguientes objetivos académicos:

1. ✅ Entender fases del proceso de compilación (léxica, sintáctica, semántica)
2. ✅ Implementar un analizador léxico completo desde cero
3. ✅ Comprender tokenización y reconocimiento de patrones
4. ✅ Manejar errores de forma robusta
5. ✅ Diseñar arquitecturas modulares y extensibles
6. ✅ Documentación profesional y buenas prácticas
7. ✅ Preparación para futuras fases (parser, AST, transpilador)

## 🛣️ Hoja de Ruta (Futuras Fases)

### Fase 2: Parser Sintáctico
- Análisis sintáctico usando tokens del lexer
- Construcción de árbol de derivación
- Detección de errores sintácticos
- Recuperación de errores sintácticos

### Fase 3: Análisis Semántico
- Validación de tipos
- Análisis de alcance (scope)
- Generación de código intermedio
- Tabla de símbolos

### Fase 4: Transpilador a Python
- Generación de código Python válido
- Mapeo de constructs de DroneScript a Python
- Optimizaciones básicas
- Validación del código generado

## 📝 Notas de Implementación

### Decisiones Técnicas

1. **Lexer Manual vs. ANTLR Compilado**
   - Decisión: Lexer manual en Python puro
   - Razón: Mayor control, mejor para aprendizaje académico
   - Futuro: Compatible con compilación ANTLR si es necesario

2. **Categorización de Tokens**
   - TokenType (general): KEYWORD, NUMBER, STRING, etc.
   - TokenCategory (semántica): CONTROL, MOVEMENT, DIRECTION, etc.
   - Beneficio: Información semántica explícita para parser/transpilador

3. **Recuperación de Errores**
   - Acumula múltiples errores sin detener en el primero
   - Usuario ve todos los problemas de una vez
   - Interfaz uniforme para manejo de errores

4. **Información de Token Completa**
   - Tipo, categoría, lexema, valor literal
   - Línea y columna precisas
   - Compatible con herramientas posteriores

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

Para más información, consulta el archivo [grammar/README.md](grammar/README.md) para detalles sobre la gramática ANTLR.
