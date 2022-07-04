import plot
import inout
import numpy as np
import math

REF_INDICES_RAW = inout.load_ref_index("./res/refractive-index-silicon-2.csv")
WAVELENGTHS = np.linspace(REF_INDICES_RAW[0][0], REF_INDICES_RAW[-1][0], 100)
PARTSIZES = np.linspace(50e-9, 99e-9, 50)

#plot.exact_sca_ext(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1, "./output/exact_sca_ext.png")
#plot.exact_sca_ext_surface(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, 3 + 1, "./output/exact_sca_ext_surface.png")
#plot.integ_sca(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 0, 2 * math.pi, 0.5 * math.pi, math.pi, 50, 3 + 1, "./output/integ_sca.png")
plot.integ_sca_surface(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, 0, 2 * math.pi, 0, math.pi * 0.5, 50, 3 + 1, "./output/integ_sca_surface.png")
#plot.integ_sca_by_triangle(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1, "./res/sphere.ply", "./output/integ_sca_by_triangle.png")
#plot.integ_sca_surface_by_triangle(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, 3 + 1, "./res/whole-low.ply", "./output/integ_sca_surface_by_triangle.png")

#x = np.linspace(0, 9, 10)
#y1 = x**2
#y2 = x * 0.0
#print(stats.ks_2samp(y1, y2))