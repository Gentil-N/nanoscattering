import math
import cmath

def trapz(func, inf, sup, div):
    step = (sup - inf) / div
    res = 0
    for i in range(div):
        a = i * step + inf
        b = a + step
        res += (func(a) + func(b)) * (step) / 2
    return res

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def clamp(val, mmin, mmax):
    return max(min(val, mmax), mmin)

def sign(val):
    if val < 0:
        return -1
    else:
        return 1

def transform_cartesian_to_spherical_angles(x, y, z):
    r = math.sqrt(x**2 + y**2 + z**2)
    cos_theta = z / r
    theta = math.acos(cos_theta)
    if x > 0:
        return (math.atan(y / x), theta)
    if x < 0 and y >= 0:
        return (math.atan(y / x) + math.pi, theta)
    if x < 0 and y < 0:
        return (math.atan(y / x) - math.pi, theta)
    if x == 0 and y > 0:
        return (math.pi / 2, theta)
    if x == 0 and y < 0:
        return (-math.pi / 2, theta)
    else:
        return (0.0, theta)

def is_white(r, g, b):
    return (r == 255 and g == 255 and b == 255)

def triangle_has_no_white(vert_0, vert_1, vert_2):
    if not(is_white(vert_0[3], vert_0[4], vert_0[5])) and not(is_white(vert_1[3], vert_1[4], vert_1[5])) and not(is_white(vert_2[3],vert_2[4], vert_2[5])):
        return True
    return False

def get_ref_index(data, wavelength):
    for i in range(len(data) - 1):
        if data[i][0] <= wavelength and data[i + 1][0] >= wavelength:
            alpha_re = (data[i + 1][1] - data[i][1]) / (data[i + 1][0] - data[i][0])
            gamma_re = data[i][1] - alpha_re * data[i][0]
            ref_re = alpha_re * wavelength + gamma_re
            alpha_im = (data[i + 1][2] - data[i][2]) / (data[i + 1][0] - data[i][0])
            gamma_im = data[i][2] - alpha_im * data[i][0]
            ref_im = alpha_im * wavelength + gamma_im
            return complex(ref_re, ref_im)
    return complex(data[0][1], data[0][2])

def volume_uniform(phi_theta_1, phi_theta_2, phi_theta_3, res1, res2, res3):
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    if res1 < res2:
        if res3 < res1:
            d = res3
            e = res1
            f = res2
            a = distance(phi_theta_3, phi_theta_1)
            b = distance(phi_theta_3, phi_theta_2)
            c = distance(phi_theta_1, phi_theta_2)
        elif res2 < res3:
            d = res1
            e = res2
            f = res3
            a = distance(phi_theta_1, phi_theta_2)
            b = distance(phi_theta_1, phi_theta_3)
            c = distance(phi_theta_3, phi_theta_2)
        else:
            d = res1
            e = res3
            f = res2
            a = distance(phi_theta_1, phi_theta_3)
            b = distance(phi_theta_1, phi_theta_2)
            c = distance(phi_theta_3, phi_theta_2)
    else:
        if res3 < res2:
            d = res3
            e = res2
            f = res1
            a = distance(phi_theta_3, phi_theta_2)
            b = distance(phi_theta_3, phi_theta_1)
            c = distance(phi_theta_1, phi_theta_2)
        elif res1 < res3:
            d = res2
            e = res1
            f = res3
            a = distance(phi_theta_2, phi_theta_1)
            b = distance(phi_theta_2, phi_theta_3)
            c = distance(phi_theta_1, phi_theta_3)
        else:
            d = res2
            e = res3
            f = res1
            a = distance(phi_theta_2, phi_theta_3)
            b = distance(phi_theta_2, phi_theta_1)
            c = distance(phi_theta_3, phi_theta_1)
    if a == 0 or c == 0:
        return 0
    h = a * math.sin(math.acos(clamp((a**2 + c**2 - b**2) / (2 * a * c), -1, 1)))
    v1 = 0.5 * c * h * d
    v2 = (1/6) * (f + e) * c * h
    return (v1 + v2)

def volume_varying(phi_theta_1, phi_theta_2, phi_theta_3, d1, d2, d3):
    c1 = distance(phi_theta_1, phi_theta_3)
    c2 = distance(phi_theta_1, phi_theta_2)
    c3 = distance(phi_theta_2, phi_theta_3)
    gammad1 = math.sin(math.acos(clamp((c1**2 + c2**2 - c3**2) / (2 * c1 * c2), -1, 1)))
    gammad2 = math.sin(math.acos(clamp((c2**2 + c3**2 - c1**2) / (2 * c2 * c3), -1, 1)))
    if d2 == 0:
        div = (1 + d1 / d3)
        return (1/6) * (-1 * d1**2 * c1 * c2 * gammad1 / (d3 * div) + d3 * c1 * c2 * gammad1 / div)
    if d3 == 0:
        div = (1 + d1 / d2)
        return (1/6) * (-1 * c1 * d1**2 * c2 * gammad1 / (d2 * div) + d2 * c3 * c2 * gammad2 / div)
    div1 = (1 + d1 / d2)
    div = div1 * (1 + d1 / d3)
    v1 = (1/6) * d1**3 * c1 * c2 * gammad1 / (d3 * d2 * div)
    v2 = (1/6) * d3 * d1 * c1 * c2 * gammad1 / (d2 * div)
    v3 = (1/6) * (d2 + d3) * c3 * c2 * gammad2 / div1
    return -v1 + v2 + v3

def volume_triangle(phi_theta_1, phi_theta_2, phi_theta_3, res1, res2, res3):
    sign1 = sign(res1)
    sign2 = sign(res2)
    sign3 = sign(res3)
    if (res1 >= 0 and res2 >= 0 and res3 >= 0) or (res1 <= 0 and res2 <= 0 and res3 <= 0):
        return sign1 * volume_uniform(phi_theta_1, phi_theta_2, phi_theta_3, abs(res1), abs(res2), abs(res3))
    if sign1 + sign2 == 0:
        if sign2 == sign3:
            return sign2 * volume_varying(phi_theta_1, phi_theta_2, phi_theta_3, abs(res1), abs(res2), abs(res3))
        else:
            return sign3 * volume_varying(phi_theta_2, phi_theta_1, phi_theta_3, abs(res2), abs(res1), abs(res3))
    else:
        return  sign1 * volume_varying(phi_theta_3, phi_theta_1, phi_theta_2, abs(res3), abs(res1), abs(res2))