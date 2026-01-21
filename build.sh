#!/usr/bin/sh

#https://andreafortuna.org//2017/12/27/how-to-cross-compile-a-python-script-into-a-windows-executable-on-linux/
#https://stackoverflow.com/questions/2950971/packaging-a-python-script-on-linux-into-a-windows-executable

uvx pyinstaller --onefile \
                --nowindow \
                --clean \
                --icon=feuerwehrhelm.ico \
                --collect-all ttkbootstrap\
                --paths ./.venv/lib64/python3.13/site-packages/ \
                --name "Feuerwehr-Anmelder" \
                --hidden-import="PIL._tkinter_finder" \
                --add-data="feuerwehrhelm.png:." \
                main.py