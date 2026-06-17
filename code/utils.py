import numpy as np
import os
import json

def ensure_hermitian(rho):
    """Ép ma trận về dạng Hermitian: rho = 0.5 * (rho + rho.conj().T)"""
    return 0.5 * (rho + rho.conj().T)

def ensure_cptp(rho):
    """Ép ma trận về dạng Trace-preserving (Trace = 1)."""
    tr = np.trace(rho)
    if np.abs(tr) < 1e-12:
        return rho # Hoặc xử lý lỗi tùy ý
    return rho / tr

def save_data_npy(filename, data):
    """Lưu data vào thư mục data/."""
    path = os.path.join("data", filename)
    np.save(path, data)
    return path

def log_to_jsonl(filename, entry):
    """Ghi log kiểu append-only (thích hợp cho run_history)."""
    path = os.path.join("logs", filename)
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")

def print_banner(text):
    """Format in log đẹp mắt."""
    print(f"\n{'='*60} - utils.py:30")
    print(f"{text} - utils.py:31")
    print(f"{'='*60}\n - utils.py:32")