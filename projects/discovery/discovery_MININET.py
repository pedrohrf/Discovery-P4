import os
import sys
import argparse
#h5 route add -net 10.0.1.0/24 h5-eth1
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../core/mininet")

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from p4_mininet import P4Switch, P4Host
from time import sleep

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../core/tools/")
import defaults
import helpers

NUM_HOSTS = 5

class DiscoverySwitch(Topo):

    def __init__(self, sw_path, json_path, thrift_port, pcap_dump, debug, **opts):
        Topo.__init__(self, **opts)
        self.initialize_variables()
        self.add_switches(sw_path, json_path, thrift_port, pcap_dump, debug, **opts)
        self.add_hosts(self.hostsCount)
        self.build_network_topo()

    def initialize_variables(self):
        self.networkSwitches = []
        self.networkHosts = []
        self.hostsCount = NUM_HOSTS

    def add_switches(self, sw_path, json_path, thrift_port, pcap_dump, debug, **opts):
        self.networkSwitches.extend((
            self.addSwitch('s0', sw_path = sw_path, json_path = 'build/discovery.json', thrift_port = 9090, pcap_dump = pcap_dump, enable_debugger = debug),
            self.addSwitch('s1', sw_path = sw_path, json_path = 'build/discovery.json', thrift_port = 9091, pcap_dump = pcap_dump, enable_debugger = debug),
            self.addSwitch('s2', sw_path = sw_path, json_path = 'build/discovery.json', thrift_port = 9092, pcap_dump = pcap_dump, enable_debugger = debug),
            self.addSwitch('s3', sw_path = sw_path, json_path = 'build/discovery.json', thrift_port = 9093, pcap_dump = pcap_dump, enable_debugger = debug),
            self.addSwitch('s4', sw_path = sw_path, json_path = 'build/discovery.json', thrift_port = 9094, pcap_dump = pcap_dump, enable_debugger = debug)
        ))

    def add_hosts(self, number):
        for i in xrange(number):
            host = self.addHost('h%d' % (i), ip = '10.0.%d.10/24' % i, mac = '00:04:00:00:00:%02x' %i)
            self.networkHosts.append(host)

    def build_network_topo(self):
        self.addLink(self.networkHosts[1], self.networkSwitches[1])
        print('h1 <-> s1:')
        print(self.port(self.networkHosts[1], self.networkSwitches[1]))

        self.addLink(self.networkSwitches[2], self.networkHosts[2])
        print('h2 <-> s2:')
        print(self.port(self.networkSwitches[2], self.networkHosts[2]))

        self.addLink(self.networkSwitches[3], self.networkHosts[3])
        print('h3 <-> s3:')
        print(self.port(self.networkSwitches[3], self.networkHosts[3]))

        self.addLink(self.networkSwitches[4], self.networkHosts[4])
        print('h4 <-> s4')
        print(self.port(self.networkSwitches[4], self.networkHosts[4]))

        self.addLink(self.networkSwitches[1], self.networkSwitches[0])
        print('s1 <-> s0:')
        print(self.port(self.networkSwitches[1], self.networkSwitches[0]))

        self.addLink(self.networkSwitches[2], self.networkSwitches[0])
        print('s2 <-> s0:')
        print(self.port(self.networkSwitches[2], self.networkSwitches[0]))

        self.addLink(self.networkSwitches[3], self.networkSwitches[0])
        print('s3 <-> s0:')
        print(self.port(self.networkSwitches[3], self.networkSwitches[0]))

        self.addLink(self.networkSwitches[4], self.networkSwitches[0])
        print('s4 <-> s0:')
        print(self.port(self.networkSwitches[4], self.networkSwitches[0]))

        self.addLink(self.networkSwitches[1], self.networkSwitches[2])
        print('s1 <-> s2:')
        print(self.port(self.networkSwitches[1], self.networkSwitches[2]))

        self.addLink(self.networkSwitches[1], self.networkSwitches[3])
        print('s1 <-> s3:')
        print(self.port(self.networkSwitches[1], self.networkSwitches[3]))

        self.addLink(self.networkSwitches[2], self.networkSwitches[4])
        print('s2 <-> s4:')
        print(self.port(self.networkSwitches[2], self.networkSwitches[4]))

        self.addLink(self.networkSwitches[3], self.networkSwitches[4])
        print('s3 <-> s4:')
        print(self.port(self.networkSwitches[3], self.networkSwitches[4]))

        self.addLink(self.networkHosts[0], self.networkSwitches[0])
        print('h0 <-> s0:')
        print(self.port(self.networkHosts[0], self.networkSwitches[0]))


def set_node_route(node, ip_addr, mac_addr, route_str):
    node.setARP(ip_addr, mac_addr)
    node.setDefaultRoute(route_str)

def initialize_routes(network):
    set_node_route(network.get('h0'), '10.0.0.1', '00:04:00:00:00:00', 'dev eth0 via 10.0.0.1')
    set_node_route(network.get('h1'), '10.0.1.1', '00:04:00:00:00:01', 'dev eth0 via 10.0.1.1')
    set_node_route(network.get('h2'), '10.0.2.1', '00:04:00:00:00:02', 'dev eth0 via 10.0.2.1')
    set_node_route(network.get('h3'), '10.0.3.1', '00:04:00:00:00:03', 'dev eth0 via 10.0.3.1')
    set_node_route(network.get('h4'), '10.0.4.1', '00:04:00:00:00:04', 'dev eth0 via 10.0.4.1')

def describe_hosts(network):
    for i in xrange(NUM_HOSTS):
        host = network.get('h%d' % (i))
        host.describe()

def start():
    topo = DiscoverySwitch(defaults.BMV2_INTERPRETER_PATH, defaults.PROJECT_BUILD_NAME + "discovery.json", 9090, False, True)
    net = Mininet(topo = topo, host = P4Host, switch = P4Switch, controller = None)
    net.start()

    initialize_routes(net)
    return net
