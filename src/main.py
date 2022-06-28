import plot
import inout
import numpy as np
import math
import time
import sys

REF_INDICES_RAW = inout.load_ref_index("./res/refractive-index-silicon-2.csv")
WAVELENGTHS = np.linspace(REF_INDICES_RAW[0][0], REF_INDICES_RAW[-1][0], 500)

#plot.exact_sca_ext(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1, "./output/exact_sca_ext.png")
#plot.exact_sca_ext_surface(REF_INDICES_RAW, WAVELENGTHS, 50e-9, 100e-9, 50, 3 + 1, "./output/exact_sca_ext_surface.png")
#plot.integ_sca(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 0, 2 * math.pi, 0, math.pi, 50, 3 + 1, "./output/integ_sca.png")
#plot.integ_sca_surface(REF_INDICES_RAW, WAVELENGTHS, 50e-9, 100e-9, 50, 0, 2 * math.pi, 0, math.pi, 50, 3 + 1, "./output/integ_sca_surface.png")
#plot.integ_sca_by_triangle(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1, "./res/sphere.ply", "./output/integ_sca_by_triangle.png")
plot.integ_sca_surface_by_triangle(REF_INDICES_RAW, WAVELENGTHS, 50e-9, 100e-9, 50, 3 + 1, "./res/whole-low.ply", "./output/integ_sca_surface_by_triangle.png")