# Cavity Backaction Analysis (G17)

Numerical exploration of the single-photon absorption efficiency $\eta_{\rm eff}(N)$
of a Rydberg-atom ensemble coupled to a haloscope cavity, including cavity
backaction. Produces the figure `backaction_eta_eff_vs_N.png` referenced in
Chapter 4 of the thesis as `\label{fig:backaction}`.

## Physical model (linear in cavity-atom coupling, valid for `<b dagger b> << N`)

### Resonant regime ($\Delta = 0$):
- Absorption: $\eta_{\rm abs}(N) = 2C(N) / (1 + 2C(N))$ where $C(N) = N\, g^2/(\kappa \gamma_\perp)$
- Backaction: Purcell broadening $\kappa_{\rm eff}(N) = \kappa\,(1 + 2C(N))$
- Result: $\eta_{\rm abs}$ saturates rapidly to 1; the cost of large $N$ is faster signal washout via shorter cavity ringdown.

### Dispersive regime ($\Delta \neq 0$):
- Absorption: $\eta_{\rm abs}(N) = C_{\rm disp}(N) / (1 + C_{\rm disp}(N))$
- Backaction: cavity dispersive shift $\delta\omega_c(N) = N\, g^2 / \Delta$
- Lorentzian filter on axion-photon coupling: $L(N) = (\kappa/2)^2 / [(\kappa/2)^2 + \delta\omega_c(N)^2]$
- Effective: $\eta_{\rm eff}(N) = \eta_{\rm abs}(N)\,L(N)$
- Result: non-monotonic; finite optimum $N^*$ but peak value small unless $\Delta$ is fine-tuned.

## Reference parameters
- $g/(2\pi)        = 1$ MHz
- $\kappa/(2\pi)   = 50$ kHz  (corresponds to $Q \sim 10^5$ at 5 GHz)
- $\gamma_\perp/(2\pi) = 1$ kHz  (Rydberg dephasing rate, $n \sim 70$)

## Run
```
python3 backaction_eta_eff_vs_N.py
```

## Output
- `backaction_eta_eff_vs_N.png` (two panels, 13×5.2 inches at 300 DPI)
- Printed numerical values: $C_1$, $N_{1/2}$, and $N^*$, $\eta_{\rm max}$ for the three dispersive detunings.

## Provenance
Generated during Wave H (G17 closure) of the post-review revision of the PhD thesis manuscript. Reconstructed from session transcript on 2026-05-10 after the original copy was lost. Output PNG identical to the version committed at commit `49ba4b1` of `rcapp2506/PhDThesis`.
