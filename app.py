"""
Entrypoint Utama untuk Streamlit Community Cloud & GitHub Repository.
Mengarahkan eksekusi ke modul deteksi.py.
"""
import runpy

if __name__ == "__main__":
    runpy.run_module("deteksi", run_name="__main__")

