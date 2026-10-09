"""
Основной модуль эмулятора оболочки ОС.
Реализует интерфейс REPL (Read-Eval-Print Loop).
"""
import getpass
import socket
from typing import Dict, Optional

from parser import parse_command
from commands import execute_command
from config import parse_arguments, print_debug_info
from vfs import VirtualFileSystem


def get_default_prompt() -> str:
    """
    Формирует стандартное приглашение к вводу.
    """
    username = getpass.getuser()
    hostname = socket.gethostname()
    return f"{username}@{hostname}:~$ "


def get_prompt(config:Dict[str,Optional[str]],vfs:VirtualFileSystem)->str:
    """
    Получает приглашение к вводу из конфига или стандартное..
    """
    if config.get('prompt'):
        return config['prompt']
    return get_default_prompt()


def execute_script(script_path:str,prompt:str,vfs:VirtualFileSystem)->None:
    """
    Выполняет команды из стартового скрипта.
    """
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                vfs.history.append(line)
                print(f"{prompt}{line}")

                cmd, args = parse_command(line)
                result = execute_command(cmd, args, vfs)

                if result == "__EXIT__":
                    break
                if result:
                    print(result)

    except FileNotFoundError:
        print(f"Error: Script '{script_path}' not found")
    except IOError as e:
        print(f"Error reading script: {e}")


def repl_loop(config:Dict[str,Optional[str]],vfs:VirtualFileSystem)->None:
    """
    Основной цикл REPL (Read-Eval-Print Loop).
    """
    prompt = get_prompt(config, vfs)

    while True:
        try:
            user_input = input(prompt)

            if not user_input.strip():
                continue

            vfs.history.append(user_input)
            cmd, args = parse_command(user_input)
            result = execute_command(cmd, args, vfs)

            if result == "__EXIT__":
                break

            if result:
                print(result)

        except EOFError:
            break
        except KeyboardInterrupt:
            print()
            continue


def main() -> None:
    """Точка входа в приложение."""
    config = parse_arguments()
    print_debug_info(config)

    vfs = VirtualFileSystem()
    if config.get('vfs'):
        if not vfs.load_from_directory(config['vfs']):
            print(f"Error: Cannot load VFS from '{config['vfs']}'")
            return

    if config.get('script'):
        prompt = get_prompt(config, vfs)
        execute_script(config['script'], prompt, vfs)
    else:
        repl_loop(config, vfs)


if __name__ == '__main__':
    main()