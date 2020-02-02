import subprocess
import re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

lattice_constants = []
cohesive_energies = []

infile = 'calc_fcc.in'
a0, a1, da = (3.0, 5.0, 0.1)

lammps_cmd = 'lmp_serial'


def run_simulation(infile, lattice_constant=4.0):
    print(f"Running LAMMPS ({infile})".center(80, "="))
    result = subprocess.run(
        [lammps_cmd, '-var', 'latconst', str(lattice_constant)], 
        stdin=open(infile), 
        stdout=subprocess.PIPE
    ).stdout.decode('utf-8')

    print(result)

    matches = re.findall('Cohesive energy \(eV\) = (.*);', result)
    try:
        cohesive_energy = float(matches[-1])
    except IndexError:
        print("No cohesive energy value found")
        cohesive_energy = np.NaN
    return cohesive_energy

for a in np.arange(a0, a1, da):
    ce = run_simulation(infile, a)
    lattice_constants.append(a)
    cohesive_energies.append(ce)

results_df = pd.DataFrame(
    dict(
        lattice_constant = lattice_constants,
        cohesive_energy = cohesive_energies,
    )
)
print(' RESULTS '.center(80, "="))
print(results_df)

plt.plot(results_df.lattice_constant, results_df.cohesive_energy, '-o')
plt.title("Cohesive Energy vs. Lattice Constant for fcc Aluminium")
plt.xlabel("Lattice constant (Å)")
plt.ylabel("Cohesive Energy (eV)")
plt.savefig("out.png")



