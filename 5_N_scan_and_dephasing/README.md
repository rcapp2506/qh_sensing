# N-scan and dephasing analysis (thesis errata-corrige, Ch. Sensing)

Exact QuTiP study of the avalanche gain vs array size and under pure dephasing.
Same Hamiltonian and parameters as the production runs (scenario a, B=0,
facilitation Delta_gr = -V_rr, local seed at the chain centre;
Omega_gr/2pi = 0.2 MHz, V_rr/2pi = 12.5 MHz).

- `qutip_avalanche.py` — engine: `sesolve` (coherent, N=1–14) and `mesolve`
  (pure dephasing L_j = sqrt(Gamma_phi) sigma_z^j, N<=7). Run
  `python qutip_avalanche.py unitary` to regenerate the coherent scan.
- `lindblad_split.py` — independent split-operator integrator used to
  cross-validate `mesolve` (agreement to 2 decimal places).
- `n_scan_thesis_figs.py` — generates the two thesis figures
  (`amplification_smallN_readout.png`, `avalanche_dephasing.png`) in the house
  style; caches dephasing data in `dephasing_scan_data.npz`.
- `qutip_unitary_summary.csv` / `dephasing_scan_data.npz` — raw results
  (rule 5: data saved before plotting).

Key numbers: measured readout time Omega_gr*T_a ≈ 0.34 N (first maximum of S);
A_peak = 7.05 vs A_convention = 5.35 at N=11; gain sub-linear below N≈8 with
A(1)=1; threshold A=3 crossed at N≳4 (peak) / N≳7 (convention); at
Gamma_phi = 0.1 Omega_gr the early peak survives within ~10% and revivals damp
to a plateau ≈ 0.42 N.
