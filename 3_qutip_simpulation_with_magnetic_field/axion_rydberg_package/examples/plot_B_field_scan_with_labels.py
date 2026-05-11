"""
Generate fig:B_field_scan (axion_detector_B_scan.png) with panel
labels (a), (b), (c), (d) drawn inside each subplot.

The script runs the standard QuTiP magnetic-field scan from
`axion_rydberg_detector_magnetic_field` (B = 0, 1, 3, 5 T, N = 11
atoms, T = 4 K), then calls the standard 4-panel plotting routine
`plot_magnetic_field_comparison` and overlays panel labels (a)-(d)
as boxed text in the upper-left corner of each subplot before
saving the figure with the manuscript-expected filename
`axion_detector_B_scan.png`.

The simulation itself is UNCHANGED with respect to the version that
generated the figure currently committed in
PhDThesis/chapters/qs_figures/.  Same Hamiltonian, same parameters,
same dimensional checks.  Only cosmetic overlays are added.


HOW TO RUN
----------
Place this script in the
    axion_rydberg_package/examples/
directory (next to the existing example_B_field_scan.py), then:

    cd .../axion_rydberg_package/examples/
    python3 plot_B_field_scan_with_labels.py

The figure is saved into the same directory.  Copy it into the
PhDThesis repository under
    chapters/qs_figures/axion_detector_B_scan.png
to overwrite the version referenced by the LaTeX caption.


REQUIREMENTS
------------
- qutip
- numpy
- matplotlib

Runtime: ~1-3 minutes on a typical workstation (4 QuTiP runs at
N = 11, Hilbert dimension 2048).
"""

import os
import sys

# Locate the code/ directory next to this examples/ directory
_here = os.path.dirname(os.path.abspath(__file__))
_code_dir = os.path.normpath(os.path.join(_here, '..', 'code'))
if _code_dir not in sys.path:
    sys.path.insert(0, _code_dir)

from axion_rydberg_detector_magnetic_field import (  # noqa: E402
    scan_magnetic_field, plot_magnetic_field_comparison
)


# ============================================================================
# Run the magnetic-field scan (full QuTiP simulation)
# ============================================================================
results = scan_magnetic_field(
    B_values=[0.0, 1.0, 3.0, 5.0],
    temperature=4.0,
    N=11,
)


# ============================================================================
# Plot — patch the standard 4-panel comparison with panel labels
# ============================================================================
fig = plot_magnetic_field_comparison(results, save_fig=False)

# Overlay panel labels (a)-(d) in the upper-left corner of each subplot.
# The first four axes of `fig.axes` are the four data panels; any
# subsequent axes belong to colorbars and are skipped.
panel_labels = ['(a)', '(b)', '(c)', '(d)']
for ax, lbl in zip(fig.axes[:4], panel_labels):
    ax.text(
        0.04, 0.94, lbl,
        transform=ax.transAxes,
        fontsize=18, fontweight='bold',
        va='top', ha='left',
        bbox=dict(
            boxstyle='round,pad=0.3',
            facecolor='white',
            edgecolor='black',
            alpha=0.85,
        ),
        zorder=10,
    )

# Save with the exact filename expected by the manuscript
out_path = os.path.join(_here, 'axion_detector_B_scan.png')
fig.savefig(out_path, dpi=300, bbox_inches='tight')
print(f"\nSaved: {out_path}")
