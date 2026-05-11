"""
G17 - Numerical exploration of single-photon absorption efficiency
       eta_eff(N) including cavity backaction from atomic ensemble.

Physical model (linear in cavity-atom coupling, valid for <b dagger b> << N):

  RESONANT regime (Delta = 0):
    eta_abs(N) = 2C(N) / (1 + 2C(N))           C(N) = N g^2/(kappa gamma_perp)
    Backaction = Purcell broadening of the cavity:
      kappa_eff(N) = kappa * (1 + 2 C(N))
    Cavity resonance is NOT shifted, only broadened.
    Consequence: eta_abs(N) saturates rapidly to 1; the cost of large N
    is a shorter cavity ringdown time (faster signal washout).

  DISPERSIVE regime (Delta != 0):
    eta_abs(N) = C_disp(N) / (1 + C_disp(N))
    Backaction = cavity dispersive shift:
      delta_omega_c(N) = N g^2 / Delta
    Lorentzian filter on the axion-photon coupling:
      L(N) = (kappa/2)^2 / [(kappa/2)^2 + delta_omega_c(N)^2]
    Effective efficiency: eta_eff(N) = eta_abs(N) * L(N).
    Result: eta_eff is non-monotonic; an optimal N* exists but the peak
    value of eta_eff is small unless |Delta| is carefully tuned.

Reference parameters (consistent with Sec. Limitations of Chapter 4):
  g  / (2 pi)        = 1 MHz       single-atom-cavity coupling
  kappa / (2 pi)     = 50 kHz      cavity linewidth (Q ~ 1e5 at 5 GHz)
  gamma_perp / (2 pi) = 1 kHz      Rydberg dephasing rate (n ~ 70)

Output: chapters/qs_figures/backaction_eta_eff_vs_N.png (two panels)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.size'] = 11
mpl.rcParams['axes.titlesize'] = 12
mpl.rcParams['axes.labelsize'] = 12
mpl.rcParams['legend.fontsize'] = 10
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['savefig.bbox'] = 'tight'

# ============================================================================
# Parameters (rad/s)
# ============================================================================
g          = 2*np.pi*1e6      # 2 pi * 1 MHz
kappa      = 2*np.pi*5e4      # 2 pi * 50 kHz   (Q = 1e5 at 5 GHz)
gamma_perp = 2*np.pi*1e3      # 2 pi * 1 kHz    (Rydberg dephasing)

# Cooperativities
C1_res = g**2 / (kappa * gamma_perp)        # resonant single-atom cooperativity
print(f"Single-atom resonant cooperativity C1 = {C1_res:.2e}")

# N range spanning 10 orders of magnitude
N_arr = np.logspace(0, 9, 800)

# ============================================================================
# (a) RESONANT regime
# ============================================================================
C_res = N_arr * C1_res
eta_abs_res = 2*C_res / (1.0 + 2*C_res)
kappa_eff_res = kappa * (1.0 + 2*C_res)

# N at which eta_abs reaches 0.5
N_half_res = 1.0/(2*C1_res)
print(f"Resonant: N at which eta_abs=0.5 is N_1/2 = {N_half_res:.2e}")

# ============================================================================
# (b) DISPERSIVE regime - scan multiple Delta values
# ============================================================================
Delta_values = [2*np.pi*1e7,    # 10 MHz
                2*np.pi*1e8,    # 100 MHz
                2*np.pi*1e9]    # 1 GHz
Delta_labels = [r'$\Delta/2\pi = 10$ MHz',
                r'$\Delta/2\pi = 100$ MHz',
                r'$\Delta/2\pi = 1$ GHz']
Delta_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

results_disp = []
for Delta in Delta_values:
    C1_disp = (g**2 / Delta**2) * gamma_perp / (kappa/2)
    C_disp = N_arr * C1_disp
    eta_abs_disp = C_disp / (1.0 + C_disp)

    delta_omega_c = N_arr * g**2 / Delta
    L_filter = (kappa/2)**2 / ((kappa/2)**2 + delta_omega_c**2)

    eta_eff_disp = eta_abs_disp * L_filter

    N_opt_idx = np.argmax(eta_eff_disp)
    N_opt = N_arr[N_opt_idx]
    eta_eff_max = eta_eff_disp[N_opt_idx]

    results_disp.append({
        'Delta': Delta,
        'eta_abs': eta_abs_disp,
        'L': L_filter,
        'eta_eff': eta_eff_disp,
        'N_opt': N_opt,
        'eta_max': eta_eff_max,
        'C1': C1_disp,
    })
    print(f"Delta/2pi = {Delta/(2*np.pi)/1e6:.0f} MHz: "
          f"N* = {N_opt:.2e}, eta_eff_max = {eta_eff_max:.2e}")

# ============================================================================
# PLOT
# ============================================================================
fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))

# ------------------------------------------------------------------
# Panel (a): RESONANT
# ------------------------------------------------------------------
ax = axes[0]

# Primary axis: eta_abs (left)
ax.semilogx(N_arr, eta_abs_res, 'g-', linewidth=2.8,
            label=r'$\eta_{\rm eff}(N) = \eta_{\rm abs}(N)$')
ax.axhline(1.0, color='gray', linestyle=':', alpha=0.4)

# Roberto's working point at N=11
N_work = 11
eta_at_N11 = eta_abs_res[np.argmin(np.abs(N_arr-N_work))]
ax.axvline(N_work, color='purple', linestyle='-', alpha=0.6, linewidth=1.5)
ax.plot([N_work], [eta_at_N11], 'p', color='purple', markersize=14, zorder=5)
ax.annotate(rf'$N\!=\!11$ (this work)' + '\n' + rf'$\eta_{{\rm eff}}\approx{eta_at_N11:.3f}$',
            xy=(N_work, eta_at_N11), xytext=(40, 0.6),
            color='purple', fontsize=10, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='purple', alpha=0.7))

ax.set_xlabel(r'Number of atoms $N$')
ax.set_ylabel(r'Single-photon absorption $\eta_{\rm eff}$', color='g')
ax.tick_params(axis='y', labelcolor='g')
ax.set_title(r'Resonant regime $\Delta=0$: monotonic, no detuning penalty', pad=10)
ax.set_ylim([0, 1.15])
ax.set_xlim([1, 1e9])
ax.grid(True, alpha=0.3, which='both')
ax.legend(loc='center right', framealpha=0.9)
# Panel label (a)
ax.text(0.04, 0.94, '(a)', transform=ax.transAxes,
        fontsize=18, fontweight='bold', va='top', ha='left',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                  edgecolor='black', alpha=0.85), zorder=10)

# Secondary axis: kappa_eff/(2pi) (Purcell broadening)
ax2 = ax.twinx()
ax2.loglog(N_arr, kappa_eff_res/(2*np.pi), 'b--', linewidth=2.0,
           alpha=0.7, label=r'$\kappa_{\rm eff}(N)$ (Purcell)')
ax2.set_ylabel(r'$\kappa_{\rm eff}/2\pi$ (Hz, dashed)', color='b')
ax2.tick_params(axis='y', labelcolor='b')
ax2.set_ylim([1e4, 1e15])
ax2.legend(loc='lower right', framealpha=0.9)

# ------------------------------------------------------------------
# Panel (b): DISPERSIVE - multiple Delta values
# ------------------------------------------------------------------
ax = axes[1]

for r, label, color in zip(results_disp, Delta_labels, Delta_colors):
    ax.loglog(N_arr, r['eta_eff'], '-', linewidth=2.5, color=color,
              label=rf'{label}: $N^*\!\approx\!{r["N_opt"]:.0e}$, '
                    rf'$\eta_{{\max}}\!\approx\!{r["eta_max"]:.0e}$')
    # Mark the maximum
    ax.plot([r['N_opt']], [r['eta_max']], 'p', color=color, markersize=12,
            zorder=5, markeredgecolor='black', markeredgewidth=0.5)

ax.set_xlabel(r'Number of atoms $N$')
ax.set_ylabel(r'Effective efficiency $\eta_{\rm eff}(N) = \eta_{\rm abs}\,L$')
ax.set_title(r'Dispersive regime $\Delta \neq 0$: $\delta\omega_c\!=\!Ng^2\!/\Delta$ detunes cavity, non-monotonic', pad=10)
ax.set_ylim([1e-12, 2])
ax.set_xlim([1, 1e9])
ax.grid(True, alpha=0.3, which='both')
ax.legend(loc='lower center', framealpha=0.9, fontsize=9, ncol=1)
# Panel label (b)
ax.text(0.04, 0.94, '(b)', transform=ax.transAxes,
        fontsize=18, fontweight='bold', va='top', ha='left',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                  edgecolor='black', alpha=0.85), zorder=10)

# Interpretive annotation
ax.text(0.98, 0.97,
        r'Backaction dominates' + '\n' + r'before $\eta_{\rm abs} \to 1$',
        transform=ax.transAxes, ha='right', va='top',
        fontsize=10, fontstyle='italic',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='wheat', alpha=0.7))

# Title
fig.suptitle(r'Cavity backaction trade-off in single-photon Rydberg detection '
             r'($g/2\pi\!=\!1$ MHz, $\kappa/2\pi\!=\!50$ kHz, $\gamma_\perp/2\pi\!=\!1$ kHz)',
             fontsize=12.5, y=1.02)

plt.tight_layout()

# Output path (relative to script location)
script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(script_dir, 'backaction_eta_eff_vs_N.png')
plt.savefig(out_path)
print(f"\nSaved: {out_path}")
