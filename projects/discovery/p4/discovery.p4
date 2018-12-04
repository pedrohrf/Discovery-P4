#include "includes/headers.p4"
#include "includes/parser.p4"

register discovery_register {
    width: 100;
    instance_count: 10000;
}

action set_output_mcg(mcast_group) {
    modify_field(intrinsic_metadata.mcast_grp, mcast_group);
}

action do_nat(dmac, sip) {
      modify_field(ethernet.dstAddr,dmac);
      modify_field(ipv4.srcAddr,sip);
}

action _drop() {
    drop();
}

action discovery(pos) {
    register_write(discovery_register,pos,1);
}

table set_mcg {
    reads {
        ipv4.srcAddr: exact;
        ipv4.dstAddr: exact;
    }
    actions {
        set_output_mcg;
	    _drop;
    }
}

table nat_table {
    reads {
        intrinsic_metadata.egress_rid : exact;
    	ipv4.srcAddr: exact;
    }
    actions {
        do_nat;
        _drop;
    }
}

table discovery {
    reads {
        ipv4.srcAddr: exact;
        ipv4.dstAddr : exact;
    }
    actions {
        discovery;
    }
}

control ingress {
    apply(discovery);
    apply(set_mcg);
}

control egress {
    apply(nat_table);
}