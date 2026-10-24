from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

csv_path = Path(__file__).resolve().parent / "cp_grid1.csv"  # look next to this script, not in the cwd
d = np.genfromtxt(csv_path, delimiter=",", skip_header=6, invalid_raise=False)
d = d[~np.isnan(d).any(axis=1)]       # drop any non-numeric lines
x, y, z, cp = d[:, 0], d[:, 1], d[:, 2], d[:, 3]

mask = np.isclose(z, z.min())         # keep one z-plane only
x, y, cp = x[mask], y[mask], cp[mask]
chord = 0.0676  # [m]
# Nearest-neighbour ordering, in case the polyline points aren't in order
order = [int(np.argmin(x))]          # start at the leading edge (min x)
left = set(range(len(x))) - set(order)
while left:
    i = order[-1]
    j = min(left, key=lambda k: (x[k]-x[i])**2 + (y[k]-y[i])**2)
    order.append(j); left.remove(j)
x, y, cp = x[order], y[order], cp[order]

# Cumulative arc length from the LE, normalised by the chord
s = np.concatenate(([0], np.cumsum(np.hypot(np.diff(x), np.diff(y))))) / chord

# The loop goes all the way round: split at the TE (max x)
iTE = np.argmax(x)
s_a, cp_a = s[:iTE+1], cp[:iTE+1]          # one side
s_b, cp_b = s[-1] - s[iTE:], cp[iTE:]      # other side, measured back from the LE

# Decide which side is the suction side (lower mean Cp) and give it positive s
if cp_a.mean() < cp_b.mean():
    ss, ps = (s_a, cp_a), (s_b, cp_b)
else:
    ss, ps = (s_b, cp_b), (s_a, cp_a)

plt.plot(*ss, label="Upper (Suction) Side")
plt.plot(*ps, label="Lower (Pressure) Side")
plt.gca().invert_yaxis()                   # -Cp upward
plt.xlabel("Coordinate along Blade Surface (s/c) [-]"); plt.ylabel("Pressure Coefficient (Cp) [-]"); plt.legend(); plt.grid()
plt.show()