"""
Модуль для парсинга команд и раскрытия переменных окружения.
"""
import os
import re
from typing import List, Tuple


def expand_variables(command: str) -> str:
    """
    Раскрывает переменные окружения в команде.
    """
    pattern_braces = r'\$\{([A-Za-z_][A-Za-z0-9_]*)\}'
    pattern_simple = r'\$([A-Za-z_][A-Za-z0-9_]*)'

    def replace_var(match):
        """Заменяет переменную на её значение."""
        var_name = match.group(1)
        return os.environ.get(var_name, '')

    result = re.sub(pattern_braces, replace_var, command)
    result = re.sub(pattern_simple, replace_var, result)

    return result


def parse_command(command_line: str) -> Tuple[str, List[str]]:
    """
    Парсит строку команды на команду и аргументы.
    """
    expanded = expand_variables(command_line)

    tokens = []
    current_token = ''
    in_quotes = False
    quote_char = None

    for char in expanded:
        if char in ('"', "'") and not in_quotes:
            in_quotes = True
            quote_char = char
        elif char == quote_char and in_quotes:
            in_quotes = False
            quote_char = None
        elif char == ' ' and not in_quotes:
            if current_token:
                tokens.append(current_token)
                current_token = ''
        else:
            current_token += char

    if current_token:
        tokens.append(current_token)

    if not tokens:
        return '', []

    command = tokens[0]
    args = tokens[1:]

    return command, args