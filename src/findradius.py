import inout
import numpy as np
import utils
from matplotlib import pyplot as plt
import os

files_spectrum = ["./res/spectrum-test-67nm", "./res/spectrum-test-72nm", "./res/spectrum-test-82nm"]

data_surface = inout.import_surface("./res/surface-test")
for filespec in files_spectrum:
    data_spectrum = inout.import_spectrum(filespec)
    index, spectrum = utils.find_matching(data_surface, data_spectrum)
    print("Estimated Radius (", filespec, "): ", data_surface[1][index], "m")
    plt.plot(data_surface[0], data_surface[2][index])
    plt.plot(data_surface[0], spectrum)
    inout.show_plot("./output/find_matching_" + os.path.basename(filespec) + ".png")