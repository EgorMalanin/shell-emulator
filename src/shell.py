"""
Основной модуль эмулятора оболочки ОС.
Реализует REPL (Read-Eval-Print Loop) интерфейс.
"""
import getpass
import socket
from typing import Dict, Optional

from parser import parse_command
from commands import execute_command
from config import parse_arguments, print_debug_info


def get_default_prompt() -> str:
    """
    Формирует стандартное приглашение к вводу.

    Формат: username@hostname:~$

    Returns:
        Строка приглашения к вводу
    """
    username = getpass.getuser()
    hostname = socket.gethostname()
    return f"{username}@{hostname}:~$ "


def get_prompt(config: Dict[str, Optional[str]]) -> str:
    """
    Получает приглашение к вводу из конфигурации.

    Args:
        config: Словарь с параметрами конфигурации

    Returns:
        Строка приглашения к вводу
    """
    if config.get('prompt'):
        return config['prompt']
    return get_default_prompt()


def execute_script(
    script_path: str,
    prompt: str
) -> None:
    """
    Выполняет команды из стартового скрипта.

    Args:
        script_path: Путь к файлу скрипта
        prompt: Приглашение к вводу для отображения
    """
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                print(f"{prompt}{line}")

                cmd, args = parse_command(line)
                result = execute_command(cmd, args)

                print(result)

    except FileNotFoundError:
        print(f"Error: Script '{script_path}' not found")
    except IOError as e:
        print(f"Error reading script: {e}")


def repl_loop(config: Dict[str, Optional[str]]) -> None:
    """
    Основной цикл REPL (Read-Eval-Print Loop).

    Args:
        config: Словарь с параметрами конфигурации
    """
    prompt = get_prompt(config)

    while True:
        try:
            user_input = input(prompt)

            if not user_input.strip():
                continue

            cmd, args = parse_command(user_input)
            result = execute_command(cmd, args)

            if result == "__EXIT__":
                break

            print(result)

        except EOFError:
            break
        except KeyboardInterrupt:
            print()
            continue


def main() -> None:
    """
    Точка входа в приложение.
    """
    config = parse_arguments()
    print_debug_info(config)

    if config.get('script'):
        prompt = get_prompt(config)
        execute_script(config['script'], prompt)
    else:
        repl_loop(config)


if __name__ == '__main__':
    main()