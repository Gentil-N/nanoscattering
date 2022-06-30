import plot
import inout
import numpy as np
import math
import time
import sys
import mietheory

REF_INDICES_RAW = inout.load_ref_index("./res/refractive-index-silicon-2.csv")
WAVELENGTHS = np.linspace(REF_INDICES_RAW[0][0], REF_INDICES_RAW[-1][0], 500)
PARTSIZES = np.linspace(95e-9, 99e-9, 5)

data_top = inout.load_selected_triangle("./res/top-medium.ply")
sca_top[index] = mietheory.ccs_integ_triangle_surface(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, data_top[0], data_top[1], 3 + 1)
data_bottom = inout.load_selected_triangle("./res/bottom-medium.ply")
sca_bottom[index] = mietheory.ccs_integ_triangle_surface(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, data_bottom[0], data_botto[1], 3 + 1)
res = sca_top / sca_bottom
fig0 = plt.figure(num=0)
ax0 = fig0.subplots(nrows=1, ncols=1)
ax0.set_title("Scattering Cross Section")
ax0.contourf(WAVELENGTHS, PARTSIZES, res, cmap='inferno', levels=70)
ax0.set(xlabel="wavelength", ylabel="particle radius")
fig0.colorbar(mappable=ScalarMappable(norm=Normalize(vmin=0, vmax=10), cmap='inferno'), ax=ax0)
inout.show_plot("./output/top_divided_by_bottom.png")