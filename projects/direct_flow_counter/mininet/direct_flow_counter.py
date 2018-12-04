import os
import sys
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../../core/mininet")

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from p4_mininet import P4Switch, P4Host
from time import sleep

NUM_HOSTS = 4

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
            self.addSwitch('s1', sw_path = sw_path, json_path = 'build/direct_flow_counter.json', thrift_port = 9090, pcap_dump = pcap_dump, enable_debugger = debug),
            self.addSwitch('s2', sw_path = sw_path, json_path = 'build/direct_flow_counter.json', thrift_port = 9091, pcap_dump = pcap_dump, enable_debugger = debug),
            self.addSwitch('s3', sw_path = sw_path, json_path = 'build/direct_flow_counter.json', thrift_port = 9092, pcap_dump = pcap_dump, enable_debugger = debug),
            self.addSwitch('s4', sw_path = sw_path, json_path = 'build/direct_flow_counter.json', thrift_port = 9093, pcap_dump = pcap_dump, enable_debugger = debug)
        ))

    def add_hosts(self, number):
        for i in xrange(number):
            host = self.addHost('h%d' % (i + 1), ip = '10.0.%d.10/24' % i, mac = '00:04:00:00:00:%02x' %i)
            self.networkHosts.append(host)

    def build_network_topo(self):
        self.addLink(self.networkHosts[0], self.networkSwitches[0])
        print('h1 <-> s1:')
        print(self.port(self.networkHosts[0], self.networkSwitches[0]))

        self.addLink(self.networkHosts[1], self.networkSwitches[1])
        print('h2 <-> s2:')
        print(self.port(self.networkHosts[1], self.networkSwitches[1]))

        self.addLink(self.networkSwitches[0], self.networkSwitches[1])
        print('s1 <-> s2:')
        print(self.port(self.networkSwitches[0], self.networkSwitches[1]))

        self.addLink(self.networkSwitches[0], self.networkSwitches[2])
        print('s1 <-> s3:')
        print(self.port(self.networkSwitches[0], self.networkSwitches[2]))

        self.addLink(self.networkSwitches[1], self.networkSwitches[3])
        print('s2 <-> s4:')
        print(self.port(self.networkSwitches[1], self.networkSwitches[3]))

        self.addLink(self.networkSwitches[2], self.networkSwitches[3])
        print('s3 <-> s4:')
        print(self.port(self.networkSwitches[2], self.networkSwitches[3]))

        self.addLink(self.networkSwitches[2], self.networkHosts[2])
        print('s3 <-> h3:')
        print(self.port(self.networkSwitches[2], self.networkHosts[2]))

        self.addLink(self.networkSwitches[3], self.networkHosts[3])
        print('s4 <-> h4:')
        print(self.port(self.networkSwitches[3], self.networkHosts[3]))

def get_args():
    parser = argparse.ArgumentParser(description='Mininet demo')
    parser.add_argument('--behavioral-exe', help='Path to behavioral model executable', type=str, action="store", required=True)
    parser.add_argument('--thrift-port', help='Thrift server port for table updates', type=int, action="store", default=9090)
    parser.add_argument('--mode', choices=['l2', 'l3'], type=str, default='l3')
    parser.add_argument('--json', help='Path to JSON config file', type=str, action="store", required=True)
    parser.add_argument('--pcap-dump', help='Dump packets on interfaces to pcap files', type=str, action="store", required=False, default=False)
    parser.add_argument('--debugger', help='Enable debugger', type=lambda x: bool(x == "True"), action="store", required=False, default=False)
    return parser.parse_args()

def set_node_route(node, ip_addr, mac_addr, route_str):
    node.setARP(ip_addr, mac_addr)
    node.setDefaultRoute(route_str)

def initialize_routes(network):
    set_node_route(network.get('h1'), '10.0.0.1', '00:04:00:00:00:00', 'dev eth0 via 10.0.0.1')
    set_node_route(network.get('h2'), '10.0.1.1', '00:04:00:00:00:01', 'dev eth0 via 10.0.1.1')
    set_node_route(network.get('h3'), '10.0.2.1', '00:04:00:00:00:02', 'dev eth0 via 10.0.2.1')
    set_node_route(network.get('h4'), '10.0.3.1', '00:04:00:00:00:03', 'dev eth0 via 10.0.3.1')

def describe_hosts(network):
    for i in xrange(NUM_HOSTS):
        host = network.get('h%d' % (i + 1))
        host.describe()

def run_network(network):
    sleep(1)
    print "Ready !"
    CLI(network)
    network.stop()

def main():
    args = get_args()
    mode = args.mode
    topo = DiscoverySwitch(args.behavioral_exe, args.json, args.thrift_port, args.pcap_dump, args.debugger)
    net = Mininet(topo = topo, host = P4Host, switch = P4Switch, controller = None)
    net.start()

    initialize_routes(net)
    describe_hosts(net)
    run_network(net)

if __name__ == '__main__':
    setLogLevel('info')
    main()
#
# import os
# import sys
#
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../../core/mininet")
#
# from mininet.net import Mininet
# from mininet.topo import Topo
# from mininet.log import setLogLevel, info
# from mininet.cli import CLI
# from mininet.net import Intf
# from p4_mininet import P4Switch, P4Host
# from time import sleep
# import argparse
#
# class SingleSwitchTopo(Topo):
#     ""
#     def __init__(self, sw_path, json_path, thrift_port, pcap_dump, n, debug, **opts):
#         ""
#         Topo.__init__(self, **opts)
#         switch = self.addSwitch('s1', sw_path = sw_path, json_path = json_path, thrift_port = thrift_port, pcap_dump = pcap_dump, enable_debugger = debug)
#         for h in xrange(n):
#             host = self.addHost('h%d' % (h + 1), ip = "10.0.%d.10/24" % h, mac = '00:04:00:00:00:%02x' %h)
#             self.addLink(host, switch)
#
# def get_args():
#     ""
#     parser = argparse.ArgumentParser(description='Mininet demo')
#     parser.add_argument('--behavioral-exe', help='Path to behavioral executable', type=str, action="store", required=True)
#     parser.add_argument('--thrift-port', help='Thrift server port for table updates', type=int, action="store", default=9090)
#     parser.add_argument('--num-hosts', help='Number of hosts to connect to switch', type=int, action="store", default=2)
#     parser.add_argument('--mode', choices=['l2', 'l3'], type=str, default='l3')
#     parser.add_argument('--json', help='Path to JSON config file', type=str, action="store", required=True)
#     parser.add_argument('--pcap-dump', help='Dump packets on interfaces to pcap files', type=str, action="store", required=False, default=False)
#     parser.add_argument('--debugger', help='Enable debugger', type=lambda x:bool(x == "True"), action="store", required=False, default=False)
#
#     return parser.parse_args()
#
#
# def main():
#
#     args = get_args()
#     num_hosts = args.num_hosts
#     mode = args.mode
#     debug = args.debugger
#
#     topo = SingleSwitchTopo(args.behavioral_exe, args.json, args.thrift_port, args.pcap_dump, num_hosts, debug)
#     net = Mininet(topo = topo, host = P4Host, switch = P4Switch, controller = None)
#     net.start()
#     Intf('enp0s3',node = net.get('s1'))
#     sw_mac = ["00:aa:bb:00:00:%02x" % n for n in xrange(num_hosts)]
#     sw_addr = ["10.0.%d.1" % n for n in xrange(num_hosts)]
#
#     for n in xrange(num_hosts):
#         h = net.get('h%d' % (n + 1))
#         if mode == "l2":
#             h.setDefaultRoute("dev eth0")
#         else:
#             h.setARP(sw_addr[n], sw_mac[n])
#             h.setDefaultRoute("dev eth0 via %s" % sw_addr[n])
#
#     for n in xrange(num_hosts):
#         h = net.get('h%d' % (n + 1))
#         h.describe()
#
#     sleep(1)
#     print "Ready !"
#     CLI( net )
#     net.stop()
#
# if __name__ == '__main__':
#
#     setLogLevel( 'info' )
#     main()
