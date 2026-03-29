#!/bin/bash
echo "Компиляция проекта..."
python3 -m nuitka --standalone \
  --onefile \
  --enable-plugin=tk-inter \
  --enable-plugin=numpy \
  --enable-plugin=matplotlib \
  --output-filename=ECU_Analyzer \
  main.pyw
echo "Готово!"