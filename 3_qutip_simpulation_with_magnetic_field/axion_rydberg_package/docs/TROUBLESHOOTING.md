# Troubleshooting Guide

Common issues and solutions for the Rydberg avalanche detector simulation package.

---

## 🔧 Installation Issues

### Issue 1: "pip install fails"

**Symptom**:
```
ERROR: Could not find a version that satisfies the requirement qutip
```

**Solutions**:

**A. Update pip**
```bash
pip install --upgrade pip
python -m pip install --upgrade pip
```

**B. Try conda instead**
```bash
conda install -c conda-forge qutip numpy matplotlib scipy
```

**C. Check Python version**
```bash
python --version
# Need: Python 3.8 or higher
```

### Issue 2: "QuTiP import error"

**Symptom**:
```python
ImportError: cannot import name 'Qobj' from 'qutip'
```

**Solutions**:

**A. Reinstall QuTiP**
```bash
pip uninstall qutip
pip install qutip>=4.7.0
```

**B. Check installation**
```python
import qutip
print(qutip.__version__)
# Should be >= 4.7.0
```

### Issue 3: "Module not found: scipy/numpy/matplotlib"

**Solution**: Install all dependencies
```bash
pip install -r requirements.txt
```

Or individually:
```bash
pip install numpy>=1.20
pip install scipy>=1.6
pip install matplotlib>=3.3
```

---

## 💻 Runtime Issues

### Issue 4: "Simulation taking too long"

**Symptom**: Simulation runs for >10 minutes

**Causes & Solutions**:

**A. System too large**
```python
# Problem:
N_atoms = 13  # 8192 states!

# Solution:
N_atoms = 9   # 512 states (much faster)
```

**B. Too many time points**
```python
# Problem:
n_times = 200

# Solution:
n_times = 50  # Still sufficient
```

**C. Too many B-field points**
```python
# Problem:
B_scan = [0, 1, 2, 3, 4, 5, 6, 7]

# Solution:
B_scan = [0, 5]  # Just endpoints
```

**Expected times**:
- N=9: ~1 minute
- N=11: ~3 minutes
- N=13: ~10 minutes

### Issue 5: "MemoryError"

**Symptom**:
```
MemoryError: Unable to allocate array
```

**Causes & Solutions**:

**A. System too large**
```python
N_atoms = 11  # Requires ~8 GB RAM
# Reduce to:
N_atoms = 9   # Requires ~2 GB RAM
```

**B. Check available RAM**
```bash
# Linux/Mac:
free -h

# Check you have at least 8 GB free
```

**C. Close other programs**
- Close browser tabs
- Close other Python instances
- Restart kernel if using Jupyter

### Issue 6: "Simulation crashes without error"

**Possible causes**:

**A. Out of memory (silent)**
- Reduce N_atoms
- Monitor memory usage

**B. Numerical instability**
- Check parameters are physical
- Ensure Hamiltonian is Hermitian
- Try different QuTiP solver options

**C. QuTiP version issue**
```bash
pip install --upgrade qutip
```

---

## 📊 Output Issues

### Issue 7: "No figures generated"

**Symptom**: Simulation completes but no PNG files

**Solutions**:

**A. Check current directory**
```bash
ls -lt *.png
# Should see recently created files
```

**B. Matplotlib backend issue**
```python
# At start of script:
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
```

**C. Save explicitly**
```python
save_fig = True  # Make sure this is set
```

### Issue 8: "Figures don't show"

**Symptom**: `plt.show()` does nothing

**Solutions**:

**A. Use non-interactive backend**
```python
# Figures are saved as PNG
# Open them with image viewer instead
```

**B. Or use interactive backend**
```python
import matplotlib
matplotlib.use('TkAgg')  # Or 'Qt5Agg'
```

**C. In Jupyter**
```python
%matplotlib inline
# Or:
%matplotlib notebook
```

### Issue 9: "Empty or corrupted figure"

**Solution**:
```python
# Ensure plot code completes before saving
plt.tight_layout()
plt.savefig(filename)
plt.close()  # Important!
```

---

## 🔬 Physical Issues

### Issue 10: "Amplification is negative or zero"

**Symptom**: S(t) = 0 or negative values

**Causes**:

**A. Facilitation condition not met**
```python
# Check:
print(f"Δ_gr + V_rr = {(params.Delta_gr + params.V_rr)/1e6:.3f} MHz")
# Should be close to 0!

# If not, adjust manually:
params.Delta_gr = -params.V_rr
```

**B. Wrong initial state**
```python
# Make sure you have:
psi0 = initial_state_single_photon(N, k=N//2)
# Not all ground state!
```

**C. Time too short**
```python
# Need sufficient time for avalanche
max_time_factor = 10  # Not 1!
```

### Issue 11: "Amplification too large"

**Symptom**: S(T_a) >> N_atoms

**Causes**:

**A. Time integration went too long**
```python
# Avalanche saturates at S ~ N
# Check your max_time_factor
```

**B. Double counting**
```python
# Make sure you're not summing twice
S_total = np.sum(S_spatial, axis=0)  # Correct
# Not: S_total = 2 * np.sum(...)
```

### Issue 12: "No avalanche observed"

**Symptom**: S(t) stays ~1 (no growth)

**Diagnose**:

**A. Check facilitation**
```python
params.print_summary()
# Look at: "Facilitation check"
```

**B. Check parameters**
```python
print(f"V_rr = {params.V_rr/1e6:.3f} MHz")
print(f"Ω_gr = {params.Omega_gr/1e6:.3f} MHz")
# V_rr should be >> Ω_gr
```

**C. Interaction too weak**
```python
# Increase interaction:
params.V_rr_0 = 2 * np.pi * 20e6  # Instead of 12.5 MHz
```

---

## 🧲 Magnetic Field Issues

### Issue 13: "B-field results don't make sense"

**Symptom**: Amplification increases with B (should decrease)

**Check**:

**A. Field-modified interactions**
```python
# Should have:
V_rr(B) < V_rr(0)
# Suppression due to mixing
```

**B. Zeeman correction**
```python
# Should adjust:
Delta_gr(B) = Delta_gr(0) + Zeeman_shift
```

**C. Range validity**
```python
# Code valid up to ~5-7 T
# Above that, need full diamagnetic calculation
```

### Issue 14: "Dark counts not decreasing with cooling"

**Symptom**: Same dark rate at T=4K and T=0.5K

**Check**:

**A. Exponential suppression implemented?**
```python
def thermal_excitation_rate(self):
    boltzmann = np.exp(-Delta_E / (k_B * self.T))
    return Gamma_0 * boltzmann
```

**B. Energy gap correct?**
```python
Delta_E = 54e9 * h_bar * 2 * np.pi  # ~54 GHz
# This should be in Joules!
```

---

## 🎯 Axion Physics Issues

### Issue 15: "Axion conversion power unrealistic"

**Symptom**: P >> 10⁻²² W or P << 10⁻²⁵ W

**Check**:

**A. Units correct?**
```python
# Axion mass in eV, not J
self.m_a = axion_mass_ueV * 1e-6 * 1.602176634e-19 / c**2
```

**B. DM density**
```python
# Should be ~ 0.3 GeV/cm³
self.rho_DM = 0.3e9 * 1.602176634e-19 / c**2  # kg/m³
```

**C. Simplified formula**
```python
# Code uses simplified version
# Actual power depends on cavity Q, B², volume
# ~10⁻²² W is order-of-magnitude target
```

---

## 🐛 Common Errors

### Error 1: "Hamiltonian is not Hermitian"

**Cause**: Bug in Hamiltonian construction

**Fix**:
```python
H = build_hamiltonian_magnetic(N, params)
print(f"Hermitian: {H.isherm}")

# If False:
H = (H + H.dag()) / 2  # Force Hermitian
```

### Error 2: "State not normalized"

**Symptom**: `psi.norm() != 1.0`

**Fix**:
```python
psi0 = psi0.unit()  # Normalize
print(f"Norm: {psi0.norm()}")  # Should be 1.0
```

### Error 3: "Index out of bounds"

**Cause**: Accessing wrong array element

**Fix**:
```python
# Python is 0-indexed!
# For N=11 atoms, indices are 0-10, not 1-11
for j in range(N):  # Correct: 0 to N-1
    ...
```

### Error 4: "Division by zero"

**Cause**: Dark rate or time = 0

**Fix**:
```python
snr = S / max(noise, 1e-10)  # Avoid division by 0
```

---

## 🔍 Debugging Tips

### Tip 1: Start Simple

```python
# Minimal working example:
N = 5  # Very small
B = 0.0  # No field
T = 4.0
max_time_factor = 2
n_times = 20

# Should run in <10 seconds
```

### Tip 2: Check Intermediate Results

```python
# After simulation:
print(f"Initial state norm: {psi0.norm()}")
print(f"Final state norm: {states[-1].norm()}")
print(f"Signal range: {signal.min()} to {signal.max()}")
print(f"Number of NaN: {np.sum(np.isnan(signal))}")
```

### Tip 3: Plot Diagnostics

```python
# Before final plot:
plt.figure()
plt.plot(times, signal, 'o-')
plt.xlabel('Time (s)')
plt.ylabel('Signal')
plt.title('Debug: Signal vs Time')
plt.show()
```

### Tip 4: Use QuTiP Diagnostics

```python
# Check Hamiltonian properties:
print(f"H shape: {H.shape}")
print(f"H isherm: {H.isherm}")
print(f"H eigenenergies (sample): {H.eigenenergies()[:5]}")
```

### Tip 5: Memory Profiling

```python
import psutil
import os

process = psutil.Process(os.getpid())
print(f"Memory usage: {process.memory_info().rss / 1e9:.2f} GB")
```

---

## 💡 Performance Optimization

### Optimization 1: Reduce Hilbert Space

**Problem**: Simulation too slow

**Solutions**:

**A. Smaller system**
```python
N = 9  # Instead of 11 or 13
```

**B. Truncate high energy states** (advanced)
```python
# Only if you know what you're doing
# Requires custom Hamiltonian
```

### Optimization 2: Parallel Computing

**For multiple B-field points**:

```python
from joblib import Parallel, delayed

def run_single_B(B):
    return run_axion_detection_simulation(B_field=B, ...)

results = Parallel(n_jobs=4)(
    delayed(run_single_B)(B) for B in B_values
)
```

### Optimization 3: Save Intermediate Results

```python
# Save after long simulation:
np.savez('simulation_results.npz',
         times=times,
         signal=signal,
         spatial=spatial,
         B=B_field)

# Load later:
data = np.load('simulation_results.npz')
times = data['times']
signal = data['signal']
```

---

## 📞 Getting Help

### Before Asking for Help

1. ✅ Read this troubleshooting guide
2. ✅ Check your Python version (≥3.8)
3. ✅ Check QuTiP version (≥4.7.0)
4. ✅ Try minimal working example
5. ✅ Check error message carefully

### How to Report Issues

Include:

1. **System info**:
   ```python
   import sys, qutip, numpy, matplotlib
   print(f"Python: {sys.version}")
   print(f"QuTiP: {qutip.__version__}")
   print(f"NumPy: {numpy.__version__}")
   print(f"Matplotlib: {matplotlib.__version__}")
   ```

2. **Minimal code** that reproduces error

3. **Full error message** (copy-paste from console)

4. **What you expected** vs what you got

### Contact

**For code issues**: Check package README

**For physics questions**: See docs/PHYSICS_BACKGROUND.md

**For WISE-RED project**: Contact consortium members

---

## ✅ Quick Diagnostics Checklist

Run this before reporting issues:

```python
# Quick diagnostic script
import sys
import numpy as np
import matplotlib
import qutip

print("=== SYSTEM DIAGNOSTICS ===")
print(f"Python version: {sys.version}")
print(f"QuTiP version: {qutip.__version__}")
print(f"NumPy version: {np.__version__}")
print(f"Matplotlib version: {matplotlib.__version__}")
print(f"Matplotlib backend: {matplotlib.get_backend()}")

# Memory check
import psutil
mem = psutil.virtual_memory()
print(f"\nAvailable RAM: {mem.available / 1e9:.1f} GB")
print(f"Total RAM: {mem.total / 1e9:.1f} GB")

# Quick test
print("\n=== QUICK TEST ===")
try:
    from qutip import *
    H = sigmaz()
    psi0 = basis(2, 0)
    times = np.linspace(0, 1, 10)
    result = sesolve(H, psi0, times)
    print("✓ QuTiP working correctly")
except Exception as e:
    print(f"✗ QuTiP test failed: {e}")

print("\n=== DIAGNOSTICS COMPLETE ===")
```

Expected output:
```
=== SYSTEM DIAGNOSTICS ===
Python version: 3.x.x
QuTiP version: 4.7.x
...
Available RAM: >8.0 GB
✓ QuTiP working correctly
```

---

## 🎯 Common Workflows

### Workflow 1: First Time Setup

```bash
# 1. Install
pip install -r requirements.txt

# 2. Test
python examples/example_basic_axion.py

# 3. If works: proceed to main simulation
python code/axion_rydberg_detector_magnetic_field.py
```

### Workflow 2: Quick Parameter Scan

```python
# Fast scan for exploration
N = 9  # Small system
B_values = [0, 5]  # Endpoints only
n_times = 50  # Fewer points

results = scan_magnetic_field(B_values, N=N)
```

### Workflow 3: Production Run

```python
# Full quality simulation
N = 11  # Standard size
B_values = [0, 1, 3, 5, 7]  # Complete scan
n_times = 100  # High resolution

# Run overnight if needed
results = scan_magnetic_field(B_values, N=N)

# Save results
np.save('production_results.npy', results)
```

---

**Remember**: Most issues are due to:
1. Wrong Python/package versions
2. Insufficient RAM for N > 11
3. Matplotlib backend issues
4. Physical parameters not set correctly

**Start simple, scale up gradually!**

---

**Last Updated**: November 2024  
**Version**: 1.0.0  
**Status**: Complete
