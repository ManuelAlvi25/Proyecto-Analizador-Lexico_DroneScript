"""
utils.py - Utilidades y validadores para el lexer
Contiene mapeos de palabras clave, operadores, funciones de validación.
"""

import re
from typing import Dict, Set, Tuple, Optional
from src.tokens import TokenType, TokenCategory


# ===== PALABRAS CLAVE RESERVADAS POR CATEGORÍA =====

CONTROL_KEYWORDS = {
    'despegar': TokenCategory.CONTROL,
    'aterrizar': TokenCategory.CONTROL,
    'iniciar_mision': TokenCategory.CONTROL,
    'finalizar_mision': TokenCategory.CONTROL,
    'pausar_mision': TokenCategory.CONTROL,
    'reanudar_mision': TokenCategory.CONTROL,
    'regresar_base': TokenCategory.CONTROL,
    'apagar': TokenCategory.CONTROL,
    'reiniciar': TokenCategory.CONTROL,
    'detener': TokenCategory.CONTROL,
    'emergencia': TokenCategory.CONTROL,
}

MOVEMENT_KEYWORDS = {
    'mover': TokenCategory.MOVEMENT,
    'avanzar': TokenCategory.MOVEMENT,
    'retroceder': TokenCategory.MOVEMENT,
    'subir': TokenCategory.MOVEMENT,
    'bajar': TokenCategory.MOVEMENT,
    'rotar': TokenCategory.MOVEMENT,
    'acelerar': TokenCategory.MOVEMENT,
    'frenar': TokenCategory.MOVEMENT,
    'mantener_altura': TokenCategory.MOVEMENT,
    'orbitar': TokenCategory.MOVEMENT,
    'seguir_objetivo': TokenCategory.MOVEMENT,
}

DIRECTION_KEYWORDS = {
    'norte': TokenCategory.DIRECTION,
    'sur': TokenCategory.DIRECTION,
    'este': TokenCategory.DIRECTION,
    'oeste': TokenCategory.DIRECTION,
    'noreste': TokenCategory.DIRECTION,
    'noroeste': TokenCategory.DIRECTION,
    'sureste': TokenCategory.DIRECTION,
    'suroeste': TokenCategory.DIRECTION,
    'arriba': TokenCategory.DIRECTION,
    'abajo': TokenCategory.DIRECTION,
    'izquierda': TokenCategory.DIRECTION,
    'derecha': TokenCategory.DIRECTION,
}

GPS_KEYWORDS = {
    'coordenada': TokenCategory.GPS,
    'gps': TokenCategory.GPS,
    'latitud': TokenCategory.GPS,
    'longitud': TokenCategory.GPS,
    'destino': TokenCategory.GPS,
    'ruta': TokenCategory.GPS,
    'waypoint': TokenCategory.GPS,
    'navegar': TokenCategory.GPS,
    'ir_a': TokenCategory.GPS,
    'guardar_ruta': TokenCategory.GPS,
    'cargar_ruta': TokenCategory.GPS,
}

SENSOR_KEYWORDS = {
    'escanear': TokenCategory.SENSOR,
    'sensor_distancia': TokenCategory.SENSOR,
    'sensor_temperatura': TokenCategory.SENSOR,
    'sensor_humedad': TokenCategory.SENSOR,
    'sensor_gas': TokenCategory.SENSOR,
    'sensor_ultrasonico': TokenCategory.SENSOR,
    'sensor_proximidad': TokenCategory.SENSOR,
    'sensor_luz': TokenCategory.SENSOR,
    'lidar': TokenCategory.SENSOR,
    'camara_termica': TokenCategory.SENSOR,
    'giroscopio': TokenCategory.SENSOR,
    'acelerometro': TokenCategory.SENSOR,
}

CAMERA_KEYWORDS = {
    'activar_camara': TokenCategory.CAMERA,
    'desactivar_camara': TokenCategory.CAMERA,
    'tomar_foto': TokenCategory.CAMERA,
    'grabar_video': TokenCategory.CAMERA,
    'detener_video': TokenCategory.CAMERA,
    'zoom': TokenCategory.CAMERA,
    'enfocar': TokenCategory.CAMERA,
    'reconocer_objeto': TokenCategory.CAMERA,
    'detectar_persona': TokenCategory.CAMERA,
    'seguir_movimiento': TokenCategory.CAMERA,
}

BATTERY_KEYWORDS = {
    'bateria': TokenCategory.BATTERY,
    'energia': TokenCategory.BATTERY,
    'cargar': TokenCategory.BATTERY,
    'nivel_bateria': TokenCategory.BATTERY,
    'ahorro_energia': TokenCategory.BATTERY,
    'temperatura_motor': TokenCategory.BATTERY,
}

CONDITIONAL_KEYWORDS = {
    'si': TokenCategory.CONDITIONAL,
    'entonces': TokenCategory.CONDITIONAL,
    'sino': TokenCategory.CONDITIONAL,
    'fin': TokenCategory.CONDITIONAL,
    'mientras': TokenCategory.CONDITIONAL,
    'hacer': TokenCategory.CONDITIONAL,
    'repetir': TokenCategory.CONDITIONAL,
    'veces': TokenCategory.CONDITIONAL,
    'para': TokenCategory.CONDITIONAL,
    'desde': TokenCategory.CONDITIONAL,
    'hasta': TokenCategory.CONDITIONAL,
    'incrementar': TokenCategory.CONDITIONAL,
}

COMMUNICATION_KEYWORDS = {
    'conectar': TokenCategory.COMMUNICATION,
    'desconectar': TokenCategory.COMMUNICATION,
    'transmitir': TokenCategory.COMMUNICATION,
    'recibir': TokenCategory.COMMUNICATION,
    'enviar_datos': TokenCategory.COMMUNICATION,
    'recibir_datos': TokenCategory.COMMUNICATION,
    'wifi': TokenCategory.COMMUNICATION,
    'bluetooth': TokenCategory.COMMUNICATION,
    'radio': TokenCategory.COMMUNICATION,
}

SECURITY_KEYWORDS = {
    'autenticar': TokenCategory.SECURITY,
    'bloquear': TokenCategory.SECURITY,
    'desbloquear': TokenCategory.SECURITY,
    'activar_alarma': TokenCategory.SECURITY,
    'desactivar_alarma': TokenCategory.SECURITY,
    'zona_segura': TokenCategory.SECURITY,
    'evitar_colision': TokenCategory.SECURITY,
}

ENVIRONMENT_KEYWORDS = {
    'viento': TokenCategory.ENVIRONMENT,
    'lluvia': TokenCategory.ENVIRONMENT,
    'temperatura': TokenCategory.ENVIRONMENT,
    'humedad': TokenCategory.ENVIRONMENT,
    'presion': TokenCategory.ENVIRONMENT,
    'detectar_obstaculo': TokenCategory.ENVIRONMENT,
}

AI_KEYWORDS = {
    'modo_autonomo': TokenCategory.AI,
    'aprendizaje': TokenCategory.AI,
    'objetivo': TokenCategory.AI,
    'patrullar': TokenCategory.AI,
    'explorar': TokenCategory.AI,
    'mapear': TokenCategory.AI,
    'reconocer_rostro': TokenCategory.AI,
    'evitar_obstaculo': TokenCategory.AI,
}

DATA_TYPE_KEYWORDS = {
    'entero': TokenCategory.DATA_TYPE,
    'decimal': TokenCategory.DATA_TYPE,
    'texto': TokenCategory.DATA_TYPE,
    'booleano': TokenCategory.DATA_TYPE,
    'verdadero': TokenCategory.DATA_TYPE,
    'falso': TokenCategory.DATA_TYPE,
}

EVENT_KEYWORDS = {
    'al_detectar': TokenCategory.EVENT,
    'al_colisionar': TokenCategory.EVENT,
    'al_bateria_baja': TokenCategory.EVENT,
    'al_perder_senal': TokenCategory.EVENT,
    'al_iniciar': TokenCategory.EVENT,
    'al_aterrizar': TokenCategory.EVENT,
}

# Consolidar todas las palabras clave
KEYWORDS_MAP: Dict[str, TokenCategory] = {
    **CONTROL_KEYWORDS,
    **MOVEMENT_KEYWORDS,
    **DIRECTION_KEYWORDS,
    **GPS_KEYWORDS,
    **SENSOR_KEYWORDS,
    **CAMERA_KEYWORDS,
    **BATTERY_KEYWORDS,
    **CONDITIONAL_KEYWORDS,
    **COMMUNICATION_KEYWORDS,
    **SECURITY_KEYWORDS,
    **ENVIRONMENT_KEYWORDS,
    **AI_KEYWORDS,
    **DATA_TYPE_KEYWORDS,
    **EVENT_KEYWORDS,
}

RESERVED_WORDS: Set[str] = set(KEYWORDS_MAP.keys())


# ===== OPERADORES =====

OPERATORS = {
    # Operadores aritméticos
    '+': TokenCategory.OPERATOR_ARITHMETIC,
    '-': TokenCategory.OPERATOR_ARITHMETIC,
    '*': TokenCategory.OPERATOR_ARITHMETIC,
    '/': TokenCategory.OPERATOR_ARITHMETIC,
    '%': TokenCategory.OPERATOR_ARITHMETIC,
    
    # Operadores de comparación
    '<': TokenCategory.OPERATOR_COMPARISON,
    '>': TokenCategory.OPERATOR_COMPARISON,
    '<=': TokenCategory.OPERATOR_COMPARISON,
    '>=': TokenCategory.OPERATOR_COMPARISON,
    '==': TokenCategory.OPERATOR_COMPARISON,
    '!=': TokenCategory.OPERATOR_COMPARISON,
    
    # Operadores lógicos
    '&&': TokenCategory.OPERATOR_LOGICAL,
    '||': TokenCategory.OPERATOR_LOGICAL,
    '!': TokenCategory.OPERATOR_LOGICAL,
    
    # Operador de asignación
    '=': TokenCategory.OPERATOR_ASSIGNMENT,
}

# Operadores multi-carácter (ordenados por longitud descendente)
MULTICHAR_OPERATORS = ['<=', '>=', '==', '!=', '&&', '||']


# ===== DELIMITADORES =====

DELIMITERS = {
    '(': TokenCategory.DELIMITER_PAREN,
    ')': TokenCategory.DELIMITER_PAREN,
    '{': TokenCategory.DELIMITER_BRACE,
    '}': TokenCategory.DELIMITER_BRACE,
    '[': TokenCategory.DELIMITER_BRACKET,
    ']': TokenCategory.DELIMITER_BRACKET,
    ';': TokenCategory.DELIMITER_PUNCTUATION,
    ',': TokenCategory.DELIMITER_PUNCTUATION,
    ':': TokenCategory.DELIMITER_PUNCTUATION,
}


# ===== FUNCIONES DE VALIDACIÓN =====

def is_valid_identifier(name: str) -> bool:
    """
    Valida si una cadena es un identificador válido.
    Regla: Comienza con letra o _, seguido de letras, dígitos o _.
    """
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, name))


def is_integer(value: str) -> bool:
    """Valida si una cadena es un número entero válido."""
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_float(value: str) -> bool:
    """Valida si una cadena es un número flotante válido."""
    try:
        float(value)
        return '.' in value
    except ValueError:
        return False


def process_escape_sequences(s: str) -> Tuple[str, bool]:
    """
    Procesa secuencias de escape en strings.
    Retorna (cadena_procesada, es_valida)
    """
    escape_map = {
        'n': '\n',
        't': '\t',
        'r': '\r',
        '"': '"',
        '\\': '\\',
    }
    
    result = []
    i = 0
    valid = True
    
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            next_char = s[i + 1]
            if next_char in escape_map:
                result.append(escape_map[next_char])
                i += 2
            else:
                # Secuencia inválida
                valid = False
                result.append(s[i])
                i += 1
        else:
            result.append(s[i])
            i += 1
    
    return ''.join(result), valid


def get_keyword_category(word: str) -> Optional[TokenCategory]:
    """Obtiene la categoría de una palabra clave, None si no es reservada."""
    return KEYWORDS_MAP.get(word.lower())


def is_keyword(word: str) -> bool:
    """Verifica si una palabra es palabra reservada."""
    return word.lower() in RESERVED_WORDS


def get_operator_category(op: str) -> Optional[TokenCategory]:
    """Obtiene la categoría de un operador, None si no existe."""
    return OPERATORS.get(op)


def is_operator(char: str) -> bool:
    """Verifica si un carácter es operador."""
    return char in OPERATORS


def get_delimiter_category(char: str) -> Optional[TokenCategory]:
    """Obtiene la categoría de un delimitador, None si no existe."""
    return DELIMITERS.get(char)


def is_delimiter(char: str) -> bool:
    """Verifica si un carácter es delimitador."""
    return char in DELIMITERS
