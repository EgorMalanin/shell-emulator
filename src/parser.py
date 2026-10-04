"""
Модуль для парсинга команд и раскрытия переменных окружения.
"""
import os
import re
import shlex
from typing import List, Tuple


def expand_variables(command: str) -> str:
    """
    Раскрывает переменные окружения в команде.
    """
    pattern_braces = r'\$\{([A-Za-z_][A-Za-z0-9_]*)\}'
    pattern_simple = r'\$([A-Za-z_][A-Za-z0-9_]*)'

    def replace_var(match):
        """Заменяет переменную на её значение из окружения."""
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
    try:
        tokens = shlex.split(expanded)
    except ValueError:
        tokens = expanded.split()

    if not tokens:
        return '', []

    command = tokens[0]
    args = tokens[1:]

    return command, args