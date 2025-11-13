"""
Basic Axion Detection Example

Simplest possible usage of the Rydberg avalanche detector
for axion dark matter search.

This example runs a single simulation at B=5T, T=4K and checks
if single-photon detection is successful.
"""

import sys
sys.path.append('../code')

from axion_rydberg_detector_magnetic_field import *

# ============================================================================
# BASIC AXION DETECTION
# ============================================================================

def basic_axion_detection():
    """
    Simplest example: detect axion-converted photon at 5 Tesla
    """
    print("="*70)
    print(" BASIC AXION DETECTION EXAMPLE")
    print("="*70 + "\n")
    
    # Configuration
    B_field = 5.0      # Tesla (strong magnet)
    T_op = 4.0         # Kelvin (cryogenic)
    N_atoms = 11       # Number of atoms
    m_axion = 20.0     # μeV (QCD axion range)
    
    print("Configuration:")
    print(f"  Magnetic field: B = {B_field} T")
    print(f"  Temperature: T = {T_op} K")
    print(f"  System size: N = {N_atoms} atoms")
    print(f"  Axion mass: m_a = {m_axion} μeV")
    print()
    
    # Run simulation
    print("Running simulation...")
    print("(This will take ~1-2 minutes)\n")
    
    times, signal, spatial, params, axion = run_axion_detection_simulation(
        B_field=B_field,
        temperature=T_op,
        N=N_atoms,
        max_time_factor=8,
        n_times=80,
        axion_mass_ueV=m_axion
    )
    
    # Analyze results
    print("\n" + "="*70)
    print(" ANALYSIS")
    print("="*70 + "\n")
    
    # Find signal at optimal time
    idx_opt = np.argmin(np.abs(times - params.T_a_optimal))
    S_opt = signal[idx_opt]
    
    print(f"Detector Performance:")
    print(f"  Initial signal: S(0) = {signal[0]:.4f}")
    print(f"  Signal at T_a: S(T_a) = {S_opt:.2f}")
    print(f"  Final signal: S(t_max) = {signal[-1]:.2f}")
    print()
    
    print(f"Amplification:")
    print(f"  Factor: {S_opt:.1f}×")
    print(f"  1 photon → {S_opt:.1f} Rydberg atoms")
    print()
    
    # Detection decision
    threshold = 3.0
    detected = S_opt > threshold
    
    print(f"Detection:")
    print(f"  Threshold: {threshold:.1f} atoms")
    print(f"  Status: {'✓ DETECTED' if detected else '✗ NOT DETECTED'}")
    print(f"  Confidence: {100*S_opt/params.N:.1f}% of maximum")
    print()
    
    # Background
    print(f"Background:")
    print(f"  Dark count rate: {params.dark_rate:.2e} Hz")
    print(f"  Signal/Noise: {S_opt/max(params.dark_rate*params.T_a_optimal, 1e-6):.1e}")
    print()
    
    # Axion physics
    print(f"Axion Physics:")
    print(f"  Photon frequency: {axion.photon_frequency()/1e9:.2f} GHz")
    print(f"  Conversion power: {axion.conversion_power():.2e} W")
    print(f"  Photon rate: {axion.photon_rate():.2e} photons/s")
    print()
    
    if detected:
        print("="*70)
        print(" ✓ SINGLE-PHOTON AXION DETECTION SUCCESSFUL!")
        print("="*70)
    else:
        print("="*70)
        print(" ✗ Detection failed - consider optimizing parameters")
        print("="*70)
    
    return detected, S_opt, params, axion


if __name__ == "__main__":
    # Run the basic example
    detected, amplification, params, axion_params = basic_axion_detection()
    
    print("\nNext steps:")
    print("  1. Try different magnetic fields: B = 1, 3, 7 T")
    print("  2. Optimize temperature: T = 1, 0.5, 0.3 K")
    print("  3. Scan axion mass: m_a = 10-100 μeV")
    print("  4. Run full B-field scan: example_B_field_scan.py")
    print()
    
    # Save key results
    results = {
        'B_field': 5.0,
        'temperature': 4.0,
        'amplification': amplification,
        'detected': detected,
        'dark_rate': params.dark_rate
    }
    
    print(f"Results summary: {results}")
