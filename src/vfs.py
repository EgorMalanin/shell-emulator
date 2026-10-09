"""
Модуль виртуальной файловой системы (VFS).
Все операции выполняются в памяти.
"""
import hashlib
import os
from typing import Dict, List, Optional, Tuple


class VFSNode:
    """Узел дерева виртуальной файловой системы."""
    def __init__(self, name: str, is_dir: bool,
                 content: bytes = b'') -> None:
        """
        Инициализирует узел VFS.
        """
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.children: Dict[str, 'VFSNode'] = {}


class VirtualFileSystem:
    """Виртуальная ФС, работающая полностью в памяти."""

    def __init__(self) -> None:
        """Инициализирует пустую VFS с корневой директорией."""
        self.root = VFSNode('/', True)
        self.cwd = self.root
        self.vfs_name = 'default'
        self.vfs_path = ''
        self.history: List[str] = []

    def load_from_directory(self, path: str) -> bool:
        """
        Загружает VFS из реальной директории на диске.
        """
        if not os.path.exists(path):
            return False
        if not os.path.isdir(path):
            return False

        self.vfs_path = path
        self.vfs_name = os.path.basename(os.path.abspath(path))
        self.root = VFSNode('/', True)
        self.cwd = self.root

        self._load_directory(path, self.root)
        return True

    def _load_directory(self, real_path: str,vfs_node: VFSNode) -> None:
        """
        Рекурсивно загружает реальную директорию в VFS.
        """
        try:
            for item in os.listdir(real_path):
                item_path = os.path.join(real_path, item)
                if os.path.isdir(item_path):
                    child = VFSNode(item, True)
                    vfs_node.children[item] = child
                    self._load_directory(item_path, child)
                else:
                    with open(item_path, 'rb') as f:
                        content = f.read()
                    child = VFSNode(item, False, content)
                    vfs_node.children[item] = child
        except PermissionError:
            pass

    def get_sha256(self) -> str:
        """
        Вычисляет SHA-256 хеш всех данных VFS.
        """
        hasher = hashlib.sha256()
        files = self._get_all_files()
        for path, content in sorted(files):
            hasher.update(path.encode('utf-8'))
            hasher.update(content)
        return hasher.hexdigest()

    def _get_all_files(self) -> List[Tuple[str, bytes]]:
        """Возвращает список (путь, контент) всех файлов."""
        result: List[Tuple[str, bytes]] = []
        self._traverse(self.root, '/', result)
        return result

    def _traverse(self,node:VFSNode,path:str,result:List[Tuple[str,bytes]])->None:
        """Рекурсивно обходит дерево VFS."""
        if not node.is_dir:
            result.append((path, node.content))
            return
        for name in sorted(node.children.keys()):
            child = node.children[name]
            suffix = '/' if child.is_dir else ''
            child_path = path + name + suffix
            self._traverse(child, child_path, result)

    def resolve_path(self, path_str: str) -> Optional[VFSNode]:
        """
        Преобразует строку пути в узел VFS.
        """
        if path_str.startswith('/'):
            current = self.root
            parts = path_str.strip('/').split('/')
        else:
            current = self.cwd
            parts = path_str.split('/')

        for part in parts:
            if part == '' or part == '.':
                continue
            elif part == '..':
                if current != self.root:
                    parent = self._find_parent(current)
                    if parent:
                        current = parent
            else:
                if part not in current.children:
                    return None
                current = current.children[part]

        return current

    def _find_parent(self, node: VFSNode) -> Optional[VFSNode]:
        """Находит родительский узел для заданного узла."""
        if node == self.root:
            return None
        return self._find_parent_rec(self.root, node)

    def _find_parent_rec(self,current:VFSNode,target:VFSNode)->Optional[VFSNode]:
        """Рекурсивно ищет родителя целевого узла."""
        for child in current.children.values():
            if child == target:
                return current
            if child.is_dir:
                result = self._find_parent_rec(child, target)
                if result:
                    return result
        return None

    def change_directory(self, path_str: str) -> Tuple[bool, str]:
        """
        Меняет текущую рабочую директорию.
        """
        if not path_str:
            return True, ''

        node = self.resolve_path(path_str)
        if node is None:
            return False, f"cd: нет директории: {path_str}"
        if not node.is_dir:
            return False, f"cd: не директория: {path_str}"

        self.cwd = node
        return True, ''

    def list_directory(self, path_str: str = '') -> Tuple[bool, str]:
        """
        Выводит содержимое директории.
        """
        if path_str:
            node = self.resolve_path(path_str)
        else:
            node = self.cwd

        if node is None:
            return False, f"ls: нет доступа к '{path_str}'"
        if not node.is_dir:
            return False, f"ls: не директория: {path_str}"

        if not node.children:
            return True, ''

        lines = []
        for name in sorted(node.children.keys()):
            child = node.children[name]
            if child.is_dir:
                lines.append(f"{name}/")
            else:
                size = len(child.content)
                lines.append(f"{name} ({size} bytes)")

        return True, '\n'.join(lines)

    def get_current_path(self) -> str:
        """Возвращает путь текущей директории строкой."""
        path_parts: List[str] = []
        current = self.cwd
        while current != self.root:
            path_parts.append(current.name)
            parent = self._find_parent(current)
            if parent is None:
                break
            current = parent
        path_parts.reverse()
        if path_parts:
            return '/' + '/'.join(path_parts)
        return '/'

    def read_file(self, path: str) -> Optional[str]:
        """
        Читает содержимое файла из VFS как текст.
        """
        node = self.resolve_path(path)
        if node is None or node.is_dir:
            return None
        try:
            return node.content.decode('utf-8')
        except UnicodeDecodeError:
            return "[Binary content]"
    def remove_directory(self, path_str: str) -> Tuple[bool, str]:
        """
        Удаляет пустую директорию из VFS.
        """
        if not path_str:
            return False, "rmdir: missing operand"

        node = self.resolve_path(path_str)
        if node is None:
            return False, f"rmdir: '{path_str}': No such file or directory"

        if not node.is_dir:
            return False, f"rmdir: '{path_str}': Not a directory"

        if node.children:
            return False, f"rmdir: '{path_str}': Directory not empty"

        if node == self.root:
            return False, "rmdir: '/': Invalid argument"

        parent = self._find_parent(node)
        if parent:
            del parent.children[node.name]
            if self.cwd == node:
                self.cwd = parent
            return True, ""

        return False, "rmdir: Internal error"