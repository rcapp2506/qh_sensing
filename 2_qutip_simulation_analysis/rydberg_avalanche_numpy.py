"""
Avalanche Terahertz Photon Detection in Rydberg Tweezer Arrays
Based on: Phys. Rev. Lett. 133, 073603 (2024)

STANDALONE VERSION - Pure NumPy implementation (no QuTiP dependency)

This code simulates the facilitated Rydberg excitation dynamics during
the amplification phase of a single-photon THz detector.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from scipy.sparse import csr_matrix, kron, identity
import time

# ============================================================================
# PHYSICAL PARAMETERS (from the paper)
# ============================================================================

class RydbergDetectorParams:
    """Parameters for the Rydberg THz detector"""
    
    def __init__(self, scenario='a'):
        """
        Initialize parameters for scenario (a) or (b) from paper
        
        Scenario (a): 68S_{1/2} -> 70P_{1/2}, ω_THz ≈ 54 GHz
        Scenario (b): 45S_{1/2} -> 70P_{1/2}, ω_THz ≈ 1 THz
        """
        # Common parameters
        self.N = 11                    # Number of atoms
        self.a0 = 6e-6                 # Lattice spacing (m)
        
        if scenario == 'a':
            # Scenario (a): Microwave demonstration
            self.V_rr = 2 * np.pi * 12.5e6    # Interaction V_rr (rad/s)
            self.V_ee = 2 * np.pi * 9e6       # Interaction V_ee (rad/s)
            self.V_er = 2 * np.pi * 1e6       # Cross interaction (rad/s)
            self.Omega_ge = 2 * np.pi * 30e6  # π-pulse Rabi frequency (rad/s)
            self.Omega_gr = 2 * np.pi * 0.2e6 # Amplification Rabi freq (rad/s)
            self.omega_THz = 2 * np.pi * 54e9 # THz frequency (rad/s)
            
        elif scenario == 'b':
            # Scenario (b): True THz regime
            self.V_rr = 2 * np.pi * 12.5e6    # Interaction V_rr (rad/s)
            self.V_ee = 2 * np.pi * 5e6       # Weaker interaction
            self.V_er = 2 * np.pi * 0.5e6     # Weaker cross interaction
            self.Omega_ge = 2 * np.pi * 30e6  # π-pulse Rabi frequency (rad/s)
            self.Omega_gr = 2 * np.pi * 0.2e6 # Amplification Rabi freq (rad/s)
            self.omega_THz = 2 * np.pi * 1e12 # THz frequency (rad/s)
        
        # Facilitation condition: Δ_gr = -V_rr
        self.Delta_gr = -self.V_rr
        
        # Optimal amplification time
        self.T_a_optimal = self.N / self.Omega_gr


# ============================================================================
# QUANTUM STATE AND OPERATOR TOOLS
# ============================================================================

def basis_state(dim, n):
    """Create basis state |n⟩ in dimension dim"""
    state = np.zeros(dim, dtype=complex)
    state[n] = 1.0
    return state


def ket_to_density(ket):
    """Convert ket |ψ⟩ to density matrix |ψ⟩⟨ψ|"""
    return np.outer(ket, ket.conj())


def tensor_product(*operators):
    """Compute tensor product of operators"""
    result = operators[0]
    for op in operators[1:]:
        result = np.kron(result, op)
    return result


def pauli_matrices():
    """Return Pauli matrices"""
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    Id = np.eye(2, dtype=complex)
    return sigma_x, sigma_y, sigma_z, Id


def ladder_operators():
    """
    Return ladder operators for two-level system
    σ+ = |1⟩⟨0| (raising/excitation)
    σ- = |0⟩⟨1| (lowering/de-excitation)
    """
    sigma_plus = np.array([[0, 0], [1, 0]], dtype=complex)  # |r⟩⟨g|
    sigma_minus = np.array([[0, 1], [0, 0]], dtype=complex)  # |g⟩⟨r|
    return sigma_plus, sigma_minus


def number_operator():
    """Return number operator n = |1⟩⟨1| for two-level system"""
    return np.array([[0, 0], [0, 1]], dtype=complex)


# ============================================================================
# INITIAL STATE PREPARATION
# ============================================================================

def initial_state_local_excitation(N, k=None):
    """
    Prepare initial state |Ψ_gr⟩ with one atom in |r⟩ at site k
    
    |Ψ_gr⟩ = |g⟩_0 ⊗ |g⟩_1 ⊗ ... ⊗ |r⟩_k ⊗ ... ⊗ |g⟩_{N-1}
    
    Args:
        N: Number of atoms
        k: Site with Rydberg excitation (default: center)
    
    Returns:
        psi0: Initial state vector (dimension 2^N)
    """
    if k is None:
        k = N // 2  # Central atom
    
    # Build tensor product
    state_list = []
    for j in range(N):
        if j == k:
            state_list.append(basis_state(2, 1))  # |r⟩ = |1⟩
        else:
            state_list.append(basis_state(2, 0))  # |g⟩ = |0⟩
    
    psi0 = tensor_product(*state_list)
    return psi0


def initial_state_collective_excitation(N):
    """
    Prepare initial state with collective Rydberg excitation
    
    |Ψ^c_gr⟩ = (1/√N) ∑_k |g⟩_0 ⊗ ... ⊗ |r⟩_k ⊗ ... ⊗ |g⟩_{N-1}
    
    This is the state created by collective THz absorption
    
    Args:
        N: Number of atoms
    
    Returns:
        psi0: Initial collective state (dimension 2^N)
    """
    psi0 = np.zeros(2**N, dtype=complex)
    
    for k in range(N):
        # Create state with excitation at site k
        state_list = []
        for j in range(N):
            if j == k:
                state_list.append(basis_state(2, 1))  # |r⟩
            else:
                state_list.append(basis_state(2, 0))  # |g⟩
        
        psi0 += tensor_product(*state_list)
    
    # Normalize
    psi0 = psi0 / np.sqrt(N)
    
    return psi0


# ============================================================================
# HAMILTONIAN CONSTRUCTION
# ============================================================================

def build_hamiltonian_amplification(N, params):
    """
    Build the Hamiltonian for the amplification phase
    
    H_a = Ω_gr ∑_j (|r⟩⟨g|_j + h.c.) + Δ_gr ∑_j n^(r)_j + V_rr ∑_j n^(r)_j n^(r)_{j+1}
    
    With facilitation condition: Δ_gr + V_rr = 0
    
    Args:
        N: Number of atoms
        params: RydbergDetectorParams object
    
    Returns:
        H: Hamiltonian matrix (2^N × 2^N)
    """
    Omega_gr = params.Omega_gr
    Delta_gr = params.Delta_gr
    V_rr = params.V_rr
    
    # Get operators
    sigma_plus, sigma_minus = ladder_operators()
    n_r = number_operator()
    Id = np.eye(2, dtype=complex)
    
    # Initialize Hamiltonian
    dim = 2**N
    H = np.zeros((dim, dim), dtype=complex)
    
    print(f"  Building Hamiltonian for N={N} atoms (Hilbert space dim = {dim})...")
    
    # 1. Laser driving term: Ω_gr ∑_j (|r⟩⟨g|_j + |g⟩⟨r|_j)
    print("    Adding laser driving term...")
    for j in range(N):
        op_list = [Id] * N
        # |r⟩⟨g| + |g⟩⟨r|
        op_list[j] = sigma_plus + sigma_minus
        H += Omega_gr * tensor_product(*op_list)
    
    # 2. Detuning term: Δ_gr ∑_j n^(r)_j
    print("    Adding detuning term...")
    for j in range(N):
        op_list = [Id] * N
        op_list[j] = n_r
        H += Delta_gr * tensor_product(*op_list)
    
    # 3. Nearest-neighbor interaction: V_rr ∑_j n^(r)_j n^(r)_{j+1}
    print("    Adding interaction term...")
    for j in range(N - 1):
        op_list = [Id] * N
        op_list[j] = n_r
        op_list[j + 1] = n_r
        H += V_rr * tensor_product(*op_list)
    
    return H


def operator_n_r_site(j, N):
    """
    Build the number operator n^(r)_j for site j in N-atom chain
    
    Args:
        j: Site index (0 to N-1)
        N: Total number of atoms
    
    Returns:
        n_r_j: Number operator matrix (2^N × 2^N)
    """
    n_r = number_operator()
    Id = np.eye(2, dtype=complex)
    
    op_list = [Id] * N
    op_list[j] = n_r
    
    return tensor_product(*op_list)


# ============================================================================
# TIME EVOLUTION
# ============================================================================

def time_evolution_unitary(H, t):
    """
    Compute time evolution operator U(t) = exp(-i H t)
    
    Args:
        H: Hamiltonian matrix
        t: Evolution time
    
    Returns:
        U: Unitary evolution operator
    """
    return expm(-1j * H * t)


def evolve_state(psi0, H, times):
    """
    Evolve state |ψ(0)⟩ to |ψ(t)⟩ = U(t) |ψ(0)⟩
    
    Args:
        psi0: Initial state vector
        H: Hamiltonian
        times: Array of time points
    
    Returns:
        states: List of state vectors at each time
    """
    states = []
    
    print(f"  Evolving quantum state over {len(times)} time steps...")
    
    for idx, t in enumerate(times):
        if (idx + 1) % 20 == 0:
            print(f"    Progress: {idx+1}/{len(times)} ({100*(idx+1)/len(times):.1f}%)")
        
        U_t = time_evolution_unitary(H, t)
        psi_t = U_t @ psi0
        states.append(psi_t)
    
    return states


def compute_signal_evolution(psi0, H, times, N):
    """
    Evolve state and compute spatially-resolved signal S_j(t)
    
    S_j(t) = ⟨Ψ(t)| n^(r)_j |Ψ(t)⟩
    S(t) = ∑_j S_j(t)
    
    Args:
        psi0: Initial state
        H: Hamiltonian
        times: Array of time points
        N: Number of atoms
    
    Returns:
        S_total: Total signal S(t)
        S_spatiotemporal: Matrix S_j(t) [sites × times]
    """
    # Time evolution
    print("Computing time evolution...")
    states = evolve_state(psi0, H, times)
    
    # Compute spatially-resolved signal
    S_spatiotemporal = np.zeros((N, len(times)))
    
    print("Computing spatially-resolved signal...")
    
    # Pre-compute all number operators
    n_r_operators = [operator_n_r_site(j, N) for j in range(N)]
    
    for idx, psi_t in enumerate(states):
        if (idx + 1) % 20 == 0:
            print(f"  Progress: {idx+1}/{len(times)} ({100*(idx+1)/len(times):.1f}%)")
        
        for j in range(N):
            # ⟨ψ| n_r_j |ψ⟩
            S_spatiotemporal[j, idx] = np.real(
                np.vdot(psi_t, n_r_operators[j] @ psi_t)
            )
    
    # Total signal
    S_total = np.sum(S_spatiotemporal, axis=0)
    
    return S_total, S_spatiotemporal


# ============================================================================
# PLOTTING FUNCTIONS
# ============================================================================

def plot_signal_evolution(times, S_total, S_spatiotemporal, params, 
                         initial_state_type='local', save_fig=True):
    """
    Plot the signal evolution S(t) and spatially-resolved S_j(t)
    """
    N = S_spatiotemporal.shape[0]
    
    # Normalize time by Omega_gr
    times_norm = times * params.Omega_gr
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # ========== Plot 1: Spatially-resolved signal ==========
    im = ax1.imshow(S_spatiotemporal, aspect='auto', origin='lower',
                    extent=[times_norm[0], times_norm[-1], 0, N],
                    cmap='hot', interpolation='nearest')
    ax1.set_xlabel(r'Time $\Omega_{gr} t$', fontsize=14)
    ax1.set_ylabel('Site $j$', fontsize=14)
    ax1.set_title(f'Spatially-resolved signal $S_j(t)$ ({initial_state_type} excitation)',
                  fontsize=14)
    
    # Mark different phases
    T_a_opt_norm = params.T_a_optimal * params.Omega_gr
    if T_a_opt_norm < times_norm[-1]:
        ax1.axvline(T_a_opt_norm, color='cyan', linestyle='--', 
                   linewidth=2, label=r'$T_a$ (optimal)')
        ax1.legend(fontsize=12, loc='upper right')
    
    plt.colorbar(im, ax=ax1, label=r'$S_j$')
    
    # ========== Plot 2: Total signal ==========
    ax2.plot(times_norm, S_total, 'b-', linewidth=2, label='Total signal')
    ax2.set_xlabel(r'Time $\Omega_{gr} t$', fontsize=14)
    ax2.set_ylabel(r'Total Signal $S$', fontsize=14)
    ax2.set_title(f'Total signal evolution ({initial_state_type} excitation)',
                  fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    # Identify phases
    # Phase 1: Quadratic (~t^2)
    # Phase 2: Linear (~t)
    # Phase 3: Saturation
    
    # Find linear region (middle part)
    mid_idx = len(S_total) // 2
    quarter_idx = len(S_total) // 4
    
    # Check if we're in linear regime
    linear_region = S_total[quarter_idx:3*quarter_idx]
    times_linear = times_norm[quarter_idx:3*quarter_idx]
    
    if len(linear_region) > 10:
        # Linear fit
        coeffs = np.polyfit(times_linear, linear_region, 1)
        linear_fit = coeffs[0] * times_norm + coeffs[1]
        ax2.plot(times_norm, linear_fit, 'r--', linewidth=1.5, 
                alpha=0.7, label=f'Linear fit: $S \propto {coeffs[0]:.2f} t$')
    
    # Mark optimal time
    if T_a_opt_norm < times_norm[-1]:
        ax2.axvline(T_a_opt_norm, color='cyan', linestyle='--',
                   linewidth=2, label=r'$T_a$ (optimal)')
        
        # Mark signal at optimal time
        idx_opt = np.argmin(np.abs(times_norm - T_a_opt_norm))
        ax2.plot(T_a_opt_norm, S_total[idx_opt], 'go', 
                markersize=10, label=f'$S(T_a) = {S_total[idx_opt]:.1f}$')
    
    ax2.legend(fontsize=11)
    
    plt.tight_layout()
    
    if save_fig:
        filename = f'signal_evolution_{initial_state_type}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\nFigure saved as {filename}")
    
    plt.show()


def plot_comparison_local_vs_collective(times, S_local, S_collective, params):
    """
    Compare signal evolution for local vs collective initial excitation
    """
    times_norm = times * params.Omega_gr
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(times_norm, S_local, 'b-', linewidth=2.5, 
            label='Local excitation (center)', alpha=0.8)
    plt.plot(times_norm, S_collective, 'r-', linewidth=2.5, 
            label='Collective excitation', alpha=0.8)
    
    plt.xlabel(r'Time $\Omega_{gr} t$', fontsize=14)
    plt.ylabel(r'Total Signal $S$', fontsize=14)
    plt.title('Comparison: Local vs Collective THz Absorption', fontsize=14, pad=15)
    plt.grid(True, alpha=0.3)
    
    # Mark optimal time
    T_a_opt_norm = params.T_a_optimal * params.Omega_gr
    if T_a_opt_norm < times_norm[-1]:
        plt.axvline(T_a_opt_norm, color='cyan', linestyle='--',
                   linewidth=2, alpha=0.7, label=r'$T_a$ (optimal)')
        
        # Mark signals at optimal time
        idx_opt = np.argmin(np.abs(times_norm - T_a_opt_norm))
        plt.plot(T_a_opt_norm, S_local[idx_opt], 'bs', 
                markersize=8, label=f'Local: $S = {S_local[idx_opt]:.1f}$')
        plt.plot(T_a_opt_norm, S_collective[idx_opt], 'rs', 
                markersize=8, label=f'Collective: $S = {S_collective[idx_opt]:.1f}$')
    
    plt.legend(fontsize=11, loc='best')
    plt.tight_layout()
    plt.savefig('comparison_local_vs_collective.png', dpi=300, bbox_inches='tight')
    print("\nComparison figure saved as: comparison_local_vs_collective.png")
    plt.show()


# ============================================================================
# MAIN SIMULATION FUNCTIONS
# ============================================================================

def run_simulation_local_excitation(N=11, scenario='a', max_time_factor=10):
    """
    Run simulation with local THz excitation at center
    """
    print(f"\n{'='*70}")
    print(f"SIMULATION 1: Local THz Excitation")
    print(f"  N = {N} atoms, scenario = {scenario}")
    print(f"{'='*70}\n")
    
    # Initialize parameters
    params = RydbergDetectorParams(scenario=scenario)
    params.N = N
    
    # Print key parameters
    print(f"Physical parameters:")
    print(f"  Ω_gr / 2π = {params.Omega_gr / (2*np.pi) / 1e6:.3f} MHz")
    print(f"  Δ_gr / 2π = {params.Delta_gr / (2*np.pi) / 1e6:.3f} MHz")
    print(f"  V_rr / 2π = {params.V_rr / (2*np.pi) / 1e6:.3f} MHz")
    print(f"  Facilitation check: Δ_gr + V_rr = {(params.Delta_gr + params.V_rr)/(2*np.pi):.2e} Hz ✓")
    print(f"  T_a (optimal) = {params.T_a_optimal * 1e6:.2f} μs")
    print()
    
    # Build Hamiltonian
    print("Building Hamiltonian...")
    t_start = time.time()
    H = build_hamiltonian_amplification(N, params)
    print(f"  Hamiltonian built in {time.time() - t_start:.2f} s")
    print(f"  Matrix shape: {H.shape}")
    print(f"  Matrix is Hermitian: {np.allclose(H, H.conj().T)}")
    print()
    
    # Prepare initial state
    print("Preparing initial state (local excitation at center)...")
    psi0 = initial_state_local_excitation(N, k=N//2)
    print(f"  Initial state norm: {np.linalg.norm(psi0):.6f}")
    print(f"  State dimension: {len(psi0)}")
    print()
    
    # Time points
    t_max = max_time_factor * params.T_a_optimal
    n_times = 100 if N <= 7 else (50 if N <= 9 else 40)
    times = np.linspace(0, t_max, n_times)
    print(f"Time evolution:")
    print(f"  t_max = {t_max*1e6:.2f} μs ({max_time_factor} × T_a)")
    print(f"  Number of time steps: {len(times)}")
    print()
    
    # Evolve and compute signal
    t_start = time.time()
    S_total, S_spatiotemporal = compute_signal_evolution(psi0, H, times, N)
    elapsed = time.time() - t_start
    print(f"\n✓ Simulation completed in {elapsed:.1f} s")
    print()
    
    # Analysis
    print("Results:")
    print(f"  Initial signal S(0) = {S_total[0]:.4f}")
    print(f"  Final signal S(t_max) = {S_total[-1]:.2f}")
    
    idx_opt = np.argmin(np.abs(times - params.T_a_optimal))
    print(f"  Signal at T_a (optimal) = {S_total[idx_opt]:.2f}")
    print(f"  Maximum possible signal = {N}")
    print(f"  Amplification factor = {S_total[idx_opt]:.1f}×")
    print()
    
    return times, S_total, S_spatiotemporal, params


def run_simulation_collective_excitation(N=11, scenario='a', max_time_factor=10):
    """
    Run simulation with collective THz excitation
    """
    print(f"\n{'='*70}")
    print(f"SIMULATION 2: Collective THz Excitation")
    print(f"  N = {N} atoms, scenario = {scenario}")
    print(f"{'='*70}\n")
    
    # Initialize parameters
    params = RydbergDetectorParams(scenario=scenario)
    params.N = N
    
    # Build Hamiltonian (reuse from previous)
    print("Building Hamiltonian...")
    t_start = time.time()
    H = build_hamiltonian_amplification(N, params)
    print(f"  Hamiltonian built in {time.time() - t_start:.2f} s")
    print()
    
    # Prepare initial state
    print("Preparing initial state (collective excitation)...")
    psi0 = initial_state_collective_excitation(N)
    print(f"  Initial state norm: {np.linalg.norm(psi0):.6f}")
    print(f"  State is superposition of {N} configurations")
    print()
    
    # Time points
    t_max = max_time_factor * params.T_a_optimal
    n_times = 100 if N <= 7 else (50 if N <= 9 else 40)
    times = np.linspace(0, t_max, n_times)
    print(f"Time evolution: 0 to {t_max*1e6:.2f} μs ({len(times)} steps)")
    print()
    
    # Evolve and compute signal
    t_start = time.time()
    S_total, S_spatiotemporal = compute_signal_evolution(psi0, H, times, N)
    elapsed = time.time() - t_start
    print(f"\n✓ Simulation completed in {elapsed:.1f} s")
    print()
    
    # Analysis
    print("Results:")
    print(f"  Initial signal S(0) = {S_total[0]:.4f}")
    print(f"  Final signal S(t_max) = {S_total[-1]:.2f}")
    
    idx_opt = np.argmin(np.abs(times - params.T_a_optimal))
    print(f"  Signal at T_a (optimal) = {S_total[idx_opt]:.2f}")
    print(f"  Amplification factor = {S_total[idx_opt]:.1f}×")
    print()
    
    return times, S_total, S_spatiotemporal, params


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    """
    Main execution: Run simulations and generate plots
    """
    
    print("\n" + "="*70)
    print(" AVALANCHE TERAHERTZ PHOTON DETECTION IN RYDBERG ARRAYS")
    print(" Based on: Phys. Rev. Lett. 133, 073603 (2024)")
    print(" Pure NumPy Implementation (Standalone)")
    print("="*70)
    
    # Choose system size (smaller for faster computation)
    N_atoms = 9  # Use 9 atoms for reasonable computation time
    
    print(f"\nSystem size: N = {N_atoms} atoms")
    print(f"Hilbert space dimension: 2^{N_atoms} = {2**N_atoms}")
    print()
    
    # ========== Simulation 1: Local excitation ==========
    times_local, S_local, S_spatio_local, params = \
        run_simulation_local_excitation(N=N_atoms, scenario='a', max_time_factor=10)
    
    # Plot results
    plot_signal_evolution(times_local, S_local, S_spatio_local, params,
                         initial_state_type='local', save_fig=True)
    
    # ========== Simulation 2: Collective excitation ==========
    times_coll, S_coll, S_spatio_coll, params = \
        run_simulation_collective_excitation(N=N_atoms, scenario='a', max_time_factor=10)
    
    # Plot results
    plot_signal_evolution(times_coll, S_coll, S_spatio_coll, params,
                         initial_state_type='collective', save_fig=True)
    
    # ========== Comparison plot ==========
    plot_comparison_local_vs_collective(times_local, S_local, S_coll, params)
    
    print("\n" + "="*70)
    print(" ALL SIMULATIONS COMPLETED SUCCESSFULLY!")
    print(" Figures saved:")
    print("   - signal_evolution_local.png")
    print("   - signal_evolution_collective.png")
    print("   - comparison_local_vs_collective.png")
    print("="*70 + "\n")
