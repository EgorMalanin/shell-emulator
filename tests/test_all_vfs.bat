@echo off
echo === Testing all VFS variants with scripts ===

echo.
echo --- Minimal VFS ---
python src\shell.py --vfs tests\vfs_minimal ^
    --script tests\script_vfs_minimal.txt

echo.
echo --- Several files VFS ---
python src\shell.py --vfs tests\vfs_several ^
    --script tests\script_vfs_several.txt

echo.
echo --- Nested VFS (3+ levels) ---
python src\shell.py --vfs tests\vfs_nested ^
    --script tests\script_vfs_nested.txt

echo.
echo --- Full command test ---
python src\shell.py --vfs tests\vfs_nested ^
    --prompt "test> " ^
    --script tests\test_all_commands.txt