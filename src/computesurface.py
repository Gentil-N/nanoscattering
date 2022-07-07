import plot
import inout
import numpy as np
import math
import mietheory
from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

REF_INDICES_RAW = inout.load_ref_index("./res/refractive-index-silicon-visible")
WAVELENGTHS = np.linspace(REF_INDICES_RAW[0][0], REF_INDICES_RAW[-1][0], 200)
PARTSIZES = np.linspace(50e-9, 99e-9, 100)

data = inout.load_triangle_by_color("./res/disktest-high.ply")
scattering_cross_section = mietheory.ccs_integ_triangle_surface(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, data[0], data[1], 3 + 1)
inout.export_surface(WAVELENGTHS, PARTSIZES, scattering_cross_section, "./output/surface-test")

fig = plt.figure(num=0)
ax = fig.subplots(nrows=1, ncols=1)
ax.contourf(WAVELENGTHS, PARTSIZES, scattering_cross_section, cmap='inferno', levels=70)
ax.set(xlabel="wavelength", ylabel="particle radius")
fig.colorbar(mappable=ScalarMappable(norm=Normalize(vmin=0, vmax=10), cmap='inferno'), ax=ax)
inout.show_plot("./output/surface-test.png")