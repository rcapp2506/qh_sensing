"""
Errata-corrige figures for Chapter "Quantum Sensing" (thesis house style).

Produces:
  chapters/qs_figures/amplification_smallN_readout.png
      (a) A(N), N=1-14, exact coherent scan: convention vs peak readout,
          linear production fit shown with its validity domain, threshold=3
      (b) readout time: convention T_a=N/Omega_gr vs measured argmax_t S
  chapters/qs_figures/avalanche_dephasing.png
      (a) S(t) at N=7 for Gamma_phi/Omega_gr in {0, 0.1, 0.5, 1} (mesolve)
      (b) peak & plateau amplification vs N at Gamma_phi=0.1 Omega_gr

Raw data saved alongside (rule 5 of the repo protocol):
  n_scan_unitary_summary.csv  (already produced by qutip_avalanche.py)
  dephasing_scan_data.npz

Engine: QuTiP (sesolve/mesolve), identical Hamiltonian and parameters to
rydberg_avalanche_qutip.py (scenario a, B=0, facilitation Delta_gr=-V_rr,
local seed at the chain centre).
"""
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from qutip_avalanche import run, Omega_gr

# ---- thesis house style (same rcParams as backaction_eta_eff_vs_N.py) ----
mpl.rcParams['font.size'] = 11
mpl.rcParams['axes.titlesize'] = 12
mpl.rcParams['axes.labelsize'] = 12
mpl.rcParams['legend.fontsize'] = 10
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['savefig.bbox'] = 'tight'

# ============================================================
# Load / compute data
# ============================================================
res = np.load("qutip_unitary_results.npy", allow_pickle=True).item()
Ns = sorted(res.keys())
A_conv = np.array([res[N]["A_analytic"] for N in Ns])
Ta_conv_us = np.array([res[N]["T_a_analytic"] * 1e6 for N in Ns])

def first_peak_time(r):
    """Time of the FIRST local maximum of S(t) (robust on oscillatory curves:
    for a quasi-periodic S the global argmax can land on a later revival)."""
    S = r["S"]; t = r["tlist"]
    for i in range(1, len(S) - 1):
        if S[i] >= S[i + 1] and S[i] > S[0]:
            return t[i], S[i]
    i = int(np.argmax(S)); return t[i], S[i]

Ta_meas_us = np.array([first_peak_time(res[N])[0] * 1e6 for N in Ns])
A_peak = np.array([first_peak_time(res[N])[1] for N in Ns])  # peak = first max

# dephasing runs (mesolve): S(t) at N=7 for several rates + scan N=2..7
N0 = 7
gammas = [0.0, 0.1, 0.5, 1.0]
import os
if os.path.exists("dephasing_scan_data.npz"):
    _d = np.load("dephasing_scan_data.npz")
    runsA = {g: {"S": _d[f"S_t_g{g}"], "tnorm": _d[f"tnorm_g{g}"]} for g in gammas}
    Ns_d = list(_d["Ns_d"])
    A_pk_uni = list(_d["A_peak_coherent"]); A_pk_d = list(_d["A_peak_dephased"])
    A_pl_d = list(_d["A_plateau_dephased"])
else:
    runsA = {g: run(N0, g * Omega_gr, n_time=200) for g in gammas}
    Ns_d = list(range(2, 8))
    A_pk_uni, A_pk_d, A_pl_d = [], [], []
    for N in Ns_d:
        rd = run(N, 0.1 * Omega_gr, n_time=180)
        A_pk_uni.append(res[N]["A_peak"])
        A_pk_d.append(rd["S"].max())
        A_pl_d.append(rd["S"][-30:].mean())

np.savez("dephasing_scan_data.npz",
         N0=N0, gammas=gammas,
         **{f"S_t_g{g}": runsA[g]["S"] for g in gammas},
         **{f"tnorm_g{g}": runsA[g]["tnorm"] for g in gammas},
         Ns_d=Ns_d, A_peak_coherent=A_pk_uni,
         A_peak_dephased=A_pk_d, A_plateau_dephased=A_pl_d)

# ============================================================
# Figure 1: small-N amplification + readout time
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.9, 5.4))

ax1.plot(Ns, A_peak, 'o-', color='tab:red', ms=7,
         label=r'$\mathcal{A}_{\rm peak} = \max_t S$ (first maximum)')
ax1.plot(Ns, A_conv, 's-', color='tab:blue', ms=6,
         label=r'$\mathcal{A} = S(N/\Omega_{\rm gr})$ (fixed convention)')
Nfit = np.linspace(11, 14.5, 10)
ax1.plot(Nfit, 2.31 + 0.286 * Nfit, '-', color='gray', lw=2,
         label=r'linear fit $2.31+0.286\,N$ ($N\geq11$)')
Nex = np.linspace(1, 11, 10)
ax1.plot(Nex, 2.31 + 0.286 * Nex, '--', color='gray', lw=1.2, alpha=0.7,
         label='fit extrapolated below its domain')
ax1.axhline(3.0, color='k', ls='--', lw=1.2, label=r'detection threshold ($\mathcal{A}=3$)')
ax1.axhline(1.0, color='k', ls=':', lw=0.9, alpha=0.6)
ax1.annotate(r'$\mathcal{A}(1)=1$: no avalanche', xy=(1, 1.0), xytext=(1.6, 1.7),
             fontsize=10, arrowprops=dict(arrowstyle='->', lw=1.1))
ax1.set_xlabel(r'Array size $N$')
ax1.set_ylabel(r'Amplification factor $\mathcal{A} = S(T_a)/S(0)$')
ax1.set_title('(a) Amplification at small $N$: two readout conventions')
ax1.set_xticks(range(1, 15, 2))
ax1.legend(loc='upper left')
ax1.grid(alpha=0.3)

ax2.plot(Ns, Ta_conv_us, 's-', color='gray', ms=6,
         label=r'convention $T_a = N/\Omega_{\rm gr}$')
ax2.plot(Ns, Ta_meas_us, 'o-', color='tab:blue', ms=7,
         label=r'measured $T_a = \arg\max_t S$  ($\Omega_{\rm gr}T_a \approx 0.34\,N$)')
ax2.set_xlabel(r'Array size $N$')
ax2.set_ylabel(r'$T_a$ [$\mu$s]')
ax2.set_title('(b) Readout time: convention vs first maximum')
ax2.set_xticks(range(1, 15, 2))
ax2.legend(loc='upper left')
ax2.grid(alpha=0.3)

fig.tight_layout()
fig.savefig("amplification_smallN_readout.png")
plt.close(fig)

# ============================================================
# Figure 2: dephasing
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.9, 5.4))
cols = ['tab:blue', 'tab:green', 'tab:orange', 'tab:red']
for g, c in zip(gammas, cols):
    r = runsA[g]
    ax1.plot(r["tnorm"], r["S"], color=c, lw=2,
             label=fr'$\Gamma_\phi/\Omega_{{\rm gr}} = {g}$')
    ip = int(np.argmax(r["S"]))
    ax1.plot(r["tnorm"][ip], r["S"][ip], 'o', color=c, ms=6)
ax1.set_xlabel(r'Normalised time $\Omega_{\rm gr} t$')
ax1.set_ylabel(r'Total signal $S(t)$')
ax1.set_title(fr'(a) Signal evolution under pure dephasing ($N={N0}$)')
ax1.legend()
ax1.grid(alpha=0.3)

ax2.plot(Ns_d, A_pk_uni, 'o-', color='tab:blue', ms=7,
         label=r'$\mathcal{A}_{\rm peak}$, coherent ($\Gamma_\phi=0$)')
ax2.plot(Ns_d, A_pk_d, 's-', color='tab:green', ms=6,
         label=r'$\mathcal{A}_{\rm peak}$ at $\Gamma_\phi=0.1\,\Omega_{\rm gr}$')
ax2.plot(Ns_d, A_pl_d, '^--', color='tab:orange', ms=6,
         label=r'$\mathcal{A}_{\rm plateau}$ (late-time) at $\Gamma_\phi=0.1\,\Omega_{\rm gr}$')
ax2.axhline(3.0, color='k', ls='--', lw=1.2, label=r'detection threshold ($\mathcal{A}=3$)')
ax2.set_xlabel(r'Array size $N$')
ax2.set_ylabel(r'Amplification factor $\mathcal{A}$')
ax2.set_title(r'(b) Peak and plateau amplification under dephasing')
ax2.set_xticks(Ns_d)
ax2.legend(loc='upper left')
ax2.grid(alpha=0.3)

fig.tight_layout()
fig.savefig("avalanche_dephasing.png")
plt.close(fig)

print("saved amplification_smallN_readout.png, avalanche_dephasing.png, dephasing_scan_data.npz")
print(f"check: N=11 conv={res[11]['A_analytic']:.2f} peak={res[11]['A_peak']:.2f}; "
      f"N=7 peaks uni/deph {A_pk_uni[-1]:.2f}/{A_pk_d[-1]:.2f} plateau {A_pl_d[-1]:.2f}")
