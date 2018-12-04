#include "includes/headers.p4"
#include "includes/parser.p4"

register discovery_register {
    width: 1000;
    instance_count: 1000000;
}

action set_destination(dmac, port) {
    modify_field(ethernet.dstAddr, dmac);
    modify_field(standard_metadata.egress_spec, port);
}

action discovery(pos) {
    register_write(discovery_register,pos,1);
}

table discovery {
    reads {
        ipv4.srcAddr : exact;
    }
    actions {
        discovery;
    }
}

table forward {
    reads {
        ipv4.dstAddr : exact;
    }
    actions {
        set_destination;
    }
}

control ingress {
    apply(forward);
    apply(discovery);
}

control egress {

}

