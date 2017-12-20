import sys
from cx_Freeze import setup, Executable

setup(
    name = "Columns Game",
    version = "1.0",
    description = "A replica of 1990 SEGA Columns",
    executables = [Executable("main.py", base = "Win32GUI")])
