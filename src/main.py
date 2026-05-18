"""
main.py - Interfaz CLI del Lexer DroneScript
Punto de entrada principal del proyecto.
"""

import sys
import argparse
import json
from pathlib import Path
from typing import Optional
from src.lexer import DroneLexer
from src.tokens import Token, TokenType, TokenCategory


def format_output_table(tokens: list, filename: str, has_errors: bool) -> str:
    """Formatea la salida como tabla ASCII."""
    result = []
    result.append("\n" + "="*80)
    result.append("TOKEN ANALYSIS REPORT")
    result.append("="*80)
    result.append(f"File: {filename}")
    result.append(f"Total tokens: {len(tokens)}")
    
    status = "✓ OK (no errors)" if not has_errors else "✗ ERRORS DETECTED"
    result.append(f"Status: {status}\n")
    
    if not tokens:
        result.append("(no tokens)")
        return "\n".join(result)
    
    # Encabezados
    headers = ["TYPE", "LEXEME", "LINE", "COL", "CATEGORY"]
    widths = [12, 20, 6, 5, 20]
    
    header_line = " | ".join(
        headers[i].ljust(widths[i]) for i in range(len(headers))
    )
    result.append(header_line)
    result.append("-" * 80)
    
    # Filas
    for token in tokens:
        type_str = token.type.name
        lexeme_str = token.lexeme[:18].replace('\n', '\\n').replace('\t', '\\t')
        line_str = str(token.line)
        col_str = str(token.column)
        category_str = token.category.name
        
        row = " | ".join([
            type_str.ljust(widths[0]),
            lexeme_str.ljust(widths[1]),
            line_str.ljust(widths[2]),
            col_str.ljust(widths[3]),
            category_str.ljust(widths[4])
        ])
        result.append(row)
    
    return "\n".join(result)


def format_output_json(tokens: list, filename: str, errors) -> str:
    """Formatea la salida como JSON."""
    data = {
        'file': filename,
        'status': 'success' if not errors.has_errors() else 'error',
        'tokens': [token.to_dict() for token in tokens],
        'error_count': errors.get_error_count(),
        'errors': [
            {
                'type': error.error_type.name,
                'line': error.line,
                'column': error.column,
                'character': error.character,
                'message': error.message
            }
            for error in errors.get_all_errors()
        ]
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def format_output_simple(tokens: list) -> str:
    """Formatea la salida como lista simple (TYPE, lexeme)."""
    return "\n".join(token.to_simple_string() for token in tokens)


def main() -> int:
    """Función principal de la CLI."""
    parser = argparse.ArgumentParser(
        description='DroneScript Lexer - Analizador Léxico para Lenguaje DroneScript',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python -m src.main tests/valid/simple.drs
  python -m src.main tests/valid/simple.drs --format json
  python -m src.main tests/invalid/broken_strings.drs --verbose
  python -m src.main tests/valid/simple.drs --output output/tokens.txt
        """
    )
    
    parser.add_argument(
        'file',
        help='Archivo .drs a analizar'
    )
    parser.add_argument(
        '--format',
        choices=['table', 'json', 'simple'],
        default='table',
        help='Formato de salida (default: table)'
    )
    parser.add_argument(
        '--output',
        help='Guardar salida en archivo'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Mostrar información detallada (incluye contexto de errores)'
    )
    parser.add_argument(
        '--errors-only',
        action='store_true',
        help='Mostrar solo errores'
    )
    parser.add_argument(
        '--tokens-only',
        action='store_true',
        help='Mostrar solo tokens (ignorar errores)'
    )
    
    args = parser.parse_args()
    
    # Validar archivo
    filepath = Path(args.file)
    
    if not filepath.exists():
        print(f"Error: Archivo no encontrado: {args.file}", file=sys.stderr)
        return 1
    
    if filepath.suffix != '.drs':
        print(f"Error: Extensión inválida. Se espera .drs, se encontró {filepath.suffix}", file=sys.stderr)
        return 1
    
    # Leer archivo
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
    except Exception as e:
        print(f"Error al leer archivo: {e}", file=sys.stderr)
        return 1
    
    # Ejecutar lexer
    lexer = DroneLexer(source, str(filepath))
    tokens, errors = lexer.tokenize()
    
    # Formatear salida
    if args.format == 'json':
        output = format_output_json(tokens, str(filepath), errors)
    elif args.format == 'simple':
        output = format_output_simple(tokens)
    else:  # table
        output = format_output_table(tokens, str(filepath), errors.has_errors())
    
    # Aplicar filtros
    if args.errors_only:
        if errors.has_errors():
            errors.print_all_errors()
        else:
            print("No errors found.")
    elif args.tokens_only:
        print(output)
    else:
        print(output)
        
        # Mostrar errores si los hay
        if errors.has_errors():
            errors.print_all_errors()
        if args.verbose and tokens:
            print(f"\n(Total: {len(tokens)} tokens, {errors.get_error_count()} errors)")
    
    # Guardar en archivo si se especifica
    if args.output:
        try:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output)
                if errors.has_errors():
                    f.write("\n\n")
                    for error in errors.get_all_errors():
                        f.write(str(error))
            print(f"\nSalida guardada en: {args.output}")
        except Exception as e:
            print(f"Error al guardar archivo: {e}", file=sys.stderr)
            return 1
    
    # Código de salida
    return 1 if errors.has_errors() else 0


if __name__ == '__main__':
    sys.exit(main())
