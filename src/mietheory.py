from scipy import special
import numpy as np
import math
import utils
import inout
import multiprocessing
import threading
import time

def psi_array(sjn, z):
    return sjn * z

def xi_array(sjn, syn, z):
    return z * (sjn + complex(0, 1) * syn)

def xi_der_array(xin, z):
    xin_der = [complex(0.0)] * len(xin)
    for i in range(1, len(xin_der)):
        xin_der[i] = xin[i - 1] - i * xin[i] / z
    return xin_der
    

def d_array(psin, z):
    dn = [complex(0.0, 0.0)] * len(psin)
    #for i in range(1, len(dn)):
    #    dn[i] = psin[i - 1] / psin[i] - i / z
    psi_last = psin[-1]
    psi_before_last = psin[-2]
    dn[-1] = psi_before_last / psi_last - (len(psin) - 1) / z
    for i in range(len(psin) - 1, 0, -1):
        ndivz = i / z
        dn[i - 1] = ndivz - 1 / (dn[i] + ndivz)
    return dn

def pi_tau_array(n_len, theta):
    #assert n_len >= 3
    mu = math.cos(theta)
    pi_tau_n = [(0.0, 0.0)] * n_len
    pi_tau_n[0] = (0.0, 0.0)
    pi_tau_n[1] = (1.0, mu * 1.0 - 2 * 0.0)
    for i in range(2, len(pi_tau_n)):
        curr_pi = (2 * i - 1) / (i - 1) * mu * pi_tau_n[i - 1][0] - i / (i - 1) * pi_tau_n[i - 2][0]
        pi_tau_n[i] = (curr_pi, i * mu * curr_pi - (i + 1) * pi_tau_n[i - 1][0])
    return pi_tau_n

def a_array(m, psin, xin, dn, z):
    an = [complex(0.0, 0.0)] * len(psin)
    for i in range(1, len(an)):
        coeff_ai = dn[i] / m + i / z
        an[i] = (coeff_ai * psin[i] - psin[i - 1]) / (coeff_ai * xin[i] - xin[i - 1])
    return an

def b_array(m, psin, xin, dn, z):
    bn = [complex(0.0, 0.0)] * len(psin)
    for i in range(1, len(bn)):
        coeff_bi = dn[i] * m + i / z
        bn[i] = (coeff_bi * psin[i] - psin[i - 1]) / (coeff_bi * xin[i] - xin[i - 1])
    return bn

def en(n):
    return complex(0.0, 1.0)**n * (2 * n + 1) / (n * (n + 1))

def theta_func_first(an, bn, xin, xin_der, theta):
    pi_tau_n = pi_tau_array(len(an), theta)
    sum_first = 0
    sum_second = 0
    for i in range(1, len(an)):
        sum_first += en(i) * (complex(0.0, 1.0) * an[i] * xin_der[i] * pi_tau_n[i][1] - bn[i] * xin[i] * pi_tau_n[i][0])
        sum_second += en(i) * (complex(0.0, 1.0) * bn[i] * xin_der[i] * pi_tau_n[i][0] - an[i] * xin[i] * pi_tau_n[i][1])
    return (sum_first * sum_second.conjugate()).real * math.sin(theta)

def theta_func_second(an, bn, xin, xin_der, theta):
    pi_tau_n = pi_tau_array(len(an), theta)
    sum_first = 0
    sum_second = 0
    for i in range(1, len(an)):
        sum_first += en(i) * (bn[i] * xin[i] * pi_tau_n[i][1] - complex(0.0, 1.0) * an[i] * xin_der[i] * pi_tau_n[i][0])
        sum_second += en(i) * (complex(0.0, 1.0) * bn[i] * xin_der[i] * pi_tau_n[i][1] - an[i] * xin[i] * pi_tau_n[i][0])
    return (sum_first * sum_second.conjugate()).real * math.sin(theta)

def theta_func(an, bn, xin, xin_der, theta):
    pi_tau_n = pi_tau_array(len(an), theta)
    sum_first = 0
    sum_second = 0
    sum_third = 0
    sum_fourth = 0
    for i in range(1, len(an)):
        sum_first += en(i) * (complex(0.0, 1.0) * an[i] * xin_der[i] * pi_tau_n[i][1] - bn[i] * xin[i] * pi_tau_n[i][0])
        sum_second += en(i) * (complex(0.0, 1.0) * bn[i] * xin_der[i] * pi_tau_n[i][0] - an[i] * xin[i] * pi_tau_n[i][1])
        sum_third += en(i) * (bn[i] * xin[i] * pi_tau_n[i][1] - complex(0.0, 1.0) * an[i] * xin_der[i] * pi_tau_n[i][0])
        sum_fourth += en(i) * (complex(0.0, 1.0) * bn[i] * xin_der[i] * pi_tau_n[i][1] - an[i] * xin[i] * pi_tau_n[i][0])
    return (sum_first * sum_second.conjugate()).real * math.sin(theta) - (sum_third * sum_fourth.conjugate()).real * math.sin(theta)

def function_value(an, bn, xin_x, xin_der_x, phi_theta):
    return math.cos(phi_theta[0])**2 * theta_func_first(an, bn, xin_x, xin_der_x, phi_theta[1]) - math.sin(phi_theta[0])**2 * theta_func_second(an, bn, xin_x, xin_der_x, phi_theta[1])

### COMPUTE CROSS SECTION

def ccs_generic(ref_indices_raw, wavelengths, particle_size, spefun, order_len, medium_n=1.0):
    upper_x = 2 * math.pi * medium_n * particle_size
    print(particle_size, ": 0.0 %", end='\r', flush=True)
    for j in range(len(wavelengths)):
        #print(wavelengths[j])
        x = upper_x / wavelengths[j]
        m = utils.get_ref_index(ref_indices_raw, wavelengths[j]) / medium_n
        mx = m * x
    
        sjn_x = []
        syn_x = []
        psin_x = []
        xin_x = []
        xin_der_x = []
        sjn_mx = []
        psin_mx = []
        dn_mx = []
        for i in range(order_len):
            sjn_x.append(special.spherical_jn(i, x))
            syn_x.append(special.spherical_yn(i, x))
            psin_x.append(psi_array(sjn_x[i], x))
            xin_x.append(xi_array(sjn_x[i], syn_x[i], x))

            sjn_mx.append(special.spherical_jn(i, mx))
            psin_mx.append(psi_array(sjn_mx[i], mx))

        xin_der_x = xi_der_array(xin_x, x)
        dn_mx = d_array(psin_mx, mx)
        an = a_array(m, psin_x, xin_x, dn_mx, x)
        bn = b_array(m, psin_x, xin_x, dn_mx, x)

        spefun(j, xin_x, xin_der_x, an, bn)

        print(particle_size, ":", float(int(j / len(wavelengths) * 1000)) / 10, " %", end='\r', flush=True)
    print(particle_size, ": 100.0 %", flush=True)

def ccs_surface_generic(partsizes, spefun):
    res = []
    def calcul(index):
        print("start:", index, " ", partsizes[index])
        res.append(spefun(index))
        print("end:", index, " ", partsizes[index])
    max_cores = multiprocessing.cpu_count()
    threads = []
    for i in range(0, len(partsizes)):
        while len(threads) == max_cores:
            #time.sleep(5)
            for j in range(len(threads)):
                if not threads[j].is_alive():
                    del threads[j]
                    break
        new_thread = threading.Thread(target=calcul, args=(i,))
        new_thread.start()
        threads.append(new_thread)
    for thread in threads:
        thread.join()
    return res

# EXACT

def ccs_exact(ref_indices_raw, wavelengths, particle_size, order_len):

    medium_n = 1.0

    res_sca = np.zeros(len(wavelengths), dtype=float)
    res_ext = np.zeros(len(wavelengths), dtype=float)
    res_sca_an = np.zeros(len(wavelengths), dtype=float)
    res_sca_bn = np.zeros(len(wavelengths), dtype=float)
    res_ext_an = np.zeros(len(wavelengths), dtype=float)
    res_ext_bn = np.zeros(len(wavelengths), dtype=float)

    def spefun(j, xin_x, xin_der_x, an, bn):
        mul = (wavelengths[j] / medium_n)**2 / (2 * math.pi) / (particle_size**2 * math.pi)
        part_res_sca = [0] * order_len
        part_res_ext = [0] * order_len
        part_res_sca_an = [0] * order_len
        part_res_sca_bn = [0] * order_len
        part_res_ext_an = [0] * order_len
        part_res_ext_bn = [0] * order_len
        for i in range(1, order_len):
            part_res_sca_an[i] = (2 * i + 1) * (an[i].real**2 + an[i].imag**2)
            part_res_sca_bn[i] = (2 * i + 1) * (bn[i].real**2 + bn[i].imag**2)
            part_res_ext_an[i] = (2 * i + 1) * an[i].real
            part_res_ext_bn[i] = (2 * i + 1) * bn[i].real
            part_res_sca[i] = part_res_sca_an[i] + part_res_sca_bn[i]
            part_res_ext[i] = part_res_ext_an[i] + part_res_ext_bn[i]
        res_sca_an[j] = mul * sum(part_res_sca_an)
        res_sca_bn[j] = mul * sum(part_res_sca_bn)
        res_ext_an[j] = mul * sum(part_res_ext_an)
        res_ext_bn[j] = mul * sum(part_res_ext_bn)
        res_sca[j] = mul * sum(part_res_sca)
        res_ext[j] = mul * sum(part_res_ext)

    ccs_generic(ref_indices_raw, wavelengths, particle_size, spefun, order_len, medium_n)
    return (res_sca, res_ext, res_sca_an, res_sca_bn, res_ext_an, res_ext_bn)

def ccs_exact_surface(ref_indices_raw, wavelengths, partsizes, order_len):
    sca = np.zeros((len(partsizes), len(wavelengths)))
    ext = np.zeros((len(partsizes), len(wavelengths)))
    sca_an = np.zeros((len(partsizes), len(wavelengths)))
    sca_bn = np.zeros((len(partsizes), len(wavelengths)))
    ext_an = np.zeros((len(partsizes), len(wavelengths)))
    ext_bn = np.zeros((len(partsizes), len(wavelengths)))
    def spefun(index):
        res = ccs_exact(ref_indices_raw, wavelengths, partsizes[index], order_len)
        sca[index] = res[0]
        ext[index] = res[1]
        sca_an[index] = res[2]
        sca_bn[index] = res[3]
        ext_an[index] = res[4]
        ext_bn[index] = res[5]
    
    ccs_surface_generic(partsizes, spefun)
    return (sca, ext, sca_an, sca_bn, ext_an, ext_bn)

# NORMAL INTEGRATION

def ccs_integ(ref_indices_raw, wavelengths, particle_size, phi_inf, phi_sup, theta_inf, theta_sup, integ_point_count, order_len):

    medium_n = 1.0

    res = np.zeros(len(wavelengths), dtype=float)

    def spefun(j, xin_x, xin_der_x, an, bn):

        integ_phi_first = utils.trapz(lambda phi: math.cos(phi)**2, phi_inf, phi_sup, integ_point_count)
        integ_phi_second = utils.trapz(lambda phi: math.sin(phi)**2, phi_inf, phi_sup, integ_point_count)
        mul = 0.5 * wavelengths[j]**2 * 0.318 / (2 * math.pi) / (particle_size**2 * math.pi)
        integ_theta_first = utils.trapz(lambda theta: theta_func_first(an, bn, xin_x, xin_der_x, theta), theta_inf, theta_sup, integ_point_count)
        integ_theta_second = utils.trapz(lambda theta: theta_func_second(an, bn, xin_x, xin_der_x, theta), theta_inf, theta_sup, integ_point_count)

        res[j] = (integ_phi_first * integ_theta_first - integ_phi_second * integ_theta_second) * mul

    ccs_generic(ref_indices_raw, wavelengths, particle_size, spefun, order_len, medium_n)
    return res

def ccs_integ_surface(ref_indices_raw, wavelengths, partsizes, phi_inf, phi_sup, theta_inf, theta_sup, integ_point_count, order_len):
    sca = np.zeros((len(partsizes), len(wavelengths)))
    def spefun(index):
        sca[index] = ccs_integ(ref_indices_raw, wavelengths, partsizes[index], phi_inf, phi_sup, theta_inf, theta_sup, integ_point_count, order_len)
    ccs_surface_generic(partsizes, spefun)
    return sca

# INTEGRATION BY TRIANGLE

def ccs_integ_triangle(ref_indices_raw, wavelengths, particle_size, point_coords, indices, order_len):

    medium_n = 1.0

    res = np.zeros(len(wavelengths), dtype=float)

    def spefun(j, xin_x, xin_der_x, an, bn):
        
        mul = 0.5 * wavelengths[j]**2 * 0.318 / (2 * math.pi) / (particle_size**2 * math.pi)

        curr_res = 0
        fn_values = []
        for coord in point_coords:
            if coord == (7.7, 7.7):
                fn_values.append(0)
            else:
                fn_values.append(function_value(an, bn, xin_x, xin_der_x, coord))

        for i in range(0, int(len(indices)), 3):
            a = point_coords[indices[i]]
            b = point_coords[indices[i + 1]]
            c = point_coords[indices[i + 2]]
            comp = utils.volume_triangle(a, b, c, fn_values[indices[i]], fn_values[indices[i + 1]], fn_values[indices[i + 2]])
            curr_res += comp

        res[j] = curr_res * mul * 0.624
    
    ccs_generic(ref_indices_raw, wavelengths, particle_size, spefun, order_len, medium_n)
    return res

def ccs_integ_triangle_surface(ref_indices_raw, wavelengths, partsizes, point_coords, indices, order_len):
    sca = np.zeros((len(partsizes), len(wavelengths)))
    def spefun(index):
        sca[index] = ccs_integ_triangle(ref_indices_raw, wavelengths, partsizes[index], point_coords, indices, order_len)
    ccs_surface_generic(partsizes, spefun)
    return sca