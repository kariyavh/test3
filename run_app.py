import os, sys, webbrowser, threading
from pathlib import Path

os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
os.environ["STREAMLIT_GLOBAL_DEVELOPMENTMODE"] = "false"
for k in ("STREAMLIT_SERVER_PORT", "STREAMLIT_SERVER_ADDRESS", "PORT"):
    os.environ.pop(k, None)

def bundle_dir() -> Path:
    return Path(getattr(sys, "_MEIPASS", Path(__file__).parent))

_bd = bundle_dir()
# make bundled modules importable
sys.path.insert(0, str(_bd))
sys.path.insert(0, str(_bd / "app"))

def rp(rel: str) -> Path:
    return _bd / rel

if __name__ == "__main__":
    app_path = rp("streamlit_app.py")
    threading.Timer(1.2, lambda: webbrowser.open("http://localhost:8501")).start()
    import streamlit.web.cli as stcli
    sys.argv = ["streamlit", "run", str(app_path), "--global.developmentMode=false"]
    sys.exit(stcli.main())
