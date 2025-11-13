# Quick Start - Axion Detection in 5 Minutes

Get your first axion detector simulation running in 5 minutes!

---

## ⚡ Super Quick (30 seconds)

```bash
# 1. Install
pip install qutip numpy matplotlib scipy

# 2. Run
cd code
python axion_rydberg_detector_magnetic_field.py

# 3. Done! Check the PNG files in current directory
```

**Expected time**: 3-5 minutes on standard laptop

---

## 📋 Step-by-Step

### Step 1: Verify Python

```bash
python --version
# Need: Python 3.8 or higher
```

### Step 2: Install Dependencies

```bash
cd axion_rydberg_package
pip install -r requirements.txt
```

**What gets installed**:
- `qutip` - Quantum simulation engine
- `numpy` - Numerical computing
- `matplotlib` - Plotting
- `scipy` - Scientific functions

### Step 3: Run Main Simulation

```bash
cd code
python axion_rydberg_detector_magnetic_field.py
```

**What happens**:
1. Simulates axion→photon conversion
2. Tests detector at B = 0, 1, 3, 5 Tesla
3. Computes amplification factors
4. Generates 2 professional figures
5. Creates benchmarking table

### Step 4: View Results

**Two figures created**:
```bash
ls -lt *.png | head -2
```

1. `axion_detector_B_scan_[timestamp].png`
2. `detector_performance_summary_[timestamp].png`

Open with any image viewer!

---

## 🎯 What You Should See

### Console Output (Excerpt)

```
================================================================================
 RYDBERG AVALANCHE DETECTOR FOR AXION DARK MATTER SEARCH
================================================================================

Simulation Configuration:
  N = 11 atoms
  T = 4.0 K
  B = [0.0, 1.0, 3.0, 5.0] T
  Axion mass = 20.0 μeV

================================================================================
Rydberg Axion Detector - Magnetic Field Configuration
================================================================================
  Magnetic field: B = 5.00 T
  Temperature: T = 4.0 K
  
  Field-modified interactions:
    V_rr(B)/(2π) = 11.406 MHz
    Suppression: 8.8%
  
  Zeeman shifts:
    |r⟩ shift = 67.938 MHz
    |e⟩ shift = 50.953 MHz
  
  Performance:
    T_a = 8.75 μs
    Dark rate = 2.37e-03 Hz

Axion Physics:
  Axion mass: 20.0 μeV
  Photon frequency: 4.83 GHz
  Conversion power: 1.00e-22 W
  Photon rate: 3.12e-09 photons/s

✓ Simulation completed!

Results:
  Signal at T_a: S(T_a) = 3.84
  Amplification factor: 3.8×
  Single-photon detection: YES ✓

================================================================================
 DETECTOR BENCHMARKING
================================================================================

Technology               Sensitivity      Dark Rate    T_op      B-field
                        (W)              (Hz)         (K)       compat.
--------------------------------------------------------------------------------
Rydberg (B=5.0T)        1.00e-22         2.37e-03     4.0       Yes
TES (100 mK)            1e-21            ~0.1         0.1       Limited
JJ (Pankratov22)        1e-22            ~1           0.01-0.1  Limited
SNSPD (Chi22)           1e-21            1e-6         1-4       No

Key findings:
  ✓ Rydberg detector achieves single-photon sensitivity (~10^-22 W)
  ✓ Compatible with high magnetic fields (0-5 T)
  ✓ Dark count rate competitive with superconducting technologies

ALL SIMULATIONS COMPLETED SUCCESSFULLY!
```

### Figure 1: B-Field Scan

**4 panels showing**:
- Top left: Signal S(t) for different B-fields
- Top right: Amplification vs B (all above threshold!)
- Bottom left: Dark count rates (log scale)
- Bottom right: Spatiotemporal avalanche at B=5T

**Key observation**: Detector works at ALL magnetic fields! ✅

### Figure 2: Performance Summary

**4 panels showing**:
- Amplification factors (3.8-5.2×)
- Dark counts (<0.01 Hz)
- Optimal times (~9 μs)
- Facilitation accuracy

**Key observation**: All WISE-RED objectives met! ✅

---

## 🔧 First Customization (2 minutes)

Want to test different conditions?

**Edit** `axion_rydberg_detector_magnetic_field.py`:

```python
# Find the main execution block (near end):
if __name__ == "__main__":
    
    # ========== Change these ==========
    N_atoms = 11              # Try 9 (faster) or 13 (more accurate)
    temperature = 4.0         # Try 1.0 K (lower noise)
    B_scan = [0.0, 2.0, 5.0]  # Custom B-field values
    axion_mass = 20.0         # Try 50 μeV (different frequency)
```

Save and run again!

---

## 📊 Understanding Your Results

### Key Numbers to Check

1. **Amplification Factor**: Should be > 3.0
   - This means single photon detected! ✓

2. **Dark Count Rate**: Should be < 0.05 Hz
   - WISE-RED target achieved! ✓

3. **Facilitation Error**: Should be < 0.1 MHz
   - Confirms Δ_gr + V_rr ≈ 0 ✓

4. **Zeeman Shifts**: Should increase with B
   - Physical consistency check ✓

### What Makes Good Results?

✅ S(T_a) > 3.0 for all B-fields (single-photon detection working)  
✅ Dark rate < 0.05 Hz (low background)  
✅ Amplification decreases smoothly with B (expected from mixing)  
✅ Avalanche visible in spatiotemporal plot (V-shape from center)

---

## 🎯 What's Next?

### Option 1: Try Different Axion Masses

```bash
cd examples
python example_axion_mass_scan.py
```

Scans axion mass from 10-100 μeV

### Option 2: Optimize Temperature

```bash
python example_temperature_scan.py
```

Tests T = 4 K, 1 K, 0.5 K, 0.3 K

### Option 3: Detailed Benchmarking

```bash
python example_benchmarking.py
```

Compares with all competing technologies

### Option 4: Understand the Physics

```bash
# Read the theory (in your browser or text editor)
docs/PHYSICS_BACKGROUND.md
docs/MAGNETIC_FIELD_EFFECTS.md
```

Complete derivations and explanations

---

## ⚠️ Common Issues

### Issue 1: "ModuleNotFoundError: No module named 'qutip'"

**Solution:**
```bash
pip install qutip numpy matplotlib scipy
```

### Issue 2: "Simulation taking too long"

**Solution:** Reduce system size
```python
N_atoms = 9  # Instead of 11
B_scan = [0, 5]  # Fewer points
```

### Issue 3: "Memory Error"

**Solution:** 
```python
N_atoms = 9  # Requires less RAM
```

### Issue 4: "Figures not showing"

**Solution:** Figures are saved as PNG!
```bash
ls -lt *.png
```

### Issue 5: "ImportError with QuTiP"

**Solution:** Update QuTiP
```bash
pip install --upgrade qutip
```

---

## 📚 Learn More

### For Understanding Physics
- **[docs/PHYSICS_BACKGROUND.md](../docs/PHYSICS_BACKGROUND.md)** - Complete theory
- **[docs/MAGNETIC_FIELD_EFFECTS.md](../docs/MAGNETIC_FIELD_EFFECTS.md)** - B-field effects
- **WISE-RED Proposal** (included in package)

### For Using the Code
- **[examples/example_basic_axion.py](../examples/example_basic_axion.py)** - Simplest usage
- **[examples/example_B_field_scan.py](../examples/example_B_field_scan.py)** - Custom scans
- **Console help**: `python axion_rydberg_detector_magnetic_field.py --help`

### For Comparing Technologies
- **[docs/BENCHMARKING.md](../docs/BENCHMARKING.md)** - Technology comparison
- **Benchmarking table** - Generated automatically

---

## ✅ Verification Checklist

After running, verify:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed
- [ ] Simulation completes without errors
- [ ] Two PNG files generated
- [ ] Console shows "COMPLETED SUCCESSFULLY"
- [ ] Amplification > 3 for all B-fields
- [ ] Dark rate < 0.05 Hz
- [ ] Facilitation condition |ΔE| < 0.1 MHz

All checked? **You're ready to explore!** 🎉

---

## 🎯 Quick Command Reference

```bash
# Full simulation (main script)
python code/axion_rydberg_detector_magnetic_field.py

# Basic example
python examples/example_basic_axion.py

# B-field scan (custom)
python examples/example_B_field_scan.py

# Temperature optimization
python examples/example_temperature_scan.py

# Benchmarking only
python examples/example_benchmarking.py

# View latest figures
ls -lt *.png | head -5

# Clean up old results
rm *.png
```

---

## 🔬 Physics Quick Reference

### Axion Detection Chain

1. **Axion** (dark matter) in galaxy halo
2. **Magnetic field** (5 T in cavity)
3. **Conversion** via Primakoff effect → photon
4. **Absorption** by Rydberg atom → 1 excitation
5. **Avalanche** via facilitation → N excitations
6. **Detection** via fluorescence imaging

### Key Equations

**Axion conversion**:
```
P ~ g_aγγ² · ρ_DM · B² · V · Q / m_a
```

**Avalanche amplification**:
```
S(t) ~ N · (Ω_gr · t)  [ballistic phase]
```

**Facilitation condition**:
```
Δ_gr + V_rr = 0  [Zeeman corrected]
```

### Target Performance

- **Sensitivity**: 10⁻²² W ✓
- **Dark counts**: <0.05 Hz ✓
- **B-field range**: 0-7 T ✓
- **Temperature**: 300 mK - 4 K ✓
- **Frequency**: GHz - THz ✓

---

## 💡 Pro Tips

### Speed Up Simulations

```python
N_atoms = 9           # Faster (512 states vs 2048)
n_times = 50          # Fewer time points
B_scan = [0, 5]       # Just endpoints
```

### Better Plots

```python
plt.rcParams['figure.dpi'] = 300  # High resolution
save_fig = True                    # Always save
```

### Save Numerical Data

```python
# At end of run_axion_detection_simulation():
np.savez('results.npz', 
         times=times, 
         signal=S_total,
         spatial=S_spatial,
         B=B_field)
```

---

## 🎓 For Students

**New to quantum physics?**
1. Start with basic example: `example_basic_axion.py`
2. Read: `docs/PHYSICS_BACKGROUND.md` (gentle introduction)
3. Watch console output (explains each step)
4. Modify one parameter at a time

**Already know quantum mechanics?**
1. Dive into main code: `axion_rydberg_detector_magnetic_field.py`
2. Read: `docs/MAGNETIC_FIELD_EFFECTS.md` (technical details)
3. Try custom scans
4. Compare with your own calculations

**Expert in Rydberg physics?**
1. Check Hamiltonian construction
2. Validate against [Nil24] paper
3. Extend to your specific system
4. Contribute improvements!

---

**Time invested**: 5 minutes  
**Results**: Professional axion detector simulation  
**Next**: Explore parameter space and understand physics!

Happy detecting! 🔬🌌
