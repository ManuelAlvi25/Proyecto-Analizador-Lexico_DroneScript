"""
tokens.py - Definición de tipos y categorías de tokens
Define TokenType (tipo léxico general) y TokenCategory (categoría semántica)
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, Any


class TokenType(Enum):
    """
    Tipo léxico general del token.
    Clasificación amplia según naturaleza del token.
    """
    # Palabras clave
    KEYWORD = auto()
    
    # Literales
    NUMBER = auto()
    FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Operadores
    OPERATOR = auto()
    
    # Delimitadores
    DELIMITER = auto()
    
    # Especiales
    EOF = auto()
    UNKNOWN = auto()


class TokenCategory(Enum):
    """
    Categoría semántica del token.
    Clasificación específica que indica el rol del token en el lenguaje.
    """
    # Control general
    CONTROL = auto()
    
    # Movimiento
    MOVEMENT = auto()
    
    # Direcciones
    DIRECTION = auto()
    
    # GPS y navegación
    GPS = auto()
    
    # Sensores
    SENSOR = auto()
    
    # Cámara y visión
    CAMERA = auto()
    
    # Batería y energía
    BATTERY = auto()
    
    # Condicionales y ciclos
    CONDITIONAL = auto()
    
    # Comunicación
    COMMUNICATION = auto()
    
    # Seguridad
    SECURITY = auto()
    
    # Clima y entorno
    ENVIRONMENT = auto()
    
    # IA y autonomía
    AI = auto()
    
    # Tipos de datos
    DATA_TYPE = auto()
    
    # Eventos automáticos
    EVENT = auto()
    
    # Operadores
    OPERATOR_ARITHMETIC = auto()
    OPERATOR_COMPARISON = auto()
    OPERATOR_LOGICAL = auto()
    OPERATOR_ASSIGNMENT = auto()
    
    # Delimitadores
    DELIMITER_PAREN = auto()      # ( )
    DELIMITER_BRACE = auto()      # { }
    DELIMITER_BRACKET = auto()    # [ ]
    DELIMITER_PUNCTUATION = auto() # ; , :
    
    # Literales
    LITERAL_IDENTIFIER = auto()
    LITERAL_NUMBER = auto()
    LITERAL_FLOAT = auto()
    LITERAL_STRING = auto()
    
    # Otros
    UNKNOWN = auto()


@dataclass
class Token:
    """
    Representa un token reconocido por el lexer.
    
    Atributos:
        type: TokenType - tipo léxico general (KEYWORD, NUMBER, etc.)
        category: TokenCategory - categoría semántica
        lexeme: str - texto exacto del token en el código fuente
        literal_value: Optional[Any] - valor procesado (para strings/números)
        line: int - número de línea (1-based)
        column: int - número de columna (1-based)
    """
    type: TokenType
    category: TokenCategory
    lexeme: str
    literal_value: Optional[Any] = None
    line: int = 1
    column: int = 1
    
    def __repr__(self) -> str:
        """Representación legible del token."""
        return f"Token({self.type.name}, {self.category.name}, '{self.lexeme}')"
    
    def to_dict(self) -> dict:
        """Convierte el token a diccionario."""
        return {
            'type': self.type.name,
            'category': self.category.name,
            'lexeme': self.lexeme,
            'literal_value': str(self.literal_value) if self.literal_value is not None else None,
            'line': self.line,
            'column': self.column
        }
    
    def to_simple_string(self) -> str:
        """Formato simple: (TYPE, lexeme)"""
        return f"({self.type.name}, {self.lexeme})"
