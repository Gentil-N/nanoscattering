import plot
import inout
import numpy as np
import math
from scipy import stats
import mietheory

import utils
from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

#x = np.linspace(0, 9, 100)
#y1 = x**2
#y2 = 0.9 * x**2
#print(stats.ks_2samp(y1, y2))

REF_INDICES_RAW = inout.load_ref_index("./res/refractive-index-silicon-2.csv")
WAVELENGTHS = np.linspace(REF_INDICES_RAW[0][0], REF_INDICES_RAW[-1][0], 100)

data_surface = inout.import_surface("./res/raw-disk-surface")
data_spectrum = inout.import_spectrum("./res/spectrum")
one_spec = data_surface[2][int(len(data_surface[2]) / 2)]
new_spec = utils.redistribute(data_spectrum[0], data_spectrum[1], WAVELENGTHS)
rescaled_spec = utils.rescale(one_spec, new_spec)
plt.plot(WAVELENGTHS, one_spec)
plt.plot(WAVELENGTHS, rescaled_spec)
plt.show()

#data = inout.import_spectrum("./res/spectrum_32_38")
#original_wavelengths = data[0] * 1e-9
#original_spectrum = data[1]
#new_spectrum = utils.redistribute(original_wavelengths, original_spectrum, WAVELENGTHS)
#fig0 = plt.figure(num=0)
#ax0 = fig0.subplots(nrows=1, ncols=1)
#ax0.plot(original_wavelengths, original_spectrum)
#fig1 = plt.figure(num=1)
#ax1 = fig1.subplots(nrows=1, ncols=1)
#ax1.plot(WAVELENGTHS, new_spectrum)
#plt.show()

#x = np.linspace(0, 10, 11)
#new_x = np.linspace(0, 20, 21)
#y = x**2
#new_y = utils.redistribute(x, y, new_x)
#plt.plot(x, y)
#plt.plot(new_x, new_y)
#plt.show()