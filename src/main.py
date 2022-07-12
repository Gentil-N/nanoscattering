import plot
import inout
import numpy as np
import math

from matplotlib import pyplot as plt
import mietheory

REF_INDICES_RAW = inout.load_ref_index("./res/refractive-index-silicon-visible")
WAVELENGTHS = np.linspace(REF_INDICES_RAW[0][0], REF_INDICES_RAW[-1][0], 200)
PARTSIZES = np.linspace(50e-9, 99e-9, 100)

NA = 0.3 * math.pi
NI = 0.1 * math.pi

#plot.exact_sca_ext(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1, "./output/exact_sca_ext.png")
#plot.exact_sca_ext_surface(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, 3 + 1, "./output/exact_sca_ext_surface.png")
#plot.integ_sca(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 0, 2 * math.pi, 0, math.pi, 50, 3 + 1, "./output/integ_sca.png")
#plot.integ_sca_surface(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, 0, 2 * math.pi, 0, math.pi * 0.5, 50, 3 + 1, "./output/#integ_sca_surface.png")
#plot.integ_sca_by_colored_triangle(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1, "./res/whole-medium.ply", "./output/#integ_sca_by_triangle.png")
plot.integ_sca_surface_by_colored_triangle(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, 3 + 1, "./res/whole-medium.ply", "./output/integ_sca_surface_by_triangle.png")
#plot.integ_sca_by_angle_triangle(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1, "./res/whole-medium.ply", NA, NI, "./output/#integ_sca_by_triangle.png")
#plot.integ_sca_surface_by_angle_triangle(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, 3 + 1, "./res/whole-medium.ply", NA, NI, "./#output/integ_sca_surface_by_triangle.png")

#ref_indices = np.linspace(3.5, 5, 1000)
#wavelength = 500e-9
#particle_size = 80e-9
#
#res = []
#for ref_index in ref_indices:
#    res.append(mietheory.ccs_exact([(wavelength, ref_index, 0.01)], [wavelength], particle_size, 3 + 1)[0])
#    print(ref_index)
#
#plt.plot(ref_indices, res)
#plt.show()