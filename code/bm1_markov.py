import numpy as np
import scipy.linalg

def initialize_state(dim=4):
    """Khởi tạo trạng thái ban đầu: thuần túy |0><0|."""
    rho = np.zeros((dim, dim), dtype=np.complex128)
    rho[0, 0] = 1.0
    return rho

def get_markov_unitary(dim, dt):
    """Tạo toán tử unitary cố định dựa trên một Hamiltonian ngẫu nhiên."""
    # Tạo Hamiltonian Hermitian cố định
    H_raw = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
    H = 0.5 * (H_raw + H_raw.conj().T)
    
    # Unitary evolution operator: U = exp(-i * H * dt)
    U = scipy.linalg.expm(-1j * H * dt)
    return U

def evolve_markov(rho0, steps=10, dim=4, dt=0.05):
    """
    Tiến hóa Markov đơn giản: rho(t+dt) = U * rho(t) * U_dag
    Trả về toàn bộ trajectory (list các density matrices).
    """
    rho = rho0.astype(np.complex128)
    U = get_markov_unitary(dim, dt)
    
    trajectory = [rho.copy()]
    
    for _ in range(steps):
        # Markovian update
        rho = U @ rho @ U.conj().T
        
        # Đảm bảo tính ổn định số học (Numerical stability)
        rho = 0.5 * (rho + rho.conj().T) # Giữ tính Hermitian
        rho = rho / np.trace(rho)        # Giữ tính Trace-preserving
        
        trajectory.append(rho.copy())
        
    return trajectory