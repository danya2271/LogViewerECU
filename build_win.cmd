@echo off
echo Компиляция проекта...
python -m nuitka --standalone ^
  --onefile ^
  --enable-plugin=tk-inter ^
  --enable-plugin=numpy ^
  --enable-plugin=matplotlib ^
  --windows-console-mode=disable ^
  --output-filename=ECU_Analyzer.exe ^
  main.py
echo Готово!
pause