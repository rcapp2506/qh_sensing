# Avalanche velocity verification

This subdirectory contains the reproducibility material for the
avalanche propagation velocity quoted in Sec. 4.5 (Cap. 4) of the
thesis, alongside the V-shaped panel of the avalanche dynamics
figure.

## Quoted value

The manuscript reports

    v ≈ 5.5 μm/μs

for a lattice spacing a = 6 μm and a Rabi frequency Ω_gr / (2π) =
0.2 MHz, at zero magnetic field. The value is extracted from the
centre-of-mass of the right-propagating excitation front in the
simulated S_j(t) traces.

## How to reproduce

From the repository root:

    cd 2_qutip_simulation_analysis/velocity_verification
    python verify_avalanche_velocity.py

Requirements: `numpy`, `matplotlib`, `qutip` (cf.
`../rydberg_thz_detector_package/requirements.txt`). Runtime: a
few seconds on a recent CPU.

The script:

  1. Imports the zero-field simulation module
     (`rydberg_avalanche_qutip.py`) from the sibling directory.
  2. Runs a short, dense simulation (4 μs, 200 time points, N = 11)
     and a longer one (Ω_gr·t up to 25, 200 time points) for the
     overlay plot.
  3. Computes the velocity with three independent methods:
       - `v_centroid`: slope of the right-side centre-of-mass
         <Δj>(t). Reported value, ~ 5.46 μm/μs.
       - `v_peak_fit`: linear fit of distance vs first-peak time on
         right-side sites. Less robust to Rabi oscillations.
       - `v_leading_edge`: slope of the most-extreme site reached
         above a threshold S_j > 0.3. ~ 11.9 μm/μs.
  4. Produces two diagnostic figures (see below).

## Outputs

- **`avalanche_velocity_overlay.png`** -- the S_j(t) heatmap with
  three velocity hypotheses overlaid. Visual confirmation that the
  v = 5.5 μm/μs line traces the boundary of the high-intensity
  V-region (i.e., the slope that a reader would naturally identify
  with the V in panel (d) of Fig. 4.X).

- **`avalanche_centroid_trace.png`** -- the right-side centroid
  trajectory `<Δj>·a(t)` with the linear fit from which v_centroid
  is extracted, in the range t ∈ [0.1, 3.0] μs where the centroid
  motion is approximately linear before the front reaches the
  boundary of the chain.

## Cross-check against the with-B simulation

The same value is reproduced independently by the with-B-field
simulation in `3_qutip_simpulation_with_magnetic_field/...` at
B = 0:

    code path                                 |  v_centroid (μm/μs)
    ------------------------------------------|--------------------
    2_qutip_simulation_analysis (this folder) |  5.46
    3_qutip_..._with_magnetic_field at B = 0  |  5.47

The two codes share the same physical parameters and use compatible
QuTiP implementations of the facilitation Hamiltonian; agreement to
2 % is a sanity check that no implementation-specific artefact
contaminates the value.

## Comparison with naive estimates

For context, the most common back-of-envelope estimates for v in a
facilitation chain are

    v_naive  =  ν_gr · a                ≈ 1.2 μm/μs
    v_hop    =  2 · ν_gr · a            ≈ 2.4 μm/μs    (T_Rabi / 2 hopping)

The simulated v_centroid ≈ 5.5 μm/μs is a factor ~ π faster than
v_hop, consistent with the coherent facilitation regime
[Valado, PRA 2016; Festa, PRA Research 2022] in which collective
dynamics produces a front faster than the nearest-neighbour Rabi
flop estimate.
