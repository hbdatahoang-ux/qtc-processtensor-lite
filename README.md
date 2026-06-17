# QTC Process-Tensor Lite v0.1-alpha

## 1. Mục tiêu (Objective)
Dự án này tập trung vào việc khảo sát các **đặc trưng sai số nén (compression-error signatures)** trong các mô hình va chạm (collision models) giữa hệ thống lượng tử và môi trường (Markovian vs. Non-Markovian). Mục đích cốt lõi là thiết lập một pipeline kiểm định để phân biệt giữa các dị thường vật lý thực sự và các tạo tác số học (numerical artifacts).

## 2. Yêu cầu (Requirements)
Pipeline yêu cầu Python 3.x với các thư viện sau:
- `numpy>=2.0.0`
- `scipy>=1.14.0`
- `matplotlib>=3.10.0`
- `pyyaml>=6.0.0`

Cài đặt môi trường:
```bash
pip install -r requirements.txt