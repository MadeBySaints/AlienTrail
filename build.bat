@echo off

echo Building executable from source code...
pyinstaller --onefile --icon=png.png --name "Alien Trail v.0.0.1" AlienTrail.py

echo Build complete.
pause
