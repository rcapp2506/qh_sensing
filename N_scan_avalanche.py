"""
Avalanche gain vs number of atoms N — scan N = 1..14.

Reuses the exact Hamiltonian and parameters of the thesis simulations
(scenario 'a', B = 0, facilitation Delta_gr = -V_rr), single local
excitation at the chain centre, and compares:
  - T_a analytic  = N / Omega_gr          (what the code/slide assume)
  - T_a data      = argmax_t S(t)          (measured from the curve)
  - A_analytic    = S(t = N/Omega_gr)      (what the thesis reports)
  - A_peak        = max_t S(t)             (true maximum gain)
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import expm_multiply
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- physical parameters (scenario a, B = 0) --------------------------------
Omega_gr = 2 * np.pi * 0.2e6      # rad/s
V_rr     = 2 * np.pi * 12.5e6     # rad/s
Delta_gr = -V_rr                  # facilitation condition

# single-atom operators (|g>=0, |r>=1)
sx = sp.csr_matrix(np.array([[0, 1], [1, 0]], dtype=complex))   # sigma+ + sigma-
nr = sp.csr_matrix(np.array([[0, 0], [0, 1]], dtype=complex))   # |r><r|
I2 = sp.identity(2, format="csr", dtype=complex)


def op_at(op, j, N):
    """Embed single-site operator on site j (site 0 = most significant, np.kron order)."""
    mats = [I2] * N
    mats[j] = op
    out = mats[0]
    for m in mats[1:]:
        out = sp.kron(out, m, format="csr")
    return out


def build_H(N):
    H = sp.csr_matrix((2**N, 2**N), dtype=complex)
    for j in range(N):
        H = H + Omega_gr * op_at(sx, j, N)
        H = H + Delta_gr * op_at(nr, j, N)
    for j in range(N - 1):
        H = H + V_rr * (op_at(nr, j, N) @ op_at(nr, j + 1, N))
    return H.tocsr()


def site_excited_diag(N):
    """d[j] = diagonal (length 2^N): 1 where site j is |r>. Consistent with kron order."""
    diags = []
    for j in range(N):
        vecs = [np.array([1.0, 1.0])] * N
        vecs[j] = np.array([0.0, 1.0])
        d = vecs[0]
        for v in vecs[1:]:
            d = np.kron(d, v)
        diags.append(d)
    return np.array(diags)               # shape (N, 2^N)


def run_N(N, n_time=320, t_factor=2.5):
    H = build_H(N)
    dim = 2**N
    # initial state: centre atom excited
    c = N // 2
    idx = 0
    for j in range(N):
        bit = 1 if j == c else 0
        idx = (idx << 1) | bit           # site 0 = MSB, matches kron order
    psi0 = np.zeros(dim, dtype=complex)
    psi0[idx] = 1.0

    T_a_analytic = N / Omega_gr
    t_max = t_factor * T_a_analytic
    times = np.linspace(0.0, t_max, n_time)

    # propagate |psi(t)> = exp(-i H t) psi0 over the grid
    psis = expm_multiply(-1j * H, psi0, start=0.0, stop=t_max, num=n_time, endpoint=True)
    prob = np.abs(psis) ** 2             # (n_time, dim)

    dj = site_excited_diag(N)            # (N, dim)
    Sj = prob @ dj.T                     # (n_time, N)  spatially resolved
    S = Sj.sum(axis=1)                   # (n_time,)  total signal

    idx_analytic = np.argmin(np.abs(times - T_a_analytic))
    idx_peak = int(np.argmax(S))
    return {
        "N": N, "times": times, "S": S, "Sj": Sj,
        "T_a_analytic": T_a_analytic, "T_a_data": times[idx_peak],
        "A_analytic": S[idx_analytic], "A_peak": S[idx_peak],
        "S0": S[0], "tnorm": times * Omega_gr,
    }


Ns = list(range(1, 15))
results = {}
for N in Ns:
    r = run_N(N)
    results[N] = r
    print(f"N={N:2d}  S0={r['S0']:.3f}  "
          f"A_analytic(S@N/Om)={r['A_analytic']:.3f}  A_peak={r['A_peak']:.3f}  "
          f"Ta_analytic={r['T_a_analytic']*1e6:.2f}us  Ta_data={r['T_a_data']*1e6:.2f}us "
          f"(Om*Ta_data={r['T_a_data']*Omega_gr:.2f})")

# save numeric summary
import csv
with open("N_scan_summary.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["N", "S0", "A_analytic_S_at_N_over_Omega", "A_peak_max",
                "Ta_analytic_us", "Ta_data_us", "Omega_Ta_data"])
    for N in Ns:
        r = results[N]
        w.writerow([N, f"{r['S0']:.4f}", f"{r['A_analytic']:.4f}", f"{r['A_peak']:.4f}",
                    f"{r['T_a_analytic']*1e6:.3f}", f"{r['T_a_data']*1e6:.3f}",
                    f"{r['T_a_data']*Omega_gr:.3f}"])

# =========================== PLOTS ===========================================
plt.rcParams.update({"font.size": 11, "axes.grid": True, "grid.alpha": 0.3})

# ---- Fig 1: S(t) for all N ----
fig, ax = plt.subplots(figsize=(9, 6))
cmap = plt.cm.viridis(np.linspace(0, 0.92, len(Ns)))
for col, N in zip(cmap, Ns):
    r = results[N]
    ax.plot(r["tnorm"], r["S"], color=col, lw=1.8, label=f"N={N}")
    ax.plot(r["T_a_data"] * Omega_gr, r["A_peak"], "o", color=col, ms=5)
ax.set_xlabel(r"Normalized time  $\Omega_{gr}\,t$")
ax.set_ylabel(r"Total signal  $S(t)=\sum_j\langle n_r^{(j)}\rangle$")
ax.set_title("Avalanche signal vs time for N = 1…14 (local excitation, B=0)\n"
             "dots = measured peak")
ax.legend(ncol=2, fontsize=8, loc="upper left")
fig.tight_layout(); fig.savefig("fig_S_vs_t_allN.png", dpi=160)

# ---- Fig 2: A(N) — two definitions vs the A~N law ----
fig, ax = plt.subplots(figsize=(8, 6))
A_an = [results[N]["A_analytic"] for N in Ns]
A_pk = [results[N]["A_peak"] for N in Ns]
ax.plot(Ns, A_pk, "o-", color="darkgreen", lw=2, ms=7, label=r"$\mathcal{A}_{\rm peak}=\max_t S$ (true max gain)")
ax.plot(Ns, A_an, "s--", color="darkorange", lw=2, ms=6, label=r"$\mathcal{A}=S(t{=}N/\Omega_{gr})$ (thesis def.)")
ax.plot(Ns, Ns, ":", color="gray", lw=1.5, label=r"ideal $\mathcal{A}=N$")
ax.axhline(3.0, color="red", ls="--", alpha=0.6, label="detection threshold = 3")
ax.axhline(1.0, color="black", ls=":", alpha=0.5, label=r"$\mathcal{A}=1$ (no gain)")
ax.set_xlabel("Number of atoms N")
ax.set_ylabel(r"Amplification factor $\mathcal{A}=S/S(0)$")
ax.set_title("Avalanche gain vs N — where the A~N law breaks at small N")
ax.set_xticks(Ns); ax.legend(fontsize=9)
fig.tight_layout(); fig.savefig("fig_A_vs_N.png", dpi=160)

# ---- Fig 3: T_a analytic vs measured ----
fig, ax = plt.subplots(figsize=(8, 6))
Ta_an = [results[N]["T_a_analytic"] * 1e6 for N in Ns]
Ta_da = [results[N]["T_a_data"] * 1e6 for N in Ns]
ax.plot(Ns, Ta_an, "s--", color="darkorange", lw=2, ms=6, label=r"$T_a=N/\Omega_{gr}$ (assumed)")
ax.plot(Ns, Ta_da, "o-", color="navy", lw=2, ms=7, label=r"$T_a=\arg\max_t S$ (measured)")
ax.set_xlabel("Number of atoms N")
ax.set_ylabel(r"$T_a$  ($\mu$s)")
ax.set_title("Optimal amplification time: assumed vs measured")
ax.set_xticks(Ns); ax.legend(fontsize=10)
fig.tight_layout(); fig.savefig("fig_Ta_vs_N.png", dpi=160)

print("\nSaved: fig_S_vs_t_allN.png, fig_A_vs_N.png, fig_Ta_vs_N.png, N_scan_summary.csv")
