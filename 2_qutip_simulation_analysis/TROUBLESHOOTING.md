# Troubleshooting Guide

Common issues and their solutions.

---

## Installation Issues

### Problem: "pip: command not found"

**Solution:**
```bash
# Install pip first
python -m ensurepip --upgrade
```

### Problem: "ModuleNotFoundError: No module named 'qutip'"

**Solution:**
```bash
pip install qutip

# If that fails, try:
pip install --user qutip

# Or with conda:
conda install -c conda-forge qutip
```

### Problem: "ImportError: cannot import name 'xx' from 'qutip'"

**Cause:** Old QuTiP version

**Solution:**
```bash
pip install --upgrade qutip
# Should be qutip >= 4.7.0
```

### Problem: "ERROR: Could not build wheels for qutip"

**Solution** (Linux/Mac):
```bash
# Install build dependencies first
sudo apt-get install python3-dev  # Ubuntu/Debian
# or
brew install python3  # macOS

# Then retry
pip install qutip
```

---

## Runtime Issues

### Problem: "MemoryError"

**Symptoms:**
```
MemoryError: Unable to allocate XXX GB
```

**Solutions:**

1. **Reduce N_atoms**
   ```python
   N_atoms = 7  # Instead of 11
   ```

2. **Reduce time points**
   ```python
   n_times = 50  # Instead of 100
   ```

3. **Use NumPy version** (uses less memory)
   ```bash
   python rydberg_avalanche_numpy.py
   ```

4. **Close other applications**

5. **Use 64-bit Python** (if on 32-bit)

### Problem: "Simulation taking forever"

**Symptoms:** Progress bar stuck, hours of waiting

**Diagnosis:**
- N > 11? Exponential scaling!
- N = 11: Should take 1-3 minutes
- N = 13: Can take 10-20 minutes

**Solutions:**

1. **Be patient** for N=11 (it's normal)

2. **Reduce N** if too slow
   ```python
   N_atoms = 9  # Much faster
   ```

3. **Reduce time resolution**
   ```python
   n_times = 30  # Fewer points
   ```

4. **Check CPU usage**
   ```bash
   top  # Linux/Mac
   # QuTiP should use ~100% of one core
   ```

### Problem: "Figures not displayed"

**Symptoms:** Script finishes but no plots show

**Solutions:**

1. **Figures are saved!** Check current directory
   ```bash
   ls -lt *.png | head
   ```

2. **Use non-interactive backend**
   ```python
   import matplotlib
   matplotlib.use('Agg')  # Add at top of script
   ```

3. **Show explicitly**
   ```python
   import matplotlib.pyplot as plt
   plt.show(block=True)
   ```

### Problem: "RuntimeWarning: divide by zero"

**Cause:** Usually harmless, related to plotting empty arrays

**Solution:** Ignore or suppress:
```python
import warnings
warnings.filterwarnings('ignore')
```

---

## Physical Issues

### Problem: "Facilitation check fails"

**Symptoms:**
```
Facilitation check: Δ_gr + V_rr = 1.23e+06 Hz ✗
```

**Cause:** Bug in parameter setup

**Solution:**
```python
# Ensure this line is correct:
params.Delta_gr = -params.V_rr  # Must be NEGATIVE
```

### Problem: "Signal doesn't grow"

**Symptoms:** S(t) stays at 1.0 throughout

**Diagnosis:**
- Facilitation not working
- Hamiltonian issue
- Time range too short

**Solutions:**

1. **Check facilitation**
   ```python
   print(f"Δ_gr + V_rr = {params.Delta_gr + params.V_rr}")
   # Should be ~0
   ```

2. **Check Hamiltonian**
   ```python
   print(f"H is Hermitian: {H.isherm}")
   # Should be True
   ```

3. **Longer time**
   ```python
   max_time_factor = 15  # Instead of 10
   ```

### Problem: "Amplification too small"

**Symptoms:** S(T_a) < 2 for N=11

**Possible causes:**
- N too small (try N=11)
- T_a not optimal (check t_max)
- Ω_gr too large (check parameters)

**Solution:**
```python
# Use paper parameters exactly:
params = RydbergDetectorParams(scenario='a')
params.N = 11  # From paper
# Don't modify other parameters
```

### Problem: "Collective not better than local"

**Symptoms:** Enhancement factor < 1.1

**Diagnosis:**
- Bug in collective state
- N too small (need N ≥ 9)

**Solution:**
```python
# Check collective state norm
psi_coll = initial_state_collective_excitation(N)
print(f"Norm: {psi_coll.norm()}")  # Should be 1.0

# Increase N
N_atoms = 11  # Clearer effect
```

---

## Performance Issues

### Problem: "NumPy version much slower than expected"

**Symptoms:** N=9 takes >5 minutes

**Solutions:**

1. **Check NumPy installation**
   ```bash
   python -c "import numpy; numpy.show_config()"
   # Should show BLAS/LAPACK libraries
   ```

2. **Reinstall with MKL** (Intel CPUs)
   ```bash
   pip uninstall numpy
   pip install numpy --no-binary numpy
   ```

3. **Use QuTiP instead** (much faster)

### Problem: "QuTiP not using all CPU cores"

**Note:** QuTiP's `sesolve` is single-threaded by default

**Solution for multiple runs:**
```python
# Use joblib for parallel parameter scans
from joblib import Parallel, delayed

def run_single(N):
    # Your simulation code
    return result

results = Parallel(n_jobs=4)(
    delayed(run_single)(N) for N in [7, 9, 11, 13]
)
```

---

## Output Issues

### Problem: "Plots look wrong"

**Symptoms:** Empty heatmap, flat lines, strange colors

**Solutions:**

1. **Check signal values**
   ```python
   print(f"Signal range: {S_total.min():.2f} to {S_total.max():.2f}")
   # Should be: 1.0 to ~5-8 for N=11
   ```

2. **Check time array**
   ```python
   print(f"Times: {times[0]:.2e} to {times[-1]:.2e}")
   # Should be: 0 to ~1e-5 (10 μs)
   ```

3. **Reset matplotlib**
   ```python
   import matplotlib.pyplot as plt
   plt.close('all')
   plt.style.use('default')
   ```

### Problem: "Figures have wrong timestamps"

**Cause:** System clock issue

**Solution:**
```python
# Use custom filename
filename = 'my_simulation.png'
plt.savefig(filename, dpi=300)
```

---

## Platform-Specific Issues

### Windows

**Problem:** "Permission denied" when saving figures

**Solution:** Run as administrator or save to different directory

**Problem:** Path issues with examples

**Solution:**
```python
# Use absolute paths
import os
CODE_DIR = os.path.abspath('../code')
sys.path.append(CODE_DIR)
```

### macOS

**Problem:** "Matplotlib backend issue"

**Solution:**
```bash
# Install specific backend
pip install pyqt5
```

Then:
```python
import matplotlib
matplotlib.use('Qt5Agg')
```

### Linux

**Problem:** "Display not found"

**Cause:** No X server (SSH session, server)

**Solution:**
```python
# Use Agg backend
import matplotlib
matplotlib.use('Agg')  # No display needed
```

---

## Getting Help

### Before Asking for Help

1. **Check this guide** - Your issue is probably here

2. **Run basic example** - Does `example_basic.py` work?

3. **Check versions**
   ```bash
   python --version
   pip list | grep -E "(qutip|numpy|matplotlib|scipy)"
   ```

4. **Read error message** - Often tells you exactly what's wrong

5. **Simplify** - Try N=7, fewer time points

### Still Stuck?

**Include in your report:**
1. Full error message (copy-paste)
2. Python version
3. Package versions
4. Operating system
5. What you tried already
6. Minimal code that reproduces issue

### Quick Checks

```python
# Run this diagnostic script
import sys
print(f"Python: {sys.version}")

try:
    import numpy as np
    print(f"NumPy: {np.__version__}")
except:
    print("NumPy: NOT INSTALLED")

try:
    import qutip
    print(f"QuTiP: {qutip.__version__}")
except:
    print("QuTiP: NOT INSTALLED")

try:
    import matplotlib
    print(f"Matplotlib: {matplotlib.__version__}")
except:
    print("Matplotlib: NOT INSTALLED")

try:
    import scipy
    print(f"SciPy: {scipy.__version__}")
except:
    print("SciPy: NOT INSTALLED")
```

---

## FAQ

**Q: Can I run on Google Colab?**  
A: Yes! Use this notebook header:
```python
!pip install qutip
import sys
sys.path.append('/content/rydberg_thz_detector_package/code')
```

**Q: How to save simulation data?**  
A: Use NumPy:
```python
np.savez('results.npz', times=times, signal=S_total, 
         spatial=S_spatial)
```

**Q: Can I use GPU?**  
A: QuTiP doesn't use GPU. For GPU, you'd need to rewrite with JAX/TensorFlow.

**Q: How accurate are results?**  
A: Exact (within numerical precision) for pure state evolution. Matches paper.

**Q: Can I modify Hamiltonian?**  
A: Yes! Edit `build_hamiltonian_amplification()` function.

---

**Still having issues?** Check:
- [docs/USER_GUIDE.md](USER_GUIDE.md) for detailed explanations
- [docs/API_REFERENCE.md](API_REFERENCE.md) for function details
- Original paper for physics questions
