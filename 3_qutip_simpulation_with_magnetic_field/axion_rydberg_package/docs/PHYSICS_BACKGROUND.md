# Physics Background - Rydberg Avalanche Detection

Complete theoretical foundation for axion detection using Rydberg atoms.

---

## 📚 Table of Contents

1. [Rydberg Atoms Basics](#rydberg-atoms-basics)
2. [Avalanche Amplification Mechanism](#avalanche-amplification)
3. [Magnetic Field Effects](#magnetic-field-effects)
4. [Axion Physics](#axion-physics)
5. [Detection Protocol](#detection-protocol)
6. [Mathematical Framework](#mathematical-framework)

---

## 🔬 Rydberg Atoms Basics

### What are Rydberg Atoms?

**Rydberg atoms** are atoms with one or more electrons excited to very high principal quantum numbers (n >> 1, typically n > 10).

**Key properties**:
- **Large size**: Orbital radius ~ n² × a₀ (Bohr radius)
- **Strong dipole moments**: d ~ n² (atomic units)
- **Long-range interactions**: V ~ C₆/r⁶ where C₆ ~ n¹¹
- **Tunable energy levels**: ΔE ~ 1/n² (covers GHz-THz)
- **Long lifetimes**: τ ~ n³ (microseconds to milliseconds)

### Energy Level Structure

For alkali atoms (e.g., Rb, Cs):

```
E_n = -Ry / (n - δ_ℓ)²

where:
- Ry = 13.6 eV (Rydberg constant)
- n = principal quantum number
- δ_ℓ = quantum defect (depends on ℓ)
```

**Example**: Rb 68S state
- Energy: ~54 GHz below ionization
- Orbital radius: ~150 nm
- Lifetime: ~100 μs

### Why Rydberg for Detection?

1. **Giant dipole transitions**: d ~ 10³ × d_ground
   - Strong coupling to EM fields
   - Efficient photon absorption

2. **Strong interactions**: V_rr ~ MHz at μm distances
   - Enable collective effects
   - Avalanche amplification possible

3. **Tunability**: Frequency set by quantum numbers
   - Same atom: GHz to THz
   - No hardware changes needed

4. **Calculable**: Hydrogen-like states
   - No device variability
   - Intrinsic calibration (SI-traceable)

5. **Decoupled**: Effective T_quantum << T_environment
   - Low thermal noise
   - Works at elevated temperatures

---

## ⚡ Avalanche Amplification Mechanism

### Physical Principle

**Key insight**: Rydberg interactions can be engineered to facilitate (rather than blockade) excitations.

### Facilitation Process

**Step 1: Initial excitation**
```
|g⟩ + ℏω → |r⟩     (photon absorption)
```
One atom excited to Rydberg state |r⟩

**Step 2: Interaction shift**
```
|r⟩₁ + |g⟩₂ → |r⟩₁ + |g'⟩₂
```
Atom 1 in |r⟩ shifts energy of nearby atom 2 by V_rr

**Step 3: Resonant transition**
```
|g'⟩₂ + ℏω → |r⟩₂
```
If V_rr matches laser detuning, atom 2 excited!

**Step 4: Cascade**
```
|r⟩₁ + |r⟩₂ → excite atom 3, 4, ...
```
Avalanche spreads through ensemble

### Facilitation Condition

**Critical requirement**:
```
Δ_gr + V_rr ≈ 0
```

where:
- Δ_gr = laser detuning from |g⟩→|r⟩
- V_rr = Rydberg-Rydberg interaction

**Interpretation**: 
- Isolated atom: off-resonance (Δ_gr ≠ 0)
- Near Rydberg atom: on-resonance (Δ_gr + V_rr ≈ 0)
- Result: Conditional excitation → facilitation!

### Ballistic Expansion Phase

In the **facilitation regime**:

```
S(t) ∝ N_excited(t) ~ Ω_gr · t
```

**Linear growth** (not exponential!) because:
- Excitations spread from boundaries
- Ballistic motion (1D/2D/3D)
- Limited by geometry

**Amplification factor**:
```
A = S(T_a) / S(0) ~ N_atoms
```

For N=11 atoms: A ~ 5-8×

### Spatial Correlations

**Key advantage**: Avalanche creates **spatial structure**

```
⟨n_r(i) n_r(j)⟩ > ⟨n_r(i)⟩⟨n_r(j)⟩    (i ≠ j nearby)
```

**Consequence**: 
- Signal has correlations
- Noise does not
- Can suppress readout noise!

**V-shaped pattern**: Avalanche from center spreads outward

---

## 🧲 Magnetic Field Effects

### Zeeman Effect

**Energy shift** in magnetic field B:

```
ΔE_Zeeman = μ_B · g_J · m_J · B
```

where:
- μ_B = Bohr magneton (9.27×10⁻²⁴ J/T)
- g_J = Landé g-factor (~2 for S, ~3/2 for P)
- m_J = magnetic quantum number

**For Rydberg states** (n~70):
```
ΔE_Zeeman ~ 70 MHz per Tesla (for m_J = ±1/2)
```

### State Mixing

At high B-fields, different ℓ,m states mix:

```
|n,ℓ,m⟩_B = Σ c_ℓ'(B) |n,ℓ',m'⟩_0
```

**Effect on interactions**:
- Pure S-S: V_SS = C₆/r⁶
- Mixed states: V_mixed < V_SS (suppression)

**Empirical scaling**:
```
V_rr(B) ≈ V_rr(0) · [1 - α(B/B₀)²]

where:
- B₀ ~ 1 T (characteristic scale)
- α ~ 0.1-0.2 (mixing strength)
```

### Modified Facilitation

**Zeeman correction** to detuning:

```
Δ_gr(B) = Δ_gr(0) + [ΔE_r(B) - ΔE_g(B)]
```

**Facilitation condition becomes**:
```
Δ_gr(B) + V_rr(B) ≈ 0
```

Must re-tune laser or accept reduced efficiency

### Diamagnetic Regime

At **very high fields** (B > 5 T for n~70):

```
E_B = ℏω_c = e·B/(2m_e) ~ E_Coulomb
```

Energy levels become **complex** (no simple formula)

**Consequence**: Need full numerical calculation
- Mixing of many states
- Energy shifts ~ GHz at 10 T
- Interactions modified significantly

**WISE-RED strategy**: Stay below diamagnetic regime
- B < 5-7 T: Perturbative treatment OK
- This simulation: Valid up to ~5 T

---

## 🌌 Axion Physics

### Axion Dark Matter

**Axions**: Hypothetical pseudo-scalar particles
- Mass: m_a ~ 1-1000 μeV (very light!)
- Coupling: g_aγγ ~ 10⁻¹⁵ GeV⁻¹
- Origin: Solution to strong CP problem
- Cosmology: Dark matter candidate

**Dark matter halo**:
```
ρ_DM ~ 0.3 GeV/cm³ (local density)
v_DM ~ 10⁻³ c (velocity dispersion)
```

### Primakoff Conversion

**In magnetic field**, axions convert to photons:

```
a + B → γ
```

**Conversion probability**:
```
P_aγ ~ (g_aγγ · B · L)²

where:
- L = interaction length
- B = magnetic field
```

**In cavity** (resonant enhancement):

```
P_aγ → P_aγ · Q · C

where:
- Q = quality factor (~10⁵)
- C = form factor (~0.5)
```

### Photon Properties

**Frequency** (from mass-energy):
```
f = m_a c² / h
  ≈ 4.8 GHz × (m_a / 20 μeV)
```

**Power** (in cavity):
```
P ~ g_aγγ² · ρ_DM · B² · V · Q · C / m_a
  ~ 10⁻²² W (for typical parameters)
```

**Photon rate**:
```
R = P / (h·f)
  ~ 10⁻⁹ photons/second
```

**Detection challenge**: 
- Extremely low power!
- Need single-photon sensitivity
- Must work in strong B-field
- Require low background

### Haloscope Experiments

**Existing experiments**:
- ADMX (USA): B=7-9 T, T~100 mK, Q~10⁵
- HAYSTAC (USA): B=8-9 T, T<100 mK, SQL amplifiers
- CAPP (Korea): Multiple cavities
- ORGAN (Australia): High frequency

**Current detectors**:
- JJ amplifiers (Josephson junctions)
- Squeezed state receivers
- TES bolometers

**Limitations**:
- ❌ B-field intolerant (JJ)
- ❌ Narrow bandwidth
- ❌ Complex cryogenics
- ❌ Not tunable

**WISE-RED advantage**:
- ✅ B-field compatible
- ✅ Broad bandwidth
- ✅ Works at 4 K (simpler)
- ✅ Tunable GHz-THz

---

## 🎯 Detection Protocol

### Complete Detection Chain

**1. Initialization** (t < 0)
```
All atoms in ground state: |ψ⟩ = |g⟩⊗N
```

**2. Photon absorption** (t = 0)
```
|g⟩_k + γ → |r⟩_k
Single atom k excited
```

**3. Laser pulse** (0 < t < T_a)
```
Apply Ω_gr on |g⟩→|r⟩ with detuning Δ_gr
Facilitation condition: Δ_gr + V_rr ≈ 0
```

**4. Avalanche** (t ~ T_a)
```
|r⟩_k → |r⟩_k + |r⟩_{k±1} → ... → N |r⟩
Linear spread: S(t) ~ Ω_gr · t
```

**5. Readout** (t = T_a)
```
Fluorescence imaging: count N_Rydberg
Threshold: N_Rydberg > 3 → detected!
```

### Optimal Timing

**Amplification time**:
```
T_a = N / Ω_gr ~ 10 μs
```

**Why not longer?**
- Decoherence: τ_coh ~ 100 μs
- Dark counts: R_dark · T_a should be << 1
- Readout: faster = higher rate

### Dark Count Sources

**Thermal excitations**:
```
R_thermal ~ Γ_0 · exp(-ΔE / k_B T)
```

At T=4 K, ΔE~54 GHz:
```
R_thermal ~ 10⁻³ Hz (negligible!)
```

**Stray light**:
```
R_stray ~ η_laser · ε_scatter
```
Can be suppressed with filters

**Collisions** (in vapor):
```
R_collision ~ n · σ · v ~ 10² Hz at 300 K
```
Solved by: use cold atoms (T<1 μK)!

### Signal-to-Noise Ratio

**Signal**: S = A × 1 = 5-8 atoms

**Noise**: N ~ √(R_dark · T_a + N_readout²)

For T=4 K, T_a=10 μs:
```
R_dark ~ 10⁻³ Hz
N_dark ~ √(10⁻³ × 10⁻⁵) ~ 10⁻⁴ (negligible!)
```

**Readout noise**: Typically N_readout ~ 0.1-1 atom

**Result**: SNR ~ 5-50 (excellent!)

---

## 📐 Mathematical Framework

### Hamiltonian

**Full system Hamiltonian**:

```
H = H_laser + H_detuning + H_interaction

H_laser = Ω_gr Σⱼ (σ_+^j + σ_-^j)

H_detuning = Δ_gr(B) Σⱼ n_r^j

H_interaction = Σⱼ V_rr(r_j,r_{j+1},B) n_r^j n_r^{j+1}
```

where:
- σ_± = raising/lowering operators
- n_r = Rydberg projector
- Ω_gr(B) = Rabi frequency (field-modified)
- Δ_gr(B) = detuning (Zeeman-corrected)
- V_rr(B) = interaction (mixing-suppressed)

### Time Evolution

**Schrödinger equation**:
```
iℏ ∂|ψ(t)⟩/∂t = H |ψ(t)⟩
```

**Formal solution**:
```
|ψ(t)⟩ = exp(-iHt/ℏ) |ψ(0)⟩
```

**Observables**:
```
⟨n_r^j(t)⟩ = ⟨ψ(t)| n_r^j |ψ(t)⟩
S(t) = Σⱼ ⟨n_r^j(t)⟩
```

### Analytical Estimates

**Early time** (t << T_a, perturbative):
```
S(t) ≈ 1 + (Ω_gr²/|Δ_gr|) t²
```
Quadratic growth

**Facilitation regime** (Δ_gr + V_rr ≈ 0):
```
S(t) ≈ Ω_gr · t
```
Linear (ballistic) growth

**Late time** (t >> T_a):
```
S(t) → N · p_ss
```
Saturation to steady-state

### Parameter Scaling

**Optimal amplification**:
```
A_max ~ N^α

where α ≈ 1 (linear scaling)
```

**Critical density**:
```
n_crit ~ (a₀/r_blockade)^d

where:
- r_blockade ~ (C₆/Ω_gr)^{1/6}
- d = dimensionality
```

**Sensitivity**:
```
P_min ~ (ℏω / T_integration) / √A
      ~ 10⁻²² W for A~5, T_int~1s
```

---

## 🔗 Key Equations Summary

### Rydberg Properties
```
Orbital radius: r_n ~ n² a₀
Energy: E_n ~ -Ry/n²
Dipole moment: d_n ~ n² e·a₀
Lifetime: τ_n ~ n³
Interaction: C₆ ~ n¹¹
```

### Facilitation
```
Condition: Δ_gr + V_rr = 0
Growth: S(t) ~ Ω_gr · t
Amplification: A ~ N
```

### Magnetic Field
```
Zeeman: ΔE = μ_B g_J m_J B
Mixing: V(B) ~ V₀[1 - α(B/B₀)²]
Correction: Δ_gr(B) = Δ_gr(0) + δE_Zeeman
```

### Axion
```
Frequency: f = m_a c²/h
Power: P ~ g_aγγ² ρ_DM B² V Q / m_a
Rate: R = P/(hf)
```

### Detection
```
Signal: S = A × N_photon
Noise: N ~ √(R_dark T_a)
SNR: S/N ~ A / √(R_dark T_a)
```

---

## 📚 References

### Foundational Papers

**Rydberg Physics**:
- Saffman, Walker, Mølmer, Rev. Mod. Phys. 82, 2313 (2010)
- Adams, Pritchard, Shaffer, J. Phys. B 53, 012002 (2020)

**Avalanche Mechanism**:
- Nill et al., Phys. Rev. Lett. 133, 073603 (2024) ⭐
- Festa et al., Phys. Rev. A 105, 013109 (2022)
- Valado et al., Phys. Rev. A 93, 040701 (2016)

**Rydberg in B-fields**:
- Zimmerman et al., Phys. Rev. A 20, 2251 (1979)
- Braun et al., Phys. Rev. A 97, 043418 (2018)

**Axion Physics**:
- Sikivie, Phys. Rev. D 32, 2988 (1985)
- Zhong et al., Phys. Rev. D 97, 092001 (2018)
- Backes et al., Nature 590, 238 (2021)

### WISE-RED Publications

- Wadley et al., Nature Photonics 11, 40 (2017) - Parametric amplification
- Gallagher et al., Phys. Rev. Res. 4, 013031 (2022) - Cu₂O excitons
- Borowka et al., Nature Photonics 18, 32 (2024) - Room-T upconversion

---

**This document provides the complete theoretical foundation for understanding Rydberg avalanche detection of axion-converted photons in strong magnetic fields.**

**Status**: Complete  
**Level**: Advanced  
**Prerequisites**: Quantum mechanics, atomic physics  
**Applications**: WISE-RED WP1, WP2, WP3

---
