#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hydraulic simulation of a network object using Epanet Toolkit version 2.2.
Uses the epanet-module wrapper for Epanet library from OpenWaterAnalytics.

@author: Eduardo Jiménez Hernández
@email: eduardojh@email.arizona.edu
"""
import os
import sys
import os.path
sys.path.append('../')
import lib.epamodule as em
EXT_INPUT = 'inp'
EXT_REPORT = 'rpt'

class Network:

    def __init__(self, basepath, filename):
        """ Initialize the network object

        :param basepath, working directory (should end with '/')
        :param filename, input file name (with .inp extension)
        """
        self.path = basepath
        self.inputfile = filename
        self.outputfile = filename[-4:] + '.' + EXT_REPORT
        self.name = None
        self.links = None
        self.nodes = None
        self.reserviors = None
        self.coordinates = None
        self.x_coordinates = None
        self.y_coordinates = None
        self.node_values = {}
        self.link_values = {}
        self.nodeids = []
        self.sources = []
        self.pressure = []
        self.velocity = []
        self.lengths = []
        self.diameters = []
        self.flowrate = []

    def check_file(self):
        """ Check file

        Checks if the input file exist
        """
        exist = os.path.isfile(self.path + self.inputfile)
        return exist

    def open_network(self):
        """ Open network

        Open the EPANET toolkit & hydraulics solver
        """
        fi = self.path + self.inputfile
        fo = self.path + self.outputfile

        if self.check_file():
            em.ENopen(fi, fo)
            em.ENopenH()
        else:
            print('File: {0} does not exist'.format(fi))

        return True

    def close_network(self):
        """ Close network

        Close hydraulics solver & EPANET toolkit
        """
        em.ENcloseH()
        em.ENclose()

    def initialize(self):
        """ Get info

        Retrieve the information of the network from EPANET
        """
        self.nodes = em.ENgetcount(em.EN_NODECOUNT)
        self.links = em.ENgetcount(em.EN_LINKCOUNT)

    def change_diameters(self, diameters):
        """ Change diameters

        Change the original diameters of the network by the specified ones
        """
        # Check that the number of diameters is equal to the number of pipes
#        print("Diam: {0}".format(len(diameters)))
#        print("Pipes:{0}".format(self.links))
        assert len(diameters) is self.links, \
            "The number of diameters and pipes don't match"

        for i in range(self.links):
            # print("Setting diameter: {0}".format(diameters[i]))
            em.ENsetlinkvalue(i+1, em.EN_DIAMETER, diameters[i])

    def simulate(self):
        """ Simulate

        Runs a hydraulic simulation of the network with EPANET
        
        Node parameter codes consist of the following constants:
        EN_ELEVATION     = 0      # /* Node parameters */
        EN_BASEDEMAND    = 1
        EN_PATTERN       = 2
        EN_EMITTER       = 3
        EN_INITQUAL      = 4
        EN_SOURCEQUAL    = 5
        EN_SOURCEPAT     = 6
        EN_SOURCETYPE    = 7
        EN_TANKLEVEL     = 8
        EN_DEMAND        = 9
        EN_HEAD          = 10
        EN_PRESSURE      = 11
        EN_QUALITY       = 12
        EN_SOURCEMASS    = 13
        EN_INITVOLUME    = 14
        EN_MIXMODEL      = 15
        EN_MIXZONEVOL    = 16
        
        EN_TANKDIAM      = 17
        EN_MINVOLUME     = 18
        EN_VOLCURVE      = 19
        EN_MINLEVEL      = 20
        EN_MAXLEVEL      = 21
        EN_MIXFRACTION   = 22
        EN_TANK_KBULK    = 23
                
        EN_DIAMETER      = 0      # /* Link parameters */
        EN_LENGTH        = 1
        EN_ROUGHNESS     = 2
        EN_MINORLOSS     = 3
        EN_INITSTATUS    = 4
        EN_INITSETTING   = 5
        EN_KBULK         = 6
        EN_KWALL         = 7
        EN_FLOW          = 8
        EN_VELOCITY      = 9
        EN_HEADLOSS      = 10
        EN_STATUS        = 11
        EN_SETTING       = 12
        EN_ENERGY        = 13

        """
        # Initialize the hydraulic solver
        em.ENinitH(em.EN_NOSAVE)
        self.pressure = []
        self.velocity = []
        self.lengths = []
        self.diameters = []
        self.sources = []

        # Hydraulic simulation
        while True:
            em.ENrunH()

            # Retrieve hydraulic results for time t
            for i in range(self.nodes):
                # Get the pressure, nodes start at 1
                node = i+1
                nid = em.ENgetnodeid(node)
                p = em.ENgetnodevalue(node, em.EN_PRESSURE)
                t = em.ENgetnodetype(node)
                self.nodeids.append(nid)
                self.pressure.append(p)
                self.sources.append(t)
                
                # Get the type of current node
                nodetype = em.ENgetnodetype(node)
                # if nodetype == em.EN_JUNCTION:
                #     print("Node type: Junction")
                # elif nodetype == em.EN_RESERVOIR:
                #     print("Node type: Reservoir")
                # elif nodetype == em.EN_TANK:
                #     print("Node type: Tank")
                
                # Get all the possible values of a node
                values = {}
                values['ELEVATION'] = em.ENgetnodevalue(node, em.EN_ELEVATION)
                values['BASEDEMAND'] = em.ENgetnodevalue(node, em.EN_BASEDEMAND)
                values['PATTERN'] = em.ENgetnodevalue(node, em.EN_PATTERN)
#                values['EMITTER'] = em.ENgetnodevalue(node, em.EN_EMITTER)
#                values['INITQUAL'] = em.ENgetnodevalue(node, em.EN_INITQUAL)
#                values['SOURCEQUAL'] = em.ENgetnodevalue(node, em.EN_SOURCEQUAL)
#                values['SOURCEPAT'] = em.ENgetnodevalue(node, em.EN_SOURCEPAT)
#                values['SOURCETYPE'] = em.ENgetnodevalue(node, em.EN_SOURCETYPE)
#                values['TANKLEVEL'] = em.ENgetnodevalue(node, em.EN_TANKLEVEL)
                values['DEMAND'] = em.ENgetnodevalue(node, em.EN_DEMAND)
                values['HEAD'] = em.ENgetnodevalue(node, em.EN_HEAD)
                values['PRESSURE'] = em.ENgetnodevalue(node, em.EN_PRESSURE)
                values['QUALITY'] = em.ENgetnodevalue(node, em.EN_QUALITY)
#                values['SOURCEMASS'] = em.ENgetnodevalue(node, em.EN_SOURCEMASS)
#                values['INITVOLUME'] = em.ENgetnodevalue(node, em.EN_INITVOLUME)
#                values['MIXMODEL'] = em.ENgetnodevalue(node, em.EN_MIXMODEL)
#                values['MIXZONEVOL'] = em.ENgetnodevalue(node, em.EN_MIXZONEVOL)
#                values['TANKDIAM'] = em.ENgetnodevalue(node, em.EN_TANKDIAM)
#                values['MINVOLUME'] = em.ENgetnodevalue(node, em.EN_MINVOLUME)
#                values['VOLCURVE'] = em.ENgetnodevalue(node, em.EN_VOLCURVE)
#                values['MINLEVEL'] = em.ENgetnodevalue(node, em.EN_MINLEVEL)
#                values['MAXLEVEL'] = em.ENgetnodevalue(node, em.EN_MAXLEVEL)
#                values['MIXFRACTION'] = em.ENgetnodevalue(node, em.EN_MIXFRACTION)
#                values['TANK_KBULK'] = em.ENgetnodevalue(node, em.EN_TANK_KBULK)
                self.node_values[nid] = values
            for i in range(self.links):
                link = i+1
                linkid = em.ENgetlinkid(link)
                
                # Get the velocity of the flow in the pipe
                v = em.ENgetlinkvalue(link, em.EN_VELOCITY)
                l = em.ENgetlinkvalue(link, em.EN_LENGTH)
                d = em.ENgetlinkvalue(link, em.EN_DIAMETER)
                f = em.ENgetlinkvalue(link, em.EN_FLOW)
                self.velocity.append(v)
                self.lengths.append(l)
                self.diameters.append(d)
                self.flowrate.append(f)
                
                # Get all possible values of a link
                values = {}
                values['DIAMETER'] = em.ENgetlinkvalue(link, em.EN_DIAMETER)
                values['LENGTH'] = em.ENgetlinkvalue(link, em.EN_LENGTH)
                values['ROUGHNESS'] = em.ENgetlinkvalue(link, em.EN_ROUGHNESS)
                values['MINORLOSS'] = em.ENgetlinkvalue(link, em.EN_MINORLOSS)
                values['INITSTATUS'] = em.ENgetlinkvalue(link, em.EN_INITSTATUS)
                values['INITSETTING'] = em.ENgetlinkvalue(link, em.EN_INITSETTING)
                values['KBULK'] = em.ENgetlinkvalue(link, em.EN_KBULK)
                values['KWALL'] = em.ENgetlinkvalue(link, em.EN_KWALL)
                values['FLOW'] = em.ENgetlinkvalue(link, em.EN_FLOW)
                values['VELOCITY'] = em.ENgetlinkvalue(link, em.EN_VELOCITY)
                values['HEADLOSS'] = em.ENgetlinkvalue(link, em.EN_HEADLOSS)
                values['STATUS'] = em.ENgetlinkvalue(link, em.EN_STATUS)
                values['SETTING'] = em.ENgetlinkvalue(link, em.EN_SETTING)
                values['ENERGY'] = em.ENgetlinkvalue(link, em.EN_ENERGY)
                
                self.link_values[linkid] = values
            tstep = em.ENnextH()
            if tstep <= 0:
                break

        return self.pressure, self.velocity, self.lengths, self.sources

    def change_init_nodes(self):
        """ Change initial nodes of each pipe

        Change the original initial nodes of each pipe
        """
        for i in range(1, self.links+1):
            s, e = em.ENgetlinknodes(i)
#            print("Link: {0} ({1}-{2})".format(i, s, e))
        return

    def save_inp_file(self, filename):
        em.ENsaveinpfile(filename)
        return
    
    def show_properties(self):
        nodes = sorted(self.node_values.keys())
        links = sorted(self.link_values.keys())
        
        print("\nNetwork nodes")
        print("Node    Elevation Pressure     Head Base-Dem   Demand  Pattern  Quality ")
        for n in nodes:
            node = self.node_values.get(n)
            print("{:8} {:-8.2f} {:-8.2f} {:-8.2f} {:-8.2f} {:-8.2f} {:-8.2f} {:-8.2f}".format(n.decode("utf-8"), node.get('ELEVATION'), node.get('PRESSURE'), node.get('HEAD'), node.get('BASEDEMAND'), node.get('DEMAND'), node.get('PATTERN'), node.get('QUALITY')))
        
        print("\nNetwork junctions")
        print("Link     Diameter   Length Velocity")
        for j in links:
            link = self.link_values.get(j)
            print("{:8} {:-8.2f} {:-8.2f} {:-8.2f}".format(j.decode("utf-8"), link.get('DIAMETER'), link.get('LENGTH'), link.get('VELOCITY')))

# *** END OF THE CLASSES ***

def simulate_network(path, infile, **kwargs):
    """ Simulate network

    Simulates a network using data from an Epanet's INP file
    :param: str path, the path where the input file is located
    :param: str infile, the name of the input file
    """
    _diameters = kwargs.get('diameters', None)
    network = Network(path, infile)
    network.open_network()
    network.initialize()
    if (_diameters is not None):
        assert len(_diameters) == network.links, "Diameters don't match"
        network.change_diameters(_diameters)
    network.simulate()
    # network.change_init_nodes()  # Prints nodes and links starting by 1
    network.close_network()

    # Print the values from hydraulic simulation
    network.show_properties()
    
    # print('Node\tPressure\tType')
    # for i in range(network.nodes):
    #     print('{0}\t{1:8.2f}\t{2}'.format(i+1, network.pressure[i],
    #           network.sources[i]))
    # print('Pipe\tDiameter\tVelocity\tFlowrate')
    # for i in range(network.links):
    #     print('{0}\t{1:8.2f}\t{2:8.2f}\t{3:8.2f}'.format(i+1,
    #           network.diameters[i],
    #           network.velocity[i],
    #           network.flowrate[i]))
    # print("Source nodes: {0}".format(sum(network.sources)))

if __name__ == "__main__":

    # *** THIS IS SOME TEST CODE ***
    print("Running test...")
    print("CWD: " + os.getcwd())
    
    path = '../data/'
    
    print("Trying to run epamodule from:")
    print(os.getcwd() + path)
    
    infile = 'TwoLoop.inp'
    mynet = Network(path, infile)
    mynet.open_network()
    mynet.initialize()
    mynet.simulate()
    # mynet.change_init_nodes()
    mynet.close_network()
    
    mynet.show_properties()

#    print(mynet.pressure)
#    print(mynet.velocity)
