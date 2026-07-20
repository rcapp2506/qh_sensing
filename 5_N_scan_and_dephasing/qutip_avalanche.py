"""Avalanche N-scan on the canonical QuTiP engine (sesolve / mesolve).

Model (identical to qh_sensing): 1D chain, |g>,|r> per atom,
H = Omega_gr sum_j sx_j + Delta_gr sum_j n_r_j + V_rr sum_j n_r_j n_r_{j+1},
facilitation Delta_gr = -V_rr, single local (centre) seed, B=0.
Pure dephasing collapse ops c_j = sqrt(gamma_phi) sz_j.
"""
import sys, time
import numpy as np
import qutip as qt

Omega_gr = 2 * np.pi * 0.2e6
V_rr     = 2 * np.pi * 12.5e6
Delta_gr = -V_rr

g = qt.basis(2, 0)          # |g>
e = qt.basis(2, 1)          # |r>
sx = qt.sigmax()
sz = qt.sigmaz()
nr = e * e.dag()            # |r><r|


def site_op(op, j, N):
    ops = [qt.qeye(2)] * N
    ops[j] = op
    return qt.tensor(ops)


def build_H(N):
    H = 0
    for j in range(N):
        H += Omega_gr * site_op(sx, j, N) + Delta_gr * site_op(nr, j, N)
    for j in range(N - 1):
        H += V_rr * site_op(nr, j, N) * site_op(nr, j + 1, N)
    return H


def psi0_local(N):
    kets = [g] * N
    kets[N // 2] = e
    return qt.tensor(kets)


def nr_ops(N):
    return [site_op(nr, j, N) for j in range(N)]


def run(N, gamma_phi=0.0, n_time=300, t_factor=2.5):
    H = build_H(N)
    psi0 = psi0_local(N)
    T_a_analytic = N / Omega_gr
    tlist = np.linspace(0.0, t_factor * T_a_analytic, n_time)
    e_ops = nr_ops(N)
    opts = qt.Options(nsteps=200000, atol=1e-8, rtol=1e-6) if hasattr(qt, "Options") \
        else {"nsteps": 200000, "atol": 1e-8, "rtol": 1e-6}
    if gamma_phi == 0.0:
        res = qt.sesolve(H, psi0, tlist, e_ops=e_ops, options=opts)
    else:
        c_ops = [np.sqrt(gamma_phi) * site_op(sz, j, N) for j in range(N)]
        res = qt.mesolve(H, psi0, tlist, c_ops=c_ops, e_ops=e_ops, options=opts)
    Sj = np.array(res.expect)                     # (N, n_time)
    S = Sj.sum(axis=0)
    ia = int(np.argmin(np.abs(tlist - T_a_analytic)))
    ip = int(np.argmax(S))
    return {"N": N, "gamma": gamma_phi, "tlist": tlist, "tnorm": tlist * Omega_gr,
            "S": S, "Sj": Sj, "T_a_analytic": T_a_analytic,
            "T_a_data": tlist[ip], "A_analytic": S[ia], "A_peak": S[ip],
            "A_plateau": S[-30:].mean()}


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "unitary"
    if mode == "unitary":
        import csv
        Ns = list(range(1, 15))
        results = {}
        for N in Ns:
            t0 = time.time()
            r = run(N, 0.0)
            results[N] = r
            print(f"N={N:2d} A_analytic={r['A_analytic']:.3f} A_peak={r['A_peak']:.3f} "
                  f"Ta_data(Om*t)={r['T_a_data']*Omega_gr:.2f} [{time.time()-t0:.1f}s]", flush=True)
        np.save("qutip_unitary_results.npy", results, allow_pickle=True)
        with open("qutip_unitary_summary.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["N", "A_analytic_S_at_N_over_Om", "A_peak", "Om_Ta_data", "Ta_data_us"])
            for N in Ns:
                r = results[N]
                w.writerow([N, f"{r['A_analytic']:.4f}", f"{r['A_peak']:.4f}",
                            f"{r['T_a_data']*Omega_gr:.4f}", f"{r['T_a_data']*1e6:.4f}"])
        print("saved qutip_unitary_results.npy, qutip_unitary_summary.csv")
