"""
lexer.py - Analizador Léxico Principal
Implementación del lexer manual en Python que tokeniza código DroneScript.
"""

from typing import Tuple, List
from src.tokens import Token, TokenType, TokenCategory
from src.errors import ErrorCollector, ErrorType
from src import utils


class DroneLexer:
    """
    Analizador léxico para el lenguaje DroneScript.
    Convierte texto fuente en una lista de tokens.
    """
    
    def __init__(self, source: str, filename: str = "<stdin>"):
        """
        Inicializa el lexer.
        
        Args:
            source: Código fuente a analizar
            filename: Nombre del archivo (para reportes)
        """
        self._input = source
        self._filename = filename
        self._position = 0
        self._line = 1
        self._column = 1
        self._tokens: List[Token] = []
        self._errors = ErrorCollector()
        self._line_starts: List[int] = [0]  # Índices de inicio de línea
    
    # ===== MÉTODOS PRINCIPALES =====
    
    def tokenize(self) -> Tuple[List[Token], ErrorCollector]:
        """
        Ejecuta el análisis léxico completo.
        
        Returns:
            Tupla (lista de tokens, recolector de errores)
        """
        while not self._at_end():
            # Intentar reconocer siguiente token
            if not self._scan_token():
                # Carácter desconocido
                self._report_unknown_character()
        
        return self._tokens, self._errors
    
    # ===== MÉTODOS DE LECTURA =====
    
    def _peek(self, offset: int = 0) -> str:
        """Mira carácter sin consumir."""
        pos = self._position + offset
        if pos >= len(self._input):
            return '\0'
        return self._input[pos]
    
    def _advance(self) -> str:
        """Consume y retorna carácter, actualiza línea/columna."""
        if self._at_end():
            return '\0'
        
        ch = self._input[self._position]
        self._position += 1
        
        if ch == '\n':
            self._line += 1
            self._column = 1
            self._line_starts.append(self._position)
        else:
            self._column += 1
        
        return ch
    
    def _match(self, expected: str) -> bool:
        """Consume carácter si coincide con expected."""
        if self._peek() == expected:
            self._advance()
            return True
        return False
    
    def _at_end(self) -> bool:
        """Verifica si se llegó al final de entrada."""
        return self._position >= len(self._input)
    
    # ===== MÉTODOS DE ESCANEO DE TOKENS =====
    
    def _scan_token(self) -> bool:
        """
        Intenta reconocer el siguiente token.
        Retorna True si reconoció algo, False si carácter desconocido.
        """
        ch = self._peek()
        
        # Espacios en blanco
        if ch.isspace():
            self._skip_whitespace()
            return True
        
        # Comentarios
        if ch == '/' and self._peek(1) == '/':
            self._skip_line_comment()
            return True
        
        if ch == '/' and self._peek(1) == '*':
            self._skip_block_comment()
            return True
        
        # Strings
        if ch == '"':
            self._scan_string()
            return True
        
        # Números
        if ch.isdigit():
            self._scan_number()
            return True
        
        # Identificadores y palabras clave
        if ch.isalpha() or ch == '_':
            self._scan_keyword_or_identifier()
            return True
        
        # Operadores
        if utils.is_operator(ch):
            self._scan_operator()
            return True
        
        # Delimitadores
        if utils.is_delimiter(ch):
            self._scan_delimiter()
            return True
        
        # Carácter desconocido
        return False
    
    def _skip_whitespace(self) -> None:
        """Salta espacios en blanco."""
        while not self._at_end() and self._peek().isspace():
            self._advance()
    
    def _skip_line_comment(self) -> None:
        """Salta comentario de línea (// ... \\n)."""
        self._advance()  # primer /
        self._advance()  # segundo /
        while not self._at_end() and self._peek() != '\n':
            self._advance()
        if not self._at_end():
            self._advance()  # consumir \n
    
    def _skip_block_comment(self) -> None:
        """Salta comentario de bloque (/* ... */)."""
        start_line = self._line
        start_col = self._column
        
        self._advance()  # /
        self._advance()  # *
        
        while not self._at_end():
            if self._peek() == '*' and self._peek(1) == '/':
                self._advance()  # *
                self._advance()  # /
                return
            self._advance()
        
        # Comentario no cerrado
        self._errors.add_error(
            ErrorType.UNTERMINATED_COMMENT,
            start_line,
            start_col,
            '/*',
            'Comentario de bloque no cerrado'
        )
    
    def _scan_string(self) -> None:
        """Escanea string con comillas dobles."""
        start_line = self._line
        start_col = self._column
        self._advance()  # consumir "
        
        value = []
        
        while not self._at_end() and self._peek() != '"':
            if self._peek() == '\n':
                # String no cerrado en la línea
                self._errors.add_error(
                    ErrorType.UNTERMINATED_STRING,
                    start_line,
                    start_col,
                    '"',
                    'String no cerrado (newline encontrado)'
                )
                return
            
            if self._peek() == '\\':
                self._advance()
                if self._at_end():
                    self._errors.add_error(
                        ErrorType.UNTERMINATED_STRING,
                        start_line,
                        start_col,
                        '"',
                        'String no cerrado (fin de archivo)'
                    )
                    return
                value.append(self._advance())
            else:
                value.append(self._advance())
        
        if self._at_end():
            # String no cerrado al fin de archivo
            self._errors.add_error(
                ErrorType.UNTERMINATED_STRING,
                start_line,
                start_col,
                '"',
                'String no cerrado (fin de archivo)'
            )
            return
        
        self._advance()  # consumir cierre "
        
        # Procesar escapes
        raw_string = ''.join(value)
        processed, is_valid = utils.process_escape_sequences(raw_string)
        
        if not is_valid:
            self._errors.add_error(
                ErrorType.INVALID_ESCAPE_SEQUENCE,
                start_line,
                start_col,
                '"',
                f'Secuencia de escape inválida en string'
            )
        
        self._add_token(
            TokenType.STRING,
            TokenCategory.LITERAL_STRING,
            f'"{raw_string}"',
            processed
        )
    
    def _scan_number(self) -> None:
        """Escanea números enteros y flotantes."""
        start_col = self._column
        value = []
        
        # Escanear parte entera
        while not self._at_end() and self._peek().isdigit():
            value.append(self._advance())
        
        # Verificar punto decimal
        if not self._at_end() and self._peek() == '.' and self._peek(1).isdigit():
            value.append(self._advance())  # punto
            while not self._at_end() and self._peek().isdigit():
                value.append(self._advance())
            
            number_str = ''.join(value)
            self._add_token(
                TokenType.FLOAT,
                TokenCategory.LITERAL_FLOAT,
                number_str,
                float(number_str)
            )
        else:
            number_str = ''.join(value)
            self._add_token(
                TokenType.NUMBER,
                TokenCategory.LITERAL_NUMBER,
                number_str,
                int(number_str)
            )
    
    def _scan_keyword_or_identifier(self) -> None:
        """Escanea palabras clave e identificadores."""
        value = []
        
        while not self._at_end() and (self._peek().isalnum() or self._peek() == '_'):
            value.append(self._advance())
        
        word = ''.join(value)
        
        # Verificar si es palabra clave
        category = utils.get_keyword_category(word)
        if category:
            self._add_token(TokenType.KEYWORD, category, word)
        else:
            # Es identificador
            self._add_token(
                TokenType.IDENTIFIER,
                TokenCategory.LITERAL_IDENTIFIER,
                word
            )
    
    def _scan_operator(self) -> None:
        """Escanea operadores (simples y multi-carácter)."""
        # Intentar operadores de 2 caracteres primero
        two_char = self._peek() + self._peek(1)
        if two_char in utils.MULTICHAR_OPERATORS:
            self._advance()
            self._advance()
            category = utils.get_operator_category(two_char)
            self._add_token(TokenType.OPERATOR, category, two_char)
        else:
            # Operador de 1 carácter
            ch = self._advance()
            category = utils.get_operator_category(ch)
            self._add_token(TokenType.OPERATOR, category, ch)
    
    def _scan_delimiter(self) -> None:
        """Escanea delimitadores."""
        ch = self._advance()
        category = utils.get_delimiter_category(ch)
        self._add_token(TokenType.DELIMITER, category, ch)
    
    # ===== MÉTODOS AUXILIARES =====
    
    def _add_token(self, token_type: TokenType, category: TokenCategory,
                   lexeme: str, literal_value=None) -> None:
        """Agrega un token a la lista."""
        token = Token(
            type=token_type,
            category=category,
            lexeme=lexeme,
            literal_value=literal_value,
            line=self._line,
            column=self._column - len(lexeme)
        )
        self._tokens.append(token)
    
    def _report_unknown_character(self) -> None:
        """Reporta carácter desconocido como error."""
        ch = self._advance()
        self._errors.add_error(
            ErrorType.UNKNOWN_CHARACTER,
            self._line,
            self._column - 1,
            ch,
            f"Símbolo desconocido '{ch}'"
        )
    
    def _get_line_content(self, line_num: int) -> str:
        """Obtiene el contenido de una línea específica."""
        if line_num < 1 or line_num - 1 >= len(self._line_starts):
            return ""
        
        start = self._line_starts[line_num - 1]
        end = self._line_starts[line_num] if line_num < len(self._line_starts) else len(self._input)
        
        return self._input[start:end].rstrip('\n')
    
    # ===== MÉTODOS DE ACCESO A RESULTADOS =====
    
    def get_tokens(self) -> List[Token]:
        """Retorna la lista de tokens."""
        return self._tokens.copy()
    
    def get_errors(self) -> ErrorCollector:
        """Retorna el recolector de errores."""
        return self._errors
    
    def has_errors(self) -> bool:
        """Retorna True si hay errores."""
        return self._errors.has_errors()
