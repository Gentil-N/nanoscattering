import plot
import inout
import numpy as np
import math
import threading
import multiprocessing
import time
import sys

REF_INDICES_RAW = inout.load_ref_index("./res/refractive-index-silicon-2.csv")
WAVELENGTHS = np.linspace(REF_INDICES_RAW[0][0], REF_INDICES_RAW[-1][0], 500)

#plot.exact_sca_ext(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1, "./output/exact_sca_ext.png")
#plot.exact_sca_ext_surface(REF_INDICES_RAW, WAVELENGTHS, 50e-9, 100e-9, 50, 3 + 1, "./output/exact_sca_ext_surface.png")
#plot.integ_sca(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 0, 2 * math.pi, 0, math.pi, 50, 3 + 1, "./output/integ_sca.png")
#plot.integ_sca_surface(REF_INDICES_RAW, WAVELENGTHS, 50e-9, 100e-9, 50, 0, 2 * math.pi, 0, math.pi, 50, 3 + 1, "./output/integ_sca_surface.png")
#plot.integ_sca_by_triangle(REF_INDICES_RAW, WAVELENGTHS, 80e-9, 3 + 1, "./res/sphere.ply", "./output/integ_sca_by_triangle.png")
plot.integ_sca_surface_by_triangle(REF_INDICES_RAW, WAVELENGTHS, 50e-9, 100e-9, 50, 3 + 1, "./res/sphere.ply", "./output/integ_sca_surface_by_triangle.png")

#print(multiprocessing.cpu_count())
#def print_haha():
#    a = 0
#    for i in range(1000):
#        a -= i
#    time.sleep(2)
#    print("haha")
#    return a
#def print_hihi():
#    a = 0
#    for i in range(1000):
#        a += i
#    time.sleep(2)
#    print("hihi")
#    return a
#ta = threading.Thread(target=print_haha)
#ti = threading.Thread(target=print_hihi)
#ta.start()
#ti.start()
#while ta.is_alive() and ti.is_alive():
#    print("huhu")