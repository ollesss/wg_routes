import ipaddress

def parse_allowed_ips(config_text: str):
    lines = config_text.splitlines()
    allowed_ips = []
    for line in lines:
        if line.strip().startswith("AllowedIPs"):
            parts = line.split("=")[-1].strip().split(",")
            allowed_ips.extend([ip.strip() for ip in parts])
    return allowed_ips

def cidr_to_mask(cidr: str):
    net = ipaddress.ip_network(cidr, strict=False)
    return str(net.network_address), str(net.netmask)

def generate_bat_file(ips: list[str], gateway: str = "0.0.0.0"):
    lines = []
    for cidr in ips:
        ip, mask = cidr_to_mask(cidr)
        lines.append(f"ROUTE ADD {ip} MASK {mask} {gateway}")
    return "\n".join(lines)
