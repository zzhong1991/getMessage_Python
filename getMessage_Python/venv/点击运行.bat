@echo off
cd  F:\pyhon\getMessage_Python\venv
start python main.py
ping -n 3 127.0.0.1>nul
start python ipProxy.py
exit