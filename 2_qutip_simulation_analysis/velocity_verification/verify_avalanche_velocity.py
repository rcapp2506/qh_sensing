"""
Verification of the avalanche propagation velocity quoted in
Sec. 4.5 (Cap. 4) of the thesis.

This script reproduces the v ~ 5.5 um/us value cited next to the
V-shaped panel of the avalanche dynamics figure, using the
zero-magnetic-field QuTiP simulation in this same package
(rydberg_avalanche_qutip.py). The same value is reproduced
independently by the with-B simulation in
3_qutip_simpulation_with_magnetic_field at B = 0.

Three independent extraction methods are computed:

  - "centroid"     : v from the slope of the right-side centre-of-mass
                     <Delta j>(t) of the excitation distribution.
                     This is the physically cleanest definition for a
                     dispersive coherent front, and is the value
                     reported in the manuscript.

  - "peak_fit"     : v from a linear fit of (distance vs first-peak
                     time) on the right-side sites j > center. Less
                     robust to internal Rabi oscillations.

  - "leading_edge" : v from the slope of the most-extreme site reached
                     above a chosen probability threshold. Captures
                     the leading edge of the quantum front; gives a
                     systematically higher value (consistent with the
                     usual leading-edge/group-velocity distinction in
                     dispersive systems).

The script also produces a heatmap of S_j(t) overlaid with three
velocity hypotheses, providing direct visual confirmation that the
v = 5.5 um/us line traces the boundary of the high-intensity V-region
on which the manuscript claim is based.

Usage:
    cd 2_qutip_simulation_analysis/velocity_verification
    python verify_avalanche_velocity.py

Outputs in current directory:
    avalanche_velocity_overlay.png  -- heatmap with the three v overlays
    avalanche_centroid_trace.png    -- centroid trajectory vs time
"""

from __future__ import annotations

import os
import sys
import contextlib
import io
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Import the simulation module from the sibling code directory
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
CODE_DIR = HERE.parent  # 2_qutip_simulation_analysis/
sys.path.insert(0, str(CODE_DIR))

from rydberg_avalanche_qutip import (   # noqa: E402
    RydbergDetectorParams,
    build_hamiltonian_amplification,
    initial_state_local_excitation,
    compute_signal_evolution,
)


# ---------------------------------------------------------------------------
# Velocity extraction methods
# ---------------------------------------------------------------------------

def v_centroid(times, S_spatial, N, a_um, t_fit_window=(0.1, 3.0)):
    """v from the slope of the right-side centre-of-mass <Delta j>(t)."""
    center = N // 2
    times_us = times * 1e6
    centroids_um = np.zeros_like(times_us)
    for idx in range(len(times)):
        weights = S_spatial[center:, idx]
        positions = np.arange(N - center)
        centroids_um[idx] = (
            np.sum(weights * positions) / max(weights.sum(), 1e-9)
        ) * a_um
    mask = (times_us > t_fit_window[0]) & (times_us < t_fit_window[1])
    slope, intercept = np.polyfit(times_us[mask], centroids_um[mask], 1)
    return slope, centroids_um, times_us


def v_peak_fit(times, S_spatial, N, a_um):
    """v from linear fit of distance vs first-peak time on right-side sites."""
    t_half = len(times) // 2
    center = N // 2
    peak_times_us = []
    distances_um = []
    for j in range(center + 1, N):
        idx_peak = int(np.argmax(S_spatial[j, :t_half]))
        if idx_peak > 0:
            peak_times_us.append(times[idx_peak] * 1e6)
            distances_um.append((j - center) * a_um)
    if len(peak_times_us) < 3:
        return float("nan")
    slope, _ = np.polyfit(peak_times_us, distances_um, 1)
    return slope


def v_leading_edge(times, S_spatial, N, a_um, threshold=0.3,
                   t_fit_window=(0.2, 3.0)):
    """v from the slope of the most-extreme right-side site reaching `threshold`."""
    center = N // 2
    times_us = times * 1e6
    extreme_um = np.zeros_like(times_us)
    for idx in range(len(times)):
        right = np.where(S_spatial[center + 1:, idx] > threshold)[0]
        if len(right):
            extreme_um[idx] = (right[-1] + 1) * a_um
    mask = (times_us > t_fit_window[0]) & (extreme_um > 0) & (times_us < t_fit_window[1])
    if mask.sum() < 3:
        return float("nan")
    slope, _ = np.polyfit(times_us[mask], extreme_um[mask], 1)
    return slope


# ---------------------------------------------------------------------------
# Main verification routine
# ---------------------------------------------------------------------------

def run_verification(N=11, t_max_short=4e-6, t_max_long_norm=25.0,
                     n_times=200, save_dir="."):
    """
    Run the verification: two simulations (short range for fits, long
    range for overlay plot), measure v with three methods, and produce
    the two diagnostic figures.
    """
    params = RydbergDetectorParams(scenario='a')
    params.N = N
    a_um = params.a0 * 1e6
    omega_gr = params.Omega_gr  # rad/s

    print("=" * 70)
    print("Avalanche velocity verification (B = 0)")
    print("=" * 70)
    print(f"  N             = {N} atoms")
    print(f"  a_lattice     = {a_um} um")
    print(f"  Omega_gr/(2pi)= {omega_gr/(2*np.pi)/1e6:.3f} MHz")
    print()

    psi0 = initial_state_local_excitation(N, k=N // 2)
    H = build_hamiltonian_amplification(N, params)

    # Run 1: short time range, dense, for v fitting -------------------------
    times_short = np.linspace(0, t_max_short, n_times)
    print(f"Run 1: t in [0, {t_max_short*1e6:.1f}] us, {n_times} points")
    with contextlib.redirect_stdout(io.StringIO()):
        _, S_spatial_short, _ = compute_signal_evolution(
            psi0, H, times_short, N, show_progress=False,
        )
    print("  done.\n")

    # Method 1: centroid
    v_c, centroids_um, t_us = v_centroid(times_short, S_spatial_short, N, a_um)

    # Method 2: peak fit
    v_p = v_peak_fit(times_short, S_spatial_short, N, a_um)

    # Method 3: leading edge
    v_l = v_leading_edge(times_short, S_spatial_short, N, a_um, threshold=0.3)

    print("Velocity extraction (three independent methods):")
    print(f"  v_centroid     = {v_c:.2f} um/us   (reported value, manuscript)")
    print(f"  v_peak_fit     = {v_p:.2f} um/us   (less robust)")
    print(f"  v_leading_edge = {v_l:.2f} um/us   (front extremity)")
    print()
    print("Sanity-check estimates:")
    nu_gr = omega_gr / (2 * np.pi)
    v_naive = (nu_gr * params.a0) * 1.0  # m/s = um/us numerically
    print(f"  v_naive = nu_gr * a = {v_naive:.2f} um/us   (no factor 2pi)")
    print(f"  v_hop   = 2*nu_gr*a = {2*v_naive:.2f} um/us   (T_Rabi/2 hopping)")
    print()

    # Run 2: long time range for overlay plot -------------------------------
    t_max_long = t_max_long_norm / omega_gr
    times_long = np.linspace(0, t_max_long, n_times)
    print(f"Run 2: Omega_gr*t in [0, {t_max_long_norm:.0f}], {n_times} points")
    with contextlib.redirect_stdout(io.StringIO()):
        _, S_spatial_long, _ = compute_signal_evolution(
            psi0, H, times_long, N, show_progress=False,
        )
    print("  done.\n")

    # Overlay plot ----------------------------------------------------------
    _make_overlay_plot(
        times_long, S_spatial_long, N, a_um, omega_gr,
        v_values=[(v_naive, "cyan", f"v_naive = nu*a = {v_naive:.1f} um/us"),
                  (v_c, "lime", f"v_centroid = {v_c:.1f} um/us"),
                  (v_l, "magenta", f"v_leading = {v_l:.1f} um/us")],
        save_path=os.path.join(save_dir, "avalanche_velocity_overlay.png"),
    )
    print(f"  overlay -> {save_dir}/avalanche_velocity_overlay.png")

    # Centroid trace plot ---------------------------------------------------
    _make_centroid_plot(
        t_us, centroids_um, v_c,
        save_path=os.path.join(save_dir, "avalanche_centroid_trace.png"),
    )
    print(f"  trace   -> {save_dir}/avalanche_centroid_trace.png")
    print()

    return {
        "v_centroid": v_c,
        "v_peak_fit": v_p,
        "v_leading_edge": v_l,
        "v_naive": v_naive,
    }


def _make_overlay_plot(times, S_spatial, N, a_um, omega_gr, v_values, save_path):
    fig, ax = plt.subplots(figsize=(11, 5))
    times_norm = times * omega_gr
    im = ax.pcolormesh(
        times_norm, np.arange(N), S_spatial,
        cmap="hot", vmin=0, vmax=1, shading="auto",
    )
    center = N // 2
    omega_rad_per_us = omega_gr / 1e6
    taus_overlay = np.linspace(0, times_norm[-1], 50)
    for v_um_per_us, color, label in v_values:
        slope = (v_um_per_us / a_um) / omega_rad_per_us
        js_right = center + slope * taus_overlay
        js_left = center - slope * taus_overlay
        ax.plot(taus_overlay, js_right, color=color, linewidth=1.5, label=label)
        ax.plot(taus_overlay, js_left, color=color, linewidth=1.5)
    ax.set_xlabel(r"Time $\Omega_{\mathrm{gr}} t$", fontsize=13)
    ax.set_ylabel("Site $j$", fontsize=13)
    ax.set_xlim(0, times_norm[-1])
    ax.set_ylim(-0.5, N - 0.5)
    ax.legend(loc="upper right", framealpha=0.9, fontsize=9)
    ax.set_title("Avalanche dynamics with velocity overlays (B = 0)", fontsize=13)
    plt.colorbar(im, ax=ax, label=r"$S_j$")
    plt.tight_layout()
    plt.savefig(save_path, dpi=120)
    plt.close(fig)


def _make_centroid_plot(t_us, centroids_um, v_c, save_path):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t_us, centroids_um, "o", markersize=4, label="centroid data")
    fit_mask = (t_us > 0.1) & (t_us < 3.0)
    fit_line = v_c * t_us[fit_mask]
    ax.plot(t_us[fit_mask], fit_line, "-",
            label=f"linear fit, v = {v_c:.2f} um/us")
    ax.set_xlabel("Time (us)")
    ax.set_ylabel(r"$\langle \Delta j \rangle \cdot a$ (um)")
    ax.set_title("Right-side centroid trajectory (B = 0, N = 11)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    results = run_verification(save_dir=str(HERE))
    print("Summary:")
    for k, v in results.items():
        print(f"  {k:15s} = {v:7.3f} um/us")
