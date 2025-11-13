"""
Basic Usage Example - Avalanche THz Detector

This script shows the simplest way to run a simulation and get results.
Perfect for beginners!
"""

import sys
sys.path.append('../code')

from rydberg_avalanche_qutip import *

# ============================================================================
# BASIC USAGE
# ============================================================================

def basic_simulation():
    """
    Run a basic simulation with default parameters
    """
    print("="*70)
    print(" BASIC EXAMPLE: Avalanche THz Detector")
    print("="*70 + "\n")
    
    # Step 1: Set up parameters
    print("Step 1: Setting up parameters...")
    params = RydbergDetectorParams(scenario='a')
    params.N = 9  # Use 9 atoms for faster simulation
    params.print_summary()
    
    # Step 2: Build Hamiltonian
    print("Step 2: Building Hamiltonian...")
    H = build_hamiltonian_amplification(params.N, params)
    print(f"  ✓ Hamiltonian dimension: {H.shape[0]}")
    print()
    
    # Step 3: Prepare initial state (local excitation)
    print("Step 3: Preparing initial state...")
    psi0 = initial_state_local_excitation(params.N)
    print(f"  ✓ State norm: {psi0.norm():.6f}")
    print()
    
    # Step 4: Set time range
    print("Step 4: Setting up time evolution...")
    t_max = 5 * params.T_a_optimal  # Simulate 5 × optimal time
    times = np.linspace(0, t_max, 50)  # 50 time points
    print(f"  ✓ Time range: 0 to {t_max*1e6:.2f} μs")
    print()
    
    # Step 5: Run simulation
    print("Step 5: Running time evolution...")
    S_total, S_spatial, states = compute_signal_evolution(
        psi0, H, times, params.N, show_progress=True
    )
    print("  ✓ Simulation complete!")
    print()
    
    # Step 6: Analyze results
    print("Step 6: Analyzing results...")
    idx_opt = np.argmin(np.abs(times - params.T_a_optimal))
    
    print(f"  Initial signal: S(0) = {S_total[0]:.4f}")
    print(f"  Signal at T_a: S(T_a) = {S_total[idx_opt]:.2f}")
    print(f"  Final signal: S(t_max) = {S_total[-1]:.2f}")
    print(f"  Amplification: {S_total[idx_opt]:.1f}×")
    print()
    
    # Step 7: Plot results
    print("Step 7: Generating plot...")
    plot_signal_evolution(times, S_total, S_spatial, params,
                         initial_state_type='local', save_fig=True)
    print("  ✓ Figure saved!")
    print()
    
    print("="*70)
    print(" BASIC EXAMPLE COMPLETED!")
    print("="*70 + "\n")
    
    return times, S_total, S_spatial, params


if __name__ == "__main__":
    # Run the basic simulation
    times, signal, spatial, params = basic_simulation()
    
    # You can now access the results:
    # - times: array of time points
    # - signal: total signal S(t)
    # - spatial: spatially-resolved S_j(t)
    # - params: parameter object
    
    print("You can now:")
    print("  1. Modify N_atoms (line 28)")
    print("  2. Change scenario to 'b' for 1 THz (line 27)")
    print("  3. Adjust time range (lines 47-48)")
    print("\nTry it and run again!")
