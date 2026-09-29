"""
Модуль обработки конфигурации эмулятора.
"""
import argparse
from typing import Dict, Optional


def parse_arguments() -> Dict[str, Optional[str]]:
    """
    Парсинг аргументов командной строки.
    """
    parser = argparse.ArgumentParser(
        description='Shell Emulator'
    )

    parser.add_argument(
        '--vfs', '-v',
        type=str,
        default=None,
        help='Path to VFS location'
    )

    parser.add_argument(
        '--prompt', '-p',
        type=str,
        default=None,
        help='Custom prompt string'
    )

    parser.add_argument(
        '--script', '-s',
        type=str,
        default=None,
        help='Path to startup script'
    )

    args = parser.parse_args()

    return {
        'vfs': args.vfs,
        'prompt': args.prompt,
        'script': args.script,
    }


def print_debug_info(config: Dict[str, Optional[str]]) -> None:
    """
    Выводит отладочную информацию о конфигурации.
    """
    print("[DEBUG] Config loaded:")
    for key, value in config.items():
        print(f"  {key}='{value}'")