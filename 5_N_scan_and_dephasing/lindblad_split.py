"""Fast pure-dephasing avalanche evolution via Strang split-operator.

Unitary step U_dt = exp(-i H dt) computed exactly once (dense eigh).
Pure dephasing in the sigma_z product basis is element-wise damping of the
density-matrix coherences: rho_ab -> exp(-Gamma_ab dt) rho_ab, with
Gamma_ab = gamma * sum_j (1 - s_ja s_jb),  s = +/-1 sigma_z eigenvalues.
Strang: half-damp, full unitary, half-damp  => O(dt^2), unitary part exact.
"""
import numpy as np

Omega_gr = 2 * np.pi * 0.2e6
V_rr     = 2 * np.pi * 12.5e6
Delta_gr = -V_rr


def _basis_sz(N):
    # s[k, j] = +1 if site j is |g> (sz=+1) else -1 if |r>, site0 = MSB
    idx = np.arange(2**N)
    s = np.ones((2**N, N))
    for j in range(N):
        bit = (idx >> (N - 1 - j)) & 1        # 1 => |r>
        s[:, j] = 1.0 - 2.0 * bit             # |g>->+1, |r>->-1
    return s


def _build_H_dense(N):
    dim = 2**N
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    nr = np.array([[0, 0], [0, 1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)

    def op_at(op, j):
        out = np.array([[1]], dtype=complex)
        for k in range(N):
            out = np.kron(out, op if k == j else I2)
        return out

    H = np.zeros((dim, dim), dtype=complex)
    for j in range(N):
        H += Omega_gr * op_at(sx, j) + Delta_gr * op_at(nr, j)
    for j in range(N - 1):
        H += V_rr * (op_at(nr, j) @ op_at(nr, j + 1))
    return H


def _site_excited(N):
    # dj[j,k] = 1 if site j excited in basis state k
    s = _basis_sz(N)
    return (s < 0).astype(float).T           # (N, dim)


def run_lindblad(N, gamma_phi, n_out=160, t_factor=2.5, steps_per_Ta=600):
    dim = 2**N
    H = _build_H_dense(N)
    E, Vv = np.linalg.eigh(H)
    T_a_analytic = N / Omega_gr
    t_max = t_factor * T_a_analytic
    n_steps = int(steps_per_Ta * t_factor)
    dt = t_max / n_steps

    # exact unitary propagator for dt
    phase = np.exp(-1j * E * dt)
    U = (Vv * phase) @ Vv.conj().T           # dim x dim

    # dephasing damping matrix (half step)
    s = _basis_sz(N)
    Gamma = gamma_phi * (N - s @ s.T)         # (dim, dim), >=0, zero on diagonal
    Damp_half = np.exp(-0.5 * Gamma * dt)

    # initial rho: centre atom excited
    c = N // 2
    k0 = 0
    for j in range(N):
        k0 = (k0 << 1) | (1 if j == c else 0)
    rho = np.zeros((dim, dim), dtype=complex)
    rho[k0, k0] = 1.0

    dj = _site_excited(N)
    out_every = max(1, n_steps // n_out)
    times, Slist, Sjlist = [], [], []

    def record(t):
        pops = np.real(np.diag(rho))
        Sjlist.append(dj @ pops)
        Slist.append(float(pops @ dj.sum(axis=0)))
        times.append(t)

    record(0.0)
    for step in range(1, n_steps + 1):
        rho *= Damp_half
        rho = U @ rho @ U.conj().T
        rho *= Damp_half
        if step % out_every == 0:
            record(step * dt)

    times = np.array(times)
    return {"N": N, "gamma": gamma_phi, "gamma_norm": gamma_phi / Omega_gr,
            "times": times, "tnorm": times * Omega_gr,
            "S": np.array(Slist), "Sj": np.array(Sjlist),
            "T_a_analytic": T_a_analytic}


if __name__ == "__main__":
    import time
    for N in [8, 10]:
        t0 = time.time()
        r = run_lindblad(N, 0.1 * Omega_gr, t_factor=2.0)
        print(f"N={N} g/Om=0.1: peak={r['S'].max():.2f} late={r['S'][-25:].mean():.2f} "
              f"[{time.time()-t0:.1f}s]")
