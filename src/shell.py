"""
Основной модуль эмулятора оболочки ОС.
Реализует REPL (Read-Eval-Print Loop) интерфейс.
"""
import getpass
import socket

from parser import parse_command
from commands import execute_command


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


def repl_loop() -> None:
    """
    Основной цикл REPL (Read-Eval-Print Loop).
    """
    prompt = get_default_prompt()

    while True:
        try:
            user_input = input(prompt)

            if not user_input.strip():
                continue

            command, args = parse_command(user_input)
            result = execute_command(command, args)

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
    repl_loop()


if __name__ == '__main__':
    main()