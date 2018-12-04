header_type intrinsic_metadata_t {
    fields {
        mcast_grp : 16;
        lf_field_list : 32;
        egress_rid : 16;
        ingress_global_timestamp : 32;
    }
}

metadata intrinsic_metadata_t intrinsic_metadata;

header_type ethernet_t {
    fields {
        dstAddr : 48;
        srcAddr : 48;
        etherType : 16;
    }
}

header_type ipv4_t {
    fields {
        version : 4;
        ihl : 4;
        diffserv : 8;
        totalLen : 16;
        identification : 16;
        flags : 3;
        fragOffset : 13;
        ttl : 8;
        protocol : 8;
        hdrChecksum : 16;
        srcAddr : 32;
        dstAddr: 32;
    }
}

header_type icmp_t {
    fields {
        type_ : 8;
        code : 8;
        hdrChecksum : 16;

    }
}

header ethernet_t ethernet;
header ipv4_t ipv4;
header icmp_t icmp;