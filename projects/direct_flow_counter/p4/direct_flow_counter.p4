#include "includes/headers.p4"
#include "includes/parser.p4"

counter my_direct_counter {
    type: packets;
    direct: forward;    
}

register discovery_register {
    width: 2048;
    instance_count: 1000;
}

action set_destination(dmac, dip, port, pos) {
    modify_field(ethernet.dstAddr, dmac);
    modify_field(ipv4.dstAddr, dip);
    modify_field(standard_metadata.egress_spec, port);
    register_write(discovery_register,pos,1);
}

table forward {
    reads {
        ipv4.dstAddr : exact;
        ipv4.srcAddr : exact;
    }
    actions {
        set_destination;
    }
}

control ingress {
    apply(forward);
}

control egress {

}
