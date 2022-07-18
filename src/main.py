import plot
import inout
import numpy as np
import math

from matplotlib import pyplot as plt
import mietheory

REF_INDICES_RAW_COMSOL = inout.load_ref_index("./res/refractive-index-silicon-comsol-dorte")
REF_INDICES_RAW = inout.load_ref_index("./res/refractive-index-silicon")
WAVELENGTHS = np.linspace(REF_INDICES_RAW[0][0], REF_INDICES_RAW[-1][0], 200)
PARTSIZES = np.linspace(50e-9, 99e-9, 100)

NA = 0.3 * math.pi
NI = 0.1 * math.pi

plot.exact_sca_ext(REF_INDICES_RAW_COMSOL, WAVELENGTHS, 80e-9, 3 + 1, "./output/exact_sca_ext_comsol.png")
plot.exact_sca_ext(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1, "./output/exact_sca_ext.png")

res_COMSOL = mietheory.ccs_exact(REF_INDICES_RAW_COMSOL, WAVELENGTHS, 80e-9, 3 + 1)
res = mietheory.ccs_exact(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1)
fig0 = plt.figure(num=0)
ax0 = fig0.subplots(nrows=1, ncols=1)
ax0.set_title("Cross Sections Diff")
ax0.plot(WAVELENGTHS, res_COMSOL[0] - res[0], label="Sca Diff")
ax0.plot(WAVELENGTHS, res_COMSOL[1] - res[1], label="Ext Diff")
ax0.plot(WAVELENGTHS, (res_COMSOL[1] - res_COMSOL[0]) - (res[1] - res[0]), label="Abs Diff")
ax0.set(xlabel="wavelength (m)")
ax0.legend()
ax0.grid()
inout.show_plot("./output/exact_sca_ext_diff.png")

#plot.exact_sca_ext(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1, "./output/exact_sca_ext.png")
#plot.exact_sca_ext_surface(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, 3 + 1, "./output/exact_sca_ext_surface.png")
#plot.integ_sca(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 0, 2 * math.pi, 0, math.pi, 50, 3 + 1, "./output/integ_sca.png")
#plot.integ_sca_surface(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, 0, 2 * math.pi, 0, math.pi * 0.5, 50, 3 + 1, "./output/#integ_sca_surface.png")
#plot.integ_sca_by_colored_triangle(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1, "./res/whole-medium.ply", "./output/#integ_sca_by_triangle.png")
#plot.integ_sca_surface_by_colored_triangle(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, 3 + 1, "./res/whole-medium.ply", "./output/integ_sca_surface_by_triangle.png")
#plot.integ_sca_by_angle_triangle(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1, "./res/whole-medium.ply", NA, NI, "./output/#integ_sca_by_triangle.png")
#plot.integ_sca_surface_by_angle_triangle(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, 3 + 1, "./res/whole-medium.ply", NA, NI, "./#output/integ_sca_surface_by_triangle.png")