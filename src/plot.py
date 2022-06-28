import mietheory
from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import numpy as np
import inout
import threading
import multiprocessing

def exact_sca_ext(ref_indices_raw, wavelengths, particle_size, order_len, output_filename):
    res = mietheory.ccs_exact(ref_indices_raw, wavelengths, particle_size, order_len)
    fig0 = plt.figure(num=0)
    ax0 = fig0.subplots(nrows=1, ncols=1)
    ax0.set_title("Scattering Cross Section with Coeff")
    ax0.plot(wavelengths, res[0], label="Sca Total")
    ax0.plot(wavelengths, res[1], label="Ext Total")
    ax0.plot(wavelengths, res[1] - res[0], label="Abs")
    ax0.set(xlabel="wavelength")
    ax0.legend()
    ax0.grid()
    inout.show_plot(output_filename)

def exact_sca_ext_surface(ref_indices_raw, wavelengths, partsize_lower, partsize_upper, number_partsizes, order_len, output_filename):
    partsizes = np.linspace(partsize_lower, partsize_upper, number_partsizes)
    scattering_cross_section = np.zeros((len(partsizes), len(wavelengths)))
    extinction_cross_section = np.zeros((len(partsizes), len(wavelengths)))
    for i in range(len(partsizes)):
        res = mietheory.ccs_exact(ref_indices_raw, wavelengths, partsizes[i], order_len)
        scattering_cross_section[i] = res[0]
        extinction_cross_section[i] = res[1]
    fig0 = plt.figure(num=0)
    fig1 = plt.figure(num=1)
    ax0 = fig0.subplots(nrows=1, ncols=1)
    ax1 = fig1.subplots(nrows=1, ncols=1)
    ax0.set_title("Scattering Cross Section")
    ax0.contourf(wavelengths, partsizes, scattering_cross_section, cmap='inferno', levels=70)
    ax0.set(xlabel="wavelength", ylabel="particle radius")
    ax1.set_title("Extinction Cross Section")
    ax1.contourf(wavelengths, partsizes, extinction_cross_section, cmap='inferno', levels=70)
    ax1.set(xlabel="wavelength", ylabel="particle radius")
    fig0.colorbar(mappable=ScalarMappable(norm=Normalize(vmin=0, vmax=10), cmap='inferno'), ax=ax0)
    fig1.colorbar(mappable=ScalarMappable(norm=Normalize(vmin=0, vmax=10), cmap='inferno'), ax=ax1)
    inout.show_plot(output_filename)

def integ_sca(ref_indices_raw, wavelengths, particle_size, phi_inf, phi_sup, theta_inf, theta_sup, integ_point_count, order_len, output_filename):
    res0 = mietheory.ccs_integ(ref_indices_raw, wavelengths, particle_size, phi_inf, phi_sup, theta_inf, theta_sup, integ_point_count, order_len)
    fig0 = plt.figure(num=0)
    ax0 = fig0.subplots(nrows=1, ncols=1)
    ax0.set_title("Scattering Cross Sections")
    ax0.plot(wavelengths, res0, label="Integrated")
    ax0.set(xlabel="wavelength")
    ax0.legend()
    ax0.grid()
    inout.show_plot(output_filename)

def integ_sca_surface(ref_indices_raw, wavelengths, partsize_lower, partsize_upper, number_partsizes, phi_inf, phi_sup, theta_inf, theta_sup, integ_point_count, order_len, output_filename):
    partsizes = np.linspace(partsize_lower, partsize_upper, number_partsizes)
    scattering_cross_section = np.zeros((len(partsizes), len(wavelengths)))
    for i in range(len(partsizes)):
        scattering_cross_section[i] = mietheory.ccs_integ(ref_indices_raw, wavelengths, partsizes[i], phi_inf, phi_sup, theta_inf, theta_sup, integ_point_count, order_len)
    fig0 = plt.figure(num=0)
    ax0 = fig0.subplots(nrows=1, ncols=1)
    ax0.set_title("Scattering Cross Section")
    ax0.contourf(wavelengths, partsizes, scattering_cross_section, cmap='inferno', levels=70)
    ax0.set(xlabel="wavelength", ylabel="particle radius")
    fig0.colorbar(mappable=ScalarMappable(norm=Normalize(vmin=0, vmax=10), cmap='inferno'), ax=ax0)
    inout.show_plot(output_filename)

def integ_sca_by_triangle(ref_indices_raw, wavelengths, particle_size, order_len, filename, output_filename):
    data = inout.load_selected_triangle(filename)
    res0 = mietheory.ccs_integ_triangle(ref_indices_raw, wavelengths, particle_size, data[0], data[1], order_len)
    fig0 = plt.figure(num=0)
    ax0 = fig0.subplots(nrows=1, ncols=1)
    ax0.set_title("Scattering Cross Sections")
    ax0.plot(wavelengths, res0, label="Integrated")
    ax0.set(xlabel="wavelength")
    ax0.legend()
    ax0.grid()
    inout.show_plot(output_filename)

def integ_sca_surface_by_triangle(ref_indices_raw, wavelengths, partsize_lower, partsize_upper, number_partsizes, order_len, filename, output_filename):
    partsizes = np.linspace(partsize_lower, partsize_upper, number_partsizes)
    scattering_cross_section = np.zeros((len(partsizes), len(wavelengths)))
    data = inout.load_selected_triangle(filename)
    def calcul(index):
        print("start:", index)
        scattering_cross_section[index] = mietheory.ccs_integ_triangle(ref_indices_raw, wavelengths, partsizes[index], data[0], data[1], order_len)
        print("end:", index)
    max_cores = multiprocessing.cpu_count()
    print("max cores:", max_cores)
    threads = []
    for i in range(0, len(partsizes)):
        while len(threads) == max_cores:
            for j in range(len(threads)):
                if not threads[j].is_alive():
                    del threads[j]
                    break
        new_thread = threading.Thread(target=calcul, args=(i,))
        new_thread.start()
        threads.append(new_thread)
        #def tafun():
        #    scattering_cross_section[i] = mietheory.ccs_integ_triangle(ref_indices_raw, wavelengths, partsizes[i], data[0], data#[1], order_len)
        #def tbfun():
        #    scattering_cross_section[i + 1] = mietheory.ccs_integ_triangle(ref_indices_raw, wavelengths, partsizes[i + 1], data#[0], data[1], order_len)
        #ta = threading.Thread(target=tafun)
        #tb = threading.Thread(target=tbfun)
        #ta.start()
        #tb.start()
        #ta.join()
        #tb.join()
        #scattering_cross_section[i] = mietheory.ccs_integ_triangle(ref_indices_raw, wavelengths, partsizes[i], data[0], data[1], order_len)
    fig0 = plt.figure(num=0)
    ax0 = fig0.subplots(nrows=1, ncols=1)
    ax0.set_title("Scattering Cross Section")
    ax0.contourf(wavelengths, partsizes, scattering_cross_section, cmap='inferno', levels=70)
    ax0.set(xlabel="wavelength", ylabel="particle radius")
    fig0.colorbar(mappable=ScalarMappable(norm=Normalize(vmin=0, vmax=10), cmap='inferno'), ax=ax0)
    inout.show_plot(output_filename)