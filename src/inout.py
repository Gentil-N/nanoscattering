import plyfile as pf
from collada import *
import utils
import numpy as np
from matplotlib import pyplot as plt
import sys
import math
import os

INTERACTIVE_ENV=True

def load_ref_index(filename):
    """
    Load a refractive index file returning a list of (wavelength, real part, imaginary part)
    """
    ref_file = open(filename, 'r')
    lines = ref_file.readlines()
    data = []
    for line in lines:
        numbers = line.split(',')
        data.append((float(numbers[0].strip()) * 1e-6, float(numbers[1].strip()), float(numbers[2].strip())))
    ref_file.close()
    return data

def load_triangle_by_color(filename):
    """
    Load a 'ply' file with all colorized (not white) triangles returning spherical coordinates (phi & theta, indices) 
    """
    data = pf.PlyData.read(filename)
    point_coords = []
    for vertex in data.elements[0]:
        if not(utils.is_white(vertex[3], vertex[4], vertex[5])):
            point_coords.append(utils.transform_cartesian_to_spherical_angles(vertex[0], vertex[1], vertex[2]))
        else:
            point_coords.append((7.7, 7.7))
    indices = []
    #print(len(data.elements[1]))
    for face in data.elements[1]:
        if len(face[0]) == 3:
            vert_0 = data.elements[0][face[0][0]]
            vert_1 = data.elements[0][face[0][1]]
            vert_2 = data.elements[0][face[0][2]]
            if utils.triangle_has_no_white(vert_0, vert_1, vert_2):
                indices.append(face[0][0])
                indices.append(face[0][1])
                indices.append(face[0][2])
        elif len(face[0]) == 4:
            vert_0 = data.elements[0][face[0][0]]
            vert_1 = data.elements[0][face[0][1]]
            vert_2 = data.elements[0][face[0][2]]
            vert_3 = data.elements[0][face[0][3]]
            if utils.triangle_has_no_white(vert_0, vert_1, vert_2):
                indices.append(face[0][0])
                indices.append(face[0][1])
                indices.append(face[0][2])
            if utils.triangle_has_no_white(vert_2, vert_3, vert_0):
                indices.append(face[0][2])
                indices.append(face[0][3])
                indices.append(face[0][0])
    #print(len(point_coords))
    #print(len(indices))
    export_collada(point_coords, indices, "./output/" + os.path.basename(filename) + ".dae")
    return (point_coords, indices)

def load_triangle_by_angle(filename, theta_a, theta_i):
    """
    Load a 'ply' file with triangles (included in collection angles) returning spherical coordinates (phi & theta, indices) 
    """
    data = pf.PlyData.read(filename)
    point_coords = []
    #vertices = []
    radius = math.sin(theta_a)
    c = math.cos(theta_a)
    center = (c * math.sin(theta_i), 0.0, -c * math.cos(theta_i))
    for vertex in data.elements[0]:
        if utils.is_inside_sphere(center, radius, (vertex[0], vertex[1], vertex[2])):
            #vertices.append((vertex[0], vertex[1], vertex[2]))
            point_coords.append(utils.transform_cartesian_to_spherical_angles(vertex[0], vertex[1], vertex[2]))
        else:
            #vertices.append((7.7, 7.7, 7.7))
            point_coords.append((7.7, 7.7))
    indices = []
    #print(len(data.elements[1]))
    for face in data.elements[1]:
        if len(face[0]) == 3:
            vert_0 = data.elements[0][face[0][0]]
            vert_1 = data.elements[0][face[0][1]]
            vert_2 = data.elements[0][face[0][2]]
            if utils.triangle_is_inside_sphere(center, radius, vert_0, vert_1, vert_2):
                indices.append(face[0][0])
                indices.append(face[0][1])
                indices.append(face[0][2])
        elif len(face[0]) == 4:
            vert_0 = data.elements[0][face[0][0]]
            vert_1 = data.elements[0][face[0][1]]
            vert_2 = data.elements[0][face[0][2]]
            vert_3 = data.elements[0][face[0][3]]
            if utils.triangle_is_inside_sphere(center, radius, vert_0, vert_1, vert_2):
                indices.append(face[0][0])
                indices.append(face[0][1])
                indices.append(face[0][2])
            if utils.triangle_is_inside_sphere(center, radius, vert_2, vert_3, vert_0):
                indices.append(face[0][2])
                indices.append(face[0][3])
                indices.append(face[0][0])
    #print(len(point_coords))
    #print(len(indices))
    #export_collada(point_coords, indices, "./output/" + os.path.basename(filename) + ".dae")
    #export_collada_3D(vertices, indices, "./output/" + os.path.basename(filename) + ".dae")
    return (point_coords, indices)

def export_collada(point_coords, indices, filename):
    """
    Export a mesh with a 'spherical coordinate' structure to collada format
    """
    mesh = Collada()
    vertices = []
    for coord in point_coords:
        vertices.append(coord[0])
        vertices.append(coord[1])
        vertices.append(0.0)
    vert_src = source.FloatSource("cubeverts-array", np.array(vertices), ('X', 'Y', 'Z'))
    geom = geometry.Geometry(mesh, "geometry0", "mycube", [vert_src])
    input_list = source.InputList()
    input_list.addInput(0, 'VERTEX', "#cubeverts-array")
    triset = geom.createTriangleSet(np.array(indices), input_list, "materialref")
    geom.primitives.append(triset)
    mesh.geometries.append(geom)
    geomnode = scene.GeometryNode(geom)
    node = scene.Node("node0", children=[geomnode])
    myscene = scene.Scene("myscene", [node])
    mesh.scenes.append(myscene)
    mesh.scene = myscene
    mesh.write(filename)

def export_collada_3D(vertices, indices, filename):
    """
    Export a mesh with a 'spherical coordinate' structure to collada format
    """
    mesh = Collada()
    vert_src = source.FloatSource("cubeverts-array", np.array(vertices), ('X', 'Y', 'Z'))
    geom = geometry.Geometry(mesh, "geometry0", "mycube", [vert_src])
    input_list = source.InputList()
    input_list.addInput(0, 'VERTEX', "#cubeverts-array")
    triset = geom.createTriangleSet(np.array(indices), input_list, "materialref")
    geom.primitives.append(triset)
    mesh.geometries.append(geom)
    geomnode = scene.GeometryNode(geom)
    node = scene.Node("node0", children=[geomnode])
    myscene = scene.Scene("myscene", [node])
    mesh.scenes.append(myscene)
    mesh.scene = myscene
    mesh.write(filename)

def show_plot(filename):
    plt.savefig(filename)
    plt.show()

def export_spectrum(wavelengths, spectrum, filename):
    """
    Export a spectrum given by 'f(wavelengths)=spectrum'
    """
    outfile = open(filename, 'w')
    for i in range(len(wavelengths)):
        outfile.write(str(wavelengths[i]) + "\t" + str(spectrum[i]) + "\n")
    outfile.close()

def export_surface(wavelengths, partsizes, surface, filename):
    """
    Export a surface given by 'f(wavelengths, partsizes)=surface'
    """
    outfile = open(filename, 'w')
    for i in range(len(wavelengths)):
        outfile.write(str(wavelengths[i]) + "\n")
    for i in range(len(partsizes)):
        outfile.write("#\t" + str(partsizes[i]) + "\n")
        for j in range(len(wavelengths)):
            outfile.write(str(surface[i][j]) + "\n")
    outfile.close()

def import_spectrum(filename):
    """
    Reciprocal from spectrum exporter
    """
    wavelengths = []
    spectrum = []
    infile = open(filename, 'r')
    lines = infile.readlines()
    for line in lines:
        data = line.split()
        wavelengths.append(float(data[0]))
        spectrum.append(float(data[1]))
    infile.close()
    return (np.array(wavelengths), np.array(spectrum))

def import_surface(filename):
    """
    Reciprocal from surface exporter
    """
    wavelengths = []
    partsizes = []
    surface = []
    infile = open(filename, 'r')
    lines = infile.readlines()
    first_partsize = 0
    for i in range(len(lines)):
        data = lines[i].split()
        if data[0] == "#":
            first_partsize = i
            partsizes.append(float(data[1]))
            break
        else:
            wavelengths.append(float(data[0]))
    local_spectrum = []
    for i in range(first_partsize + 1, len(lines)):
        data = lines[i].split()
        if data[0] == "#":
            partsizes.append(float(data[1]))
            surface.append(local_spectrum.copy())
            local_spectrum = []
        else:
            local_spectrum.append(float(data[0]))
    surface.append(local_spectrum.copy())
    return (np.array(wavelengths), np.array(partsizes), np.array(surface))

def get_input_args():
    return sys.argv[1:]