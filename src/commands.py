"""
Модуль с реализацией команд эмулятора оболочки.
"""
from typing import List, Optional
from vfs import VirtualFileSystem

def cmd_ls(args: List[str], vfs: VirtualFileSystem) -> str:
    """
    Выводит содержимое директории в VFS.
    """
    path = args[0] if args else ''
    success, output = vfs.list_directory(path)
    if not success:
        return output
    return output

def cmd_cd(args: List[str], vfs: VirtualFileSystem) -> str:
    """
    Меняет текущую директорию в VFS.
    """
    path = args[0] if args else ''
    success, message = vfs.change_directory(path)
    return message


def cmd_vfs_info(args: List[str], vfs: VirtualFileSystem) -> str:
    """
    Выводит информацию о VFS (имя и SHA-256 хеш).
    """
    name = vfs.vfs_name
    sha = vfs.get_sha256()
    return f"VFS name: {name}\nSHA-256: {sha}"


def cmd_exit(args: List[str]) -> str:
    """
    Завершает работу эмулятора.
    """
    return "__EXIT__"


def execute_command(command: str, args: List[str],
                    vfs: Optional[VirtualFileSystem] = None) -> str:
    """
    Выполняет команду и возвращает результат.
    """
    if vfs is None:
        vfs = VirtualFileSystem()

    commands = {
        'vfs-ls': lambda: cmd_ls(args, vfs),      # Было 'ls'
        'vfs-cd': lambda: cmd_cd(args, vfs),      # Было 'cd'
        'vfs-info': lambda: cmd_vfs_info(args, vfs),
        'exit': lambda: cmd_exit(args),
    }

    if command in commands:
        return commands[command]()

    return f"Error: Unknown command '{command}'"