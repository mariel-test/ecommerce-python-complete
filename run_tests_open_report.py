#!/usr/bin/env python3
import subprocess
import sys
import webbrowser
from pathlib import Path

root = Path(__file__).resolve().parent
report = root / "python-report" / "report.html"

command = [sys.executable, "-m", "pytest", "--html={}".format(report), "--self-contained-html"]
print("Ejecutando:", " ".join(command))
result = subprocess.run(command)

if result.returncode == 0:
    if report.exists():
        print(f"Reporte generado en: {report}")
        webbrowser.open_new_tab(report.as_uri())
    else:
        print("El reporte no se generó: archivo no encontrado.")
else:
    print("Pytest falló con código de salida", result.returncode)

sys.exit(result.returncode)
