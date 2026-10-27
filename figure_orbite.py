# -*- coding: utf-8 -*-
"""
Génère la figure du README : orbite de Mercure et mouvement du Soleil
autour du barycentre, avec les mêmes paramètres que tipe.py.

Usage : python figure_orbite.py
Sortie : images/orbite-light.png et images/orbite-dark.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt

G = 6.67430e-11
DT = 86400            # pas de temps : 1 jour (comme dans tipe.py)
N_JOURS = 2 * 88      # deux révolutions de Mercure
UA = 1.495978707e11

# Mêmes corps que dans tipe.py : Soleil + Mercure
m = np.array([1.989e30, 3.301e23])
pos = np.array([[0.0, 0.0], [5.79e10, 0.0]])
vit = np.array([[0.0, 0.0], [0.0, 47360.0]])

# On donne au Soleil la vitesse qui annule la quantité de mouvement totale,
# pour que le barycentre reste immobile au lieu de dériver.
vit[0] = -(m[1] * vit[1]) / m[0]


def acceleration(pos):
    acc = np.zeros_like(pos)
    for i in range(len(m)):
        for j in range(len(m)):
            if i != j:
                d = pos[j] - pos[i]
                r = np.linalg.norm(d)
                acc[i] += G * m[j] * d / r**3
    return acc


traj = [pos.copy()]
for _ in range(N_JOURS):
    vit += acceleration(pos) * DT   # Euler semi-implicite, comme tipe.py
    pos += vit * DT
    traj.append(pos.copy())
traj = np.array(traj)              # forme (temps, corps, 2)

bary = (m[:, None] * traj).sum(axis=1) / m.sum()
soleil = (traj[:, 0] - bary) / 1e3            # en km
mercure = (traj[:, 1] - bary) / UA            # en UA

THEMES = {
    "light": dict(fg="#24292f", grid="#d0d7de", accent="#871DF7", sun="#e3a008"),
    "dark": dict(fg="#c9d1d9", grid="#30363d", accent="#a855f7", sun="#f5c542"),
}

os.makedirs("images", exist_ok=True)
for nom, t in THEMES.items():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.6))
    fig.patch.set_alpha(0)
    for ax in (ax1, ax2):
        ax.set_facecolor("none")
        ax.set_aspect("equal")
        ax.grid(color=t["grid"], lw=0.6)
        ax.tick_params(colors=t["fg"], labelsize=9)
        for s in ax.spines.values():
            s.set_color(t["grid"])

    ax1.plot(mercure[:, 0], mercure[:, 1], color=t["accent"], lw=1.6)
    ax1.plot(0, 0, "o", color=t["sun"], ms=12)
    ax1.plot(*mercure[-1], "o", color=t["fg"], ms=4)
    ax1.set_title("Orbite de Mercure", color=t["fg"], fontsize=11)
    ax1.set_xlabel("x (UA)", color=t["fg"], fontsize=9)
    ax1.set_ylabel("y (UA)", color=t["fg"], fontsize=9)

    ax2.plot(soleil[:, 0], soleil[:, 1], color=t["sun"], lw=1.6)
    ax2.plot(0, 0, "+", color=t["fg"], ms=10, mew=1.4)
    ax2.set_title("Le Soleil autour du barycentre", color=t["fg"], fontsize=11)
    ax2.set_xlabel("x (km)", color=t["fg"], fontsize=9)
    ax2.set_ylabel("y (km)", color=t["fg"], fontsize=9)

    fig.tight_layout()
    fig.savefig(f"images/orbite-{nom}.png", dpi=160, transparent=True)
    plt.close(fig)

print("Rayon du mouvement du Soleil : %.1f km" % np.abs(soleil).max())
