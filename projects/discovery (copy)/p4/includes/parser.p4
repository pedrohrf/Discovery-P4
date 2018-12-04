#define ETHERTYPE_IPV4 0x0800
#define IP_PROTOCOLS_ICMP 1
#define IP_PROTOCOLS_ICMP_PAYLOAD 8

parser start {
    return parse_ethernet;
}

parser parse_ethernet {
    extract(ethernet);
    return select(latest.etherType) {
        ETHERTYPE_IPV4 : parse_ipv4;
        default: ingress;
    }
}

parser parse_ipv4 {
    extract(ipv4);
    return select(latest.protocol) {
        IP_PROTOCOLS_ICMP : parse_icmp;
        default: ingress;
    }
}

parser parse_icmp {
    extract(icmp);
    return select(latest.type_) {
        IP_PROTOCOLS_ICMP_PAYLOAD : parse_icmp_payload;
        default: ingress;
    }
}

parser parse_icmp_payload {
    extract(icmp_payload);
    return ingress;
}

