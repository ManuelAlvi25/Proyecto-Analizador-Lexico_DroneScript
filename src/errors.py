"""
errors.py - Manejo de errores léxicos
Define tipos de error y clase para recolectar y reportar errores.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class ErrorType(Enum):
    """Tipos de errores léxicos posibles."""
    UNKNOWN_CHARACTER = auto()
    UNTERMINATED_STRING = auto()
    UNTERMINATED_COMMENT = auto()
    INVALID_ESCAPE_SEQUENCE = auto()
    INVALID_FLOAT_FORMAT = auto()


@dataclass
class LexerError:
    """
    Representa un error léxico encontrado durante el análisis.
    
    Atributos:
        error_type: ErrorType - tipo de error
        line: int - línea donde ocurrió
        column: int - columna donde ocurrió
        character: str - carácter/token problemático
        message: str - descripción del error
        context: str - línea de código con indicador
    """
    error_type: ErrorType
    line: int
    column: int
    character: str
    message: str
    context: str = ""
    
    def __str__(self) -> str:
        """Formato profesional del error."""
        result = f"\n[ERROR] {self.error_type.name}\n"
        result += f"Line {self.line}, Column {self.column}\n"
        result += f"Character: '{self.character}'\n"
        result += f"Message: {self.message}\n"
        if self.context:
            result += f"\nContext:\n{self.context}\n"
        return result


class ErrorCollector:
    """
    Recolecta y gestiona múltiples errores léxicos.
    Permite continuar análisis sin detener en primer error.
    """
    
    def __init__(self):
        """Inicializa recolector vacío."""
        self._errors: List[LexerError] = []
    
    def add_error(self, error_type: ErrorType, line: int, column: int,
                  character: str, message: str, context: str = "") -> None:
        """
        Agrega un error a la colección.
        
        Args:
            error_type: Tipo de error
            line: Línea del error
            column: Columna del error
            character: Carácter problemático
            message: Descripción del error
            context: Línea de código con contexto visual
        """
        error = LexerError(
            error_type=error_type,
            line=line,
            column=column,
            character=character,
            message=message,
            context=context
        )
        self._errors.append(error)
    
    def has_errors(self) -> bool:
        """Retorna True si hay errores acumulados."""
        return len(self._errors) > 0
    
    def get_all_errors(self) -> List[LexerError]:
        """Retorna lista de todos los errores."""
        return self._errors.copy()
    
    def get_error_count(self) -> int:
        """Retorna cantidad de errores."""
        return len(self._errors)
    
    def print_all_errors(self) -> None:
        """Imprime todos los errores en formato legible."""
        if not self.has_errors():
            return
        
        print("\n" + "="*50)
        print(f"LEXICAL ERRORS DETECTED ({self.get_error_count()})")
        print("="*50)
        
        for i, error in enumerate(self._errors, 1):
            print(f"\n[ERROR {i}] {error.error_type.name}")
            print(f"Line {error.line}, Column {error.column}")
            print(f"Character: '{error.character}'")
            print(f"Message: {error.message}")
            if error.context:
                print(f"\nContext:\n{error.context}")
