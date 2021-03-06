import sys
import os
import argparse
import numpy as np
from scipy import constants

class Parameter(object):

    def __init__(self,name,value=None, unit=None):
        self.name(name)
        self.value(value)
        self.unit(unit)

    def name(self,value=None):
        """
        Standard get/set functionality for the name of the parameter.
        Allows chaining.
        """
        if value is None:
            return self.n
        self.n = value
        return self

    def value(self,value=None):
        """
        Standard get/set functionality for the name of the parameter.
        Allows chaining.
        """
        if value is None:
            return self.v
        self.v = value
        return self

    def unit(self,value=None):
        """
        Standard get/set functionality for the unit of the parameter.
        Allows chaining.
        """
        if value is None:
            return self.u
        self.u = value
        return self

    def __str__(self):
        """
        Converts the parameter to a string for printing.
        """
        output = [self.name()]
        if self.value() is not None:
            value = str(self.value())
            if self.unit() is not None:
                value += " " + self.unit()
            output.append(value)
        return " = ".join(output)

class ParameterContainer(object):

    def __init__(self):
        self.parameters = []

    def addParameter(self,name,*args,**kwargs):
        """
        Add the parameter with the given name to the paramters set.
        """
        self.parameters.append(Parameter(name,*args,**kwargs))

    def getParameter(self,name):
        """
        Returns the parameter with the give name.
        """
        for parameter in self:
            if parameter.name() == name:
                return parameter
        return None

    def __iter__(self):
        """
        Allows us to iterate over the object instead of referencing parameters.
        """
        for parameter in self.parameters:
            yield parameter

    def __str__(self):
        """
        Joins all of the parameters with new lines between them.
        """
        output = []
        for parameter in self:
            output.append(str(parameter))
        return "\n".join(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='For the unifying USPAS 2016 course.  This program prints the parameters based off the input energy and field strength.')
    parser.add_argument('energy', type=float, help='The energy of the beam in GeV.')
    parser.add_argument('B', type=float, help='The magnetic field of the quadrupole for the turns in Tesla.')
    parser.add_argument('-l', '--length_quad', dest="L_quad", type=float, help='The length of the quadrupole lens for the doublet in m.  Default is 0.10 m.', default = 0.1)
    parser.add_argument('--quad_gradient_1', dest="G1", type=float, help='The gradient of the first quadrupole lens for the doublet in T/m.  Default is 50 T/m.', default = 50.)
    parser.add_argument('--quad_gradient_2', dest="G2", type=float, help='The gradient of the second quadrupole lens for the doublet in T/m.  Default is 100 T/m.', default = 100.)
    #parser.add_argument('--quad_d', dest="quad_d", type=float, help='The drift within the quadrupole doublet in m.  Default is 0.5 m.', default = 0.5)
    #parser.add_argument('--doublet_focus', dest="doublet_focus", type=float, help='The focal distance for the doublet in m.  Default is 1 m.', default = 1.0)
    args = parser.parse_args()

    #Get the physical constants
    c = constants.physical_constants["speed of light in vacuum"][0] #m/sec by default
    e = constants.physical_constants["elementary charge"][0] #m/sec by default
    m_e_c2 = constants.physical_constants["electron mass energy equivalent in MeV"][0]*10**-3 #in GeV
    r_e = constants.physical_constants["classical electron radius"][0]#in m
    h_bar = constants.physical_constants["Planck constant over 2 pi in eV s"][0] #in eV s

    #Get some useful quanitites
    kinetic_energy = (args.energy - m_e_c2)*10**9 #in eV
    momentum = np.sqrt(args.energy**2 - m_e_c2**2)*10**9/c #in eV/c
    gamma = kinetic_energy/(m_e_c2*10**9) + 1

    #Store parameters
    parameters = ParameterContainer()
    parameters.addParameter("energy",args.energy,"GeV")
    parameters.addParameter("quadrupole B",args.B,"T")
    parameters.addParameter("rho",momentum/args.B,"m")
    parameters.addParameter("L_bend",np.pi/2.*parameters.getParameter("rho").value(),"m")
    parameters.addParameter("U0",4.*np.pi/3.*r_e*gamma**4/parameters.getParameter("rho").value()*m_e_c2*10**6,"keV")
    parameters.addParameter("E_photon",h_bar*3./2.*c*gamma**3/parameters.getParameter("rho").value()/1000,"keV")
    parameters.addParameter("Quad length",args.L_quad,"m")
    parameters.addParameter("Quad gradient 1",args.G1,"T/m")
    parameters.addParameter("Quad gradient 2",args.G2,"T/m")
    parameters.addParameter("K1",args.G1/momentum,"1/m^2")
    parameters.addParameter("K2",args.G2/momentum,"1/m^2")
    parameters.addParameter("f1",momentum/(args.G1*args.L_quad),"m")
    parameters.addParameter("f2",momentum/(args.G2*args.L_quad),"m")
    parameters.addParameter("Post quad drift",np.sqrt(parameters.getParameter("f2").value()**2*parameters.getParameter("f1").value()/(parameters.getParameter("f1").value()-parameters.getParameter("f2").value())),"m")
    parameters.addParameter("Quad spacing",parameters.getParameter("f2").value()*parameters.getParameter("f1").value()/parameters.getParameter("Post quad drift").value(),"m")
    parameters.addParameter("Doublet focus",parameters.getParameter("Post quad drift").value()+parameters.getParameter("Quad spacing").value(),"m")
    
    
    
    print str(parameters)
