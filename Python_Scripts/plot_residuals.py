import os
import matplotlib.pyplot as plt

folder = r"C:\Users\helen\Downloads\TU_DELFT\MSc_FPP\Q1\CFD\Assignment\cfd_repo\CFD_Group17\Grid1\RES_Grid1"
filename = os.path.join(folder, "grid1_first_try2_001.out")

equations = ["U-Mom", "V-Mom", "P-Mass", "H-Energy", "Eddy Viscosity"]
res = {eq: [] for eq in equations}
iterations = []

in_table = False  # only read the residual table of each iteration

with open(filename) as f:
    for line in f:
        if "OUTER LOOP ITERATION" in line:
            iterations.append(int(line.split("=")[1].split()[0]))
            in_table = True
        elif line.startswith(" ===="):
            in_table = False
        elif in_table and line.startswith(" |"):
            parts = [p.strip() for p in line.split("|")]
            name = parts[1]
            if name in res:
                res[name].append(float(parts[3]))  # RMS residual

for eq in equations:
    plt.semilogy(iterations[:len(res[eq])], res[eq], label=eq)

plt.xlabel("Iteration [-]")
plt.ylabel("RMS residual [-]")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(filename.replace(".out", "_residuals.png"), dpi=300)
plt.show()