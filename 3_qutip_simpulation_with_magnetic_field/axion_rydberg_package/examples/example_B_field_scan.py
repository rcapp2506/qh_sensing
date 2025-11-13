"""
Magnetic Field Scan Example

Systematic scan of detector performance across B-field range.
Tests compatibility with strong magnetic fields required for axion searches.
"""

import sys
sys.path.append('../code')

from axion_rydberg_detector_magnetic_field import *

# ============================================================================
# MAGNETIC FIELD SCAN
# ============================================================================

def custom_B_field_scan():
    """
    Custom magnetic field scan with user-defined parameters
    """
    print("="*70)
    print(" MAGNETIC FIELD SCAN EXAMPLE")
    print("="*70 + "\n")
    
    # Define scan parameters
    B_values = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]  # Tesla
    temperature = 4.0  # Kelvin
    N_atoms = 11       # Number of atoms
    
    print("Scan Configuration:")
    print(f"  B-field range: {min(B_values):.1f} to {max(B_values):.1f} T")
    print(f"  Number of points: {len(B_values)}")
    print(f"  Temperature: {temperature} K")
    print(f"  System size: N = {N_atoms} atoms")
    print()
    
    # Run scan
    print("Starting magnetic field scan...")
    print(f"(This will take ~{len(B_values)*2} minutes)\n")
    
    results = scan_magnetic_field(
        B_values=B_values,
        temperature=temperature,
        N=N_atoms
    )
    
    # Extract performance metrics
    print("\n" + "="*70)
    print(" SCAN RESULTS")
    print("="*70 + "\n")
    
    print(f"{'B (T)':<10} {'Amplif.':<12} {'Dark (Hz)':<15} {'Detected?':<12}")
    print("-"*70)
    
    for B in B_values:
        data = results[B]
        params = data['params']
        
        idx_opt = np.argmin(np.abs(data['times'] - params.T_a_optimal))
        S_opt = data['signal'][idx_opt]
        detected = "✓ YES" if S_opt > 3.0 else "✗ NO"
        
        print(f"{B:<10.1f} {S_opt:<12.2f} {params.dark_rate:<15.2e} {detected:<12}")
    
    print()
    
    # Generate comprehensive plots
    print("Generating analysis plots...")
    fig1 = plot_magnetic_field_comparison(results, save_fig=True)
    fig2 = plot_detector_performance_summary(results, save_fig=True)
    print("✓ Figures saved!\n")
    
    # Generate benchmarking table
    print("="*70)
    generate_benchmarking_table(results)
    
    # Analysis
    print("="*70)
    print(" CONCLUSIONS")
    print("="*70 + "\n")
    
    all_detected = all(
        results[B]['signal'][np.argmin(np.abs(
            results[B]['times'] - results[B]['params'].T_a_optimal
        ))] > 3.0
        for B in B_values
    )
    
    if all_detected:
        print("✓ Single-photon detection successful at ALL magnetic fields!")
        print(f"✓ Detector operational from {min(B_values)} to {max(B_values)} T")
        print("✓ WISE-RED Objective O3 validated!")
    else:
        print("⚠ Detection failed at some B-field values")
        print("→ Consider parameter optimization")
    
    print()
    
    return results


def fine_B_scan_around_optimal():
    """
    Fine scan around optimal B-field to study field dependence in detail
    """
    print("\n" + "="*70)
    print(" FINE B-FIELD SCAN (Advanced)")
    print("="*70 + "\n")
    
    # Fine scan around 5T
    B_fine = np.linspace(4.0, 6.0, 11)
    print(f"Fine scan: {len(B_fine)} points from {B_fine[0]} to {B_fine[-1]} T")
    print()
    
    results_fine = scan_magnetic_field(
        B_values=B_fine.tolist(),
        temperature=4.0,
        N=9  # Smaller system for speed
    )
    
    # Extract amplification vs B
    amplifications = []
    for B in B_fine:
        data = results_fine[B]
        idx_opt = np.argmin(np.abs(data['times'] - data['params'].T_a_optimal))
        amplifications.append(data['signal'][idx_opt])
    
    # Plot fine scan
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(B_fine, amplifications, 'o-', linewidth=2.5, markersize=8)
    ax.axhline(3.0, linestyle='--', color='red', label='Threshold')
    ax.set_xlabel('Magnetic Field (T)', fontsize=13)
    ax.set_ylabel('Amplification Factor', fontsize=13)
    ax.set_title('Fine B-Field Dependence', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'fine_B_scan_{timestamp}.png'
    plt.savefig(filename, dpi=300)
    print(f"Fine scan plot saved: {filename}\n")
    
    return results_fine


if __name__ == "__main__":
    # Run main B-field scan
    results = custom_B_field_scan()
    
    # Optional: Run fine scan
    response = input("\nRun fine B-field scan? (y/n): ")
    if response.lower() == 'y':
        results_fine = fine_B_scan_around_optimal()
    
    print("\n" + "="*70)
    print(" SCAN COMPLETE!")
    print("="*70)
    print("\nGenerated files:")
    print("  - axion_detector_B_scan_[timestamp].png")
    print("  - detector_performance_summary_[timestamp].png")
    print("  - fine_B_scan_[timestamp].png (if run)")
    print()
    print("Next: Analyze temperature dependence with example_temperature_scan.py")
