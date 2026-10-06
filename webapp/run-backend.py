"""Portable launcher: python webapp/run-backend.py (inside the installed environment)."""
import os
from pathlib import Path
import runpy
import sys
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('HF_HOME',str(ROOT/'.cache'/'huggingface'))
os.environ.setdefault('KAPAMPANGAN_MODEL_DIR',str(ROOT/'nllb'/'checkpoints'))
sys.path.insert(0,str(ROOT/'webapp'/'backend'))
if __name__=='__main__':runpy.run_path(str(ROOT/'webapp'/'backend'/'server.py'),run_name='__main__')
