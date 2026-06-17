import numpy as np
import scipy.linalg

def get_interaction_unitary(dim_S, dim_E, dt):
    """Sinh toán tử tương tác Unitary ngẫu nhiên giữa Hệ (S) và Môi trường (E)."""
    dim_tot = dim_S * dim_E
    H_rand = np.random.randn(dim_tot, dim_tot) + 1j * np.random.randn(dim_tot, dim_tot)
    H = 0.5 * (H_rand + H_rand.conj().T)
    return scipy.linalg.expm(-1j * H * dt)

def partial_trace(rho_tot, dim_S, dim_E, trace_out="E"):
    """Trích xuất ma trận mật độ của Hệ hoặc Môi trường (Partial Trace)."""
    if trace_out == "E":
        # Trace out Môi trường (E) để lấy Hệ (S)
        rho_S = np.zeros((dim_S, dim_S), dtype=rho_tot.dtype)
        for i in range(dim_E):
            rho_S += rho_tot[i::dim_E, i::dim_E]
        return rho_S
    else:
        # Trace out Hệ (S) để lấy Môi trường (E)
        rho_E = np.zeros((dim_E, dim_E), dtype=rho_tot.dtype)
        for i in range(dim_S):
            rho_E += rho_tot[i*dim_E:(i+1)*dim_E, i*dim_E:(i+1)*dim_E]
        return rho_E

def evolve_nonmarkov(steps=10, dim_S=2, dim_E=2, dt=0.05, mem_strength=0.5):
    """
    Tiến hóa phi-Markov thông qua cơ chế Ancilla Memory.
    mem_strength: 0.0 = Markov, 1.0 = Max Memory Retention.
    """
    # Khởi tạo trạng thái ban đầu
    psi_S = np.array([1.0, 0.0], dtype=np.complex128)
    rho_S = np.outer(psi_S, psi_S.conj().T)
    
    # Trạng thái ban đầu của môi trường (Ancilla)
    rho_E = np.eye(dim_E) / dim_E
    
    U_SE = get_interaction_unitary(dim_S, dim_E, dt)
    
    current_rho_E = rho_E.copy()

    for _ in range(steps):
        # 1. Kết hợp Hệ và Môi trường (Ancilla)
        rho_tot = np.kron(rho_S, current_rho_E)
        
        # 2. Tương tác Unitary
        rho_tot = U_SE @ rho_tot @ U_SE.conj().T
        
        # 3. Trích xuất Môi trường sau va chạm
        rho_E_after = partial_trace(rho_tot, dim_S, dim_E, trace_out="S")
        
        # 4. Cơ chế phi-Markov: Trộn trạng thái môi trường cũ với trạng thái tươi mới
        # Đây là nút xoay (control knob) cho Non-Markovianity
        current_rho_E = (1.0 - mem_strength) * rho_E + mem_strength * rho_E_after
        
        # Chuẩn hóa môi trường
        current_rho_E = current_rho_E / np.trace(current_rho_E)
        
    # Trả về trạng thái cuối của Hệ S
    # Để đơn giản, ta trả về rho S sau bước cuối cùng
    return partial_trace(rho_tot, dim_S, dim_E, trace_out="E")