@echo off
python -m pip install -U pip
pip install -r requirements.txt

pyinstaller --noconfirm --onefile --console ^
  --name OfficeEfficiencyToolkit ^
  --collect-all streamlit ^
  --collect-all pandas ^
  --collect-all openpyxl ^
  --collect-all pypdf ^
  --hidden-import app.data_tools ^
  --hidden-import app.pdf_tools ^
  --hidden-import app.rename_tools ^
  --add-data "streamlit_app.py;." ^
  --add-data "app;app" ^
  run_app.py

echo Build complete. Executable is in dist\
