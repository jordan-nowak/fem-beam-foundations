"""
Visualize analytical solution of a cantilever beam under tip load.

- Shows deformed shape of the beam
- Coloration along the beam based on bending moment
- Flèche de charge à l'extrémité
- Traditional plots of deflection, rotation, and bending moment

Author: Jordan NOWAK
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from theory_beam.euler_bernoulli import deflection, rotation, bending_moment

# --- Beam parameters ---
F = 1000.0           # Tip load [N]
L = 2.0              # Beam length [m]
E = 210e9            # Young's modulus [Pa]
I = 1e-6             # Second moment of area [m^4]

# --- Discretize the beam ---
x = np.linspace(0, L, 200)

# --- Compute analytical solution ---
w = deflection(x, F, L, E, I)
theta = rotation(x, F, L, E, I)
M = bending_moment(x, F, L)

# --- Normalize moment for coloring ---
M_norm = (M - M.min()) / (M.max() - M.min())

# --- Create three subplots ---
fig, axs = plt.subplots(3, 1, figsize=(7, 9), sharex=True)
fig.suptitle("Cantilever beam: analytical solution visualization", fontsize=16)

# --- Deformed beam plot with color map based on bending moment ---
for i in range(len(x) - 1):
    axs[0].plot(x[i:i+2], w[i:i+2], color=cm.viridis(M_norm[i]), lw=3)

axs[0].plot(x, np.zeros_like(x), 'k--', lw=1, label="Neutral axis")         # Draw neutral axis
axs[0].arrow(L, w[-1]+0.05, 0, -0.1, head_width=0.05*L, head_length=0.05,   # Force applied
             fc='red', ec='red', label="Load F")
axs[0].set_ylabel("Deformation [m]")
axs[0].grid(True)
axs[0].legend()
axs[0].set_title("Deformed beam colored by bending moment")

# --- Rotation plot ---
axs[1].plot(x, theta, 'g', lw=2, label="Rotation theta(x)")
axs[1].axhline(0, linestyle='--', color='k', alpha=0.5)
axs[1].set_ylabel("Rotation theta(x) [rad]")
axs[1].grid(True)
axs[1].legend()

# --- Bending moment plot ---
axs[2].plot(x, M, 'r', lw=2, label="Bending moment M(x)")
axs[2].axhline(0, linestyle='--', color='k', alpha=0.5)
axs[2].set_xlabel("Position along beam [m]")
axs[2].set_ylabel("Bending moment M(x) [Nm]")
axs[2].grid(True)
axs[2].legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()