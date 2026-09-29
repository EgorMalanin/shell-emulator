"""
Модуль с реализацией команд эмулятора оболочки.
"""
from typing import List


def cmd_ls(args: List[str]) -> str:
    """
    Команда ls (заглушка).
    """
    return f"Command 'ls' executed with args: {args}"


def cmd_cd(args: List[str]) -> str:
    """
    Команда cd (заглушка).
    """
    return f"Command 'cd' executed with args: {args}"


def cmd_exit(args: List[str]) -> str:
    """
    Команда exit для завершения работы эмулятора.
    """
    return "__EXIT__"


def execute_command(command: str, args: List[str]) -> str:
    """
    Выполняет команду и возвращает результат.
    """
    commands = {
        'ls': cmd_ls,
        'cd': cmd_cd,
        'exit': cmd_exit,
    }

    if command in commands:
        return commands[command](args)

    return f"Error: Unknown command '{command}'"