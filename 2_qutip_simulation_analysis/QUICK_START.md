# Quick Start Guide - 5 Minutes to Results

Get your first avalanche THz detector simulation running in 5 minutes!

---

## ⚡ Super Quick (30 seconds)

```bash
# 1. Install
pip install qutip numpy matplotlib scipy

# 2. Run
cd code
python rydberg_avalanche_qutip.py

# 3. Done! Check the generated PNG files
```

---

## 📋 Step-by-Step

### Step 1: Check Python Version

```bash
python --version
# Need: Python 3.8 or higher
```

### Step 2: Install Dependencies

```bash
# Navigate to package directory
cd rydberg_thz_detector_package

# Install all requirements
pip install -r requirements.txt
```

**What gets installed:**
- `qutip` - Quantum toolbox (main simulation engine)
- `numpy` - Numerical arrays
- `matplotlib` - Plotting
- `scipy` - Scientific computing

### Step 3: Run Your First Simulation

```bash
cd code
python rydberg_avalanche_qutip.py
```

**What happens:**
1. Builds Hamiltonian for N=11 atoms
2. Simulates local THz excitation
3. Simulates collective THz excitation  
4. Generates 3 publication-quality figures
5. Prints detailed results

**Time:** ~1-2 minutes on standard laptop

### Step 4: View Results

Three PNG files created:
- `signal_evolution_local_[timestamp].png`
- `signal_evolution_collective_[timestamp].png`
- `comparison_local_vs_collective_[timestamp].png`

Open with any image viewer!

---

## 🎨 What You Should See

### Console Output (excerpt)

```
======================================================================
 AVALANCHE TERAHERTZ PHOTON DETECTION
======================================================================

Physical Parameters (Scenario a)
  System: N = 11 atoms, a₀ = 6.0 μm
  Facilitation check: Δ_gr + V_rr = 0.00e+00 Hz ✓
  Optimal time: T_a = 8.75 μs

Building Hamiltonian...
  Hilbert space dimension: 2048
  Hamiltonian is Hermitian: True

[Progress bar showing time evolution...]

✓ Simulation completed!

Results:
  Local: S(T_a) = 5.23 → Amplification 5.2×
  Collective: S(T_a) = 7.84 → Amplification 7.8×
  Enhancement: 1.50×

ALL SIMULATIONS COMPLETED SUCCESSFULLY!
```

### Figure 1: Local Excitation

You'll see:
- **Top panel**: Heatmap showing avalanche spreading from center
- **Bottom panel**: Signal S(t) growing linearly (ballistic phase)
- **Annotations**: Three phases marked (quadratic, ballistic, saturation)

### Figure 2: Collective Excitation

Similar layout but:
- Faster growth (red line above blue)
- More uniform spatial distribution
- Higher final signal

### Figure 3: Comparison

Direct comparison showing:
- Blue line (local) vs Red line (collective)
- Enhancement factor ~1.5× clearly visible
- Both reaching similar saturation

---

## 🔧 First Customization (1 minute)

Want to try a smaller system (faster simulation)?

**Edit** `rydberg_avalanche_qutip.py`:

```python
# Find this line (near end of file):
N_atoms = 11          # Default

# Change to:
N_atoms = 9           # Faster!
```

Save and run again. Simulation now takes ~15 seconds!

---

## 📊 Understanding Your Results

### Key Numbers to Look For

1. **Facilitation check**: Should be `0.00e+00 Hz ✓`
   - Confirms Δ_gr + V_rr = 0 (critical condition!)

2. **Amplification factor**: Typically 5-8× for N=11
   - Single photon → Multiple Rydberg atoms

3. **Enhancement factor**: Typically 1.4-1.6×
   - Collective better than local (quantum coherence)

4. **Optimal time T_a**: Around 8.75 μs for N=11
   - Time for avalanche to propagate across chain

### What Makes Good Results?

✓ S(T_a) > 3 for N=11 (good amplification)  
✓ Collective > Local (quantum enhancement working)  
✓ Linear growth phase visible in plot  
✓ V-shape in spatial heatmap (avalanche from center)

---

## 🎯 What Next?

### Option 1: Try Different Parameters

```bash
cd examples
python example_custom_parameters.py
```

This runs parameter scans (N, Ω_gr, etc.)

### Option 2: Understand the Physics

```bash
# Open in your text editor or browser
docs/PHYSICS_EXPLANATION.md
```

Explains:
- Why facilitation works
- Three phases of evolution
- Collective vs local difference

### Option 3: Advanced Analysis

```bash
cd examples
python example_analysis.py
```

Shows how to:
- Extract phase velocities
- Compute correlations
- Analyze entanglement

---

## ⚠️ Common Issues

### Issue 1: "ModuleNotFoundError: No module named 'qutip'"

**Solution:**
```bash
pip install qutip
```

### Issue 2: "Simulation taking forever"

**Solution:** Reduce N_atoms
```python
N_atoms = 9  # Instead of 11
```

### Issue 3: "Memory Error"

**Solution:** 
- Close other applications
- Reduce N_atoms to 7 or 9
- Use NumPy version instead (less memory)

### Issue 4: "Figures don't show"

**Solution:** Figures are saved as PNG files, check current directory!
```bash
ls -lt *.png | head -3
```

### Issue 5: "ImportError: cannot import name 'xx' from 'qutip'"

**Solution:** Update QuTiP
```bash
pip install --upgrade qutip
```

---

## 🚀 Alternative: NumPy Version

Don't have QuTiP or prefer standalone?

```bash
cd code
python rydberg_avalanche_numpy.py
```

**Pros:**
- No QuTiP dependency
- Easier to understand code
- Good for learning

**Cons:**
- Slower (~3× slower)
- Limited to N ≤ 11
- More verbose code

Same output, same figures!

---

## 📚 Learn More

Now that you have results, dive deeper:

1. **[USER_GUIDE.md](docs/USER_GUIDE.md)** - Complete walkthrough
2. **[PHYSICS_EXPLANATION.md](docs/PHYSICS_EXPLANATION.md)** - Theory
3. **[API_REFERENCE.md](docs/API_REFERENCE.md)** - Code documentation

---

## ✅ Quick Checklist

Before moving on, verify:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Simulation runs without errors
- [ ] Three PNG files generated
- [ ] Console shows "COMPLETED SUCCESSFULLY"
- [ ] Facilitation check shows `0.00e+00 Hz`
- [ ] Amplification factor > 3

All checked? **Congratulations!** You're ready to explore more! 🎉

---

## 🎯 Quick Command Reference

```bash
# Full simulation (QuTiP)
python code/rydberg_avalanche_qutip.py

# Fast version (NumPy)
python code/rydberg_avalanche_numpy.py

# Run all examples
python code/run_all_simulations.py

# View latest figures
ls -lt *.png | head -3

# Clean up old results
rm signal_*.png comparison_*.png
```

---

**Time invested**: 5 minutes  
**Results**: 3 professional figures + complete understanding  
**Next**: Explore physics or customize parameters!

Happy simulating! 🚀
