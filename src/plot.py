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

def exact_sca_ext_surface(ref_indices_raw, wavelengths, partsizes, order_len, output_filename):
    res = mietheory.ccs_exact_surface(ref_indices_raw, wavelengths, partsizes, order_len)
    scattering_cross_section = res[0]
    extinction_cross_section = res[1]
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

def integ_sca_surface(ref_indices_raw, wavelengths, partsizes, phi_inf, phi_sup, theta_inf, theta_sup, integ_point_count, order_len, output_filename):
    scattering_cross_section = mietheory.ccs_integ_surface(ref_indices_raw, wavelengths, partsizes, phi_inf, phi_sup, theta_inf, theta_sup, integ_point_count, order_len)
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

def integ_sca_surface_by_triangle(ref_indices_raw, wavelengths, partsizes, order_len, filename, output_filename):
    data = inout.load_selected_triangle(filename)
    scattering_cross_section[index] = mietheory.ccs_integ_triangle_surface(ref_indices_raw, wavelengths, partsizes, data[0], data[1], order_len)
    fig0 = plt.figure(num=0)
    ax0 = fig0.subplots(nrows=1, ncols=1)
    ax0.set_title("Scattering Cross Section")
    ax0.contourf(wavelengths, partsizes, scattering_cross_section, cmap='inferno', levels=70)
    ax0.set(xlabel="wavelength", ylabel="particle radius")
    fig0.colorbar(mappable=ScalarMappable(norm=Normalize(vmin=0, vmax=10), cmap='inferno'), ax=ax0)
    inout.show_plot(output_filename)