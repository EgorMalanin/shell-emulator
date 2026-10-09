"""
Модуль с реализацией команд эмулятора оболочки.
"""
from typing import List, Optional
from vfs import VirtualFileSystem
VFS = VirtualFileSystem

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


def cmd_uniq(args: List[str], vfs: VirtualFileSystem) -> str:
    """
    Выводит уникальные строки файла (удаляет подряд идущие дубли).
    """
    if not args:
        return "uniq: missing file operand"

    content = vfs.read_file(args[0])
    if content is None:
        return f"uniq: {args[0]}: No such file"

    lines = content.splitlines()
    if not lines:
        return ""

    result = [lines[0]]
    for line in lines[1:]:
        if line != result[-1]:
            result.append(line)

    return '\n'.join(result)


def cmd_tail(args: List[str], vfs: VirtualFileSystem) -> str:
    """
    Выводит последние N строк файла (по умолчанию 10).
    """
    num_lines = 10
    file_path = ''

    if args and args[0].startswith('-'):
        try:
            num_lines = int(args[0][1:])
            file_path = args[1] if len(args) > 1 else ''
        except ValueError:
            file_path = args[0]
    elif args:
        file_path = args[0]

    if not file_path:
        return "tail: missing file operand"

    content = vfs.read_file(file_path)
    if content is None:
        return f"tail: {file_path}: No such file"

    lines = content.splitlines()
    return '\n'.join(lines[-num_lines:])


def cmd_history(args: List[str], vfs: VirtualFileSystem) -> str:
    """
    Выводит историю выполненных команд.
    """
    if not vfs.history:
        return "History is empty"

    result = []
    for i, cmd in enumerate(vfs.history, 1):
        result.append(f"{i}: {cmd}")

    return '\n'.join(result)


def cmd_exit(args: List[str]) -> str:
    """
    Завершает работу эмулятора.
    """
    return "__EXIT__"


def execute_command(cmd:str,args:List[str],vfs:Optional[VFS]=None) -> str:
    """
    Выполняет команду и возвращает результат.
    """
    if vfs is None:
        vfs = VirtualFileSystem()

    commands = {
        'ls': lambda: cmd_ls(args, vfs),
        'cd': lambda: cmd_cd(args, vfs),
        'vfs-info': lambda: cmd_vfs_info(args, vfs),
        'uniq': lambda: cmd_uniq(args, vfs),
        'tail': lambda: cmd_tail(args, vfs),
        'history': lambda: cmd_history(args, vfs),
        'exit': lambda: cmd_exit(args),
    }

    if cmd in commands:
        return commands[cmd]()

    return f"Error: Unknown command '{cmd}'"