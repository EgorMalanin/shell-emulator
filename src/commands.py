"""
Модуль с реализацией команд эмулятора оболочки.
"""
from typing import List


def cmd_ls(args: List[str]) -> str:
    """
    Команда ls (заглушка).

    Args:
        args: Список аргументов команды

    Returns:
        Строка с результатом выполнения
    """
    return f"Command 'ls' executed with args: {args}"


def cmd_cd(args: List[str]) -> str:
    """
    Команда cd (заглушка).

    Args:
        args: Список аргументов команды

    Returns:
        Строка с результатом выполнения
    """
    return f"Command 'cd' executed with args: {args}"


def cmd_exit(args: List[str]) -> str:
    """
    Команда exit для завершения работы эмулятора.

    Args:
        args: Список аргументов команды (игнорируются)

    Returns:
        Специальная строка-сигнал для завершения
    """
    return "__EXIT__"


def execute_command(command: str, args: List[str]) -> str:
    """
    Выполняет команду и возвращает результат.

    Args:
        command: Имя команды
        args: Список аргументов

    Returns:
        Результат выполнения команды или сообщение об ошибке
    """
    commands = {
        'ls': cmd_ls,
        'cd': cmd_cd,
        'exit': cmd_exit,
    }

    if command in commands:
        return commands[command](args)

    return f"Error: Unknown command '{command}'"