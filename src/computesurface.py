import plot
import inout
import numpy as np
import math
import mietheory

REF_INDICES_RAW = inout.load_ref_index("./res/refractive-index-silicon-2.csv")
WAVELENGTHS = np.linspace(REF_INDICES_RAW[0][0], REF_INDICES_RAW[-1][0], 100)
PARTSIZES = np.linspace(50e-9, 99e-9, 50)

data = inout.load_selected_triangle("./res/raw-disk-high.ply")
scattering_cross_section = mietheory.ccs_integ_triangle_surface(REF_INDICES_RAW, WAVELENGTHS, PARTSIZES, data[0], data[1], 3 + 1)
inout.export_surface(WAVELENGTHS, PARTSIZES, scattering_cross_section, "./output/raw-disk-surface")