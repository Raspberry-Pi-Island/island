from rpi_router.router_cmd import *
from rpi_router.router_data import *

from sys import exit
from pathlib import Path
import argparse


def get_cl_parameters() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("link_t", help="external link type")
    parser.add_argument("external_addr", help="external ip address")
    parser.add_argument("external_network_bytes", help="netmask bytes")
    parser.add_argument("gateway_addr", help="raspberry as a gateway address")
    parser.add_argument("gateway_network_bytes", help="netmask bytes")

    args = parser.parse_args()

    return args


def print_cl_parameters(params: argparse.Namespace):
    print("-" * 50)
    print(f"EXTERNAL LINK TYPE: {params.link_t}")
    print(f"EXTERNAL IP ADDRESS: {params.external_addr}")
    print(f"EXTERNAL NETMASK BYTES: {params.external_network_bytes}")
    print(f"RASPBERRY AS A GATEWAY ADDRESS: {params.gateway_addr}")
    print(f"GATEWAY NETMASK BYTES: {params.gateway_network_bytes}")
    print("-" * 50)


def init_address(addr_network_bytes: int, address_as_str: str):
    print("\nSETTING ADDRESS:")

    parsed_address = address_as_str.split(".")

    if len(parsed_address) >= 4:
        address = RTIpv4Address(
            addr_network_bytes,
            parsed_address[0],
            parsed_address[1],
            parsed_address[2],
            parsed_address[3],
        )

        print(address.address)
        return address
    else:
        return None


def set_network(
    client_link_t: str,
    gateway_link_t: str,
    external_addr: RTIpv4Address,
    gateway_addr: RTIpv4Address,
) -> bool:
    print("\nSETTING NETWORK INTERFACES:")

    if external_addr != None and gateway_addr != None:
        conf_directory = RTPath(Path("/", "etc", "network", "interfaces.d"))

        conf_directory.append(RTNetFile(external_addr, client_link_t, True))
        conf_directory.append(RTNetFile(gateway_addr, gateway_link_t, False))

        conf_directory.go()

        conf_directory.get_file(client_link_t).set_address()
        print(conf_directory.get_current_dir())

        conf_directory.get_file(gateway_link_t).set_address()
        print(conf_directory.get_current_dir())

        conf_directory.goback()

        return True
    else:
        return False


def disable_dhcp_client() -> bool:
    print("DISABLING DHCP CLIENT:")

    dhcp_client = RTDhcpClient()
    return dhcp_client.disable()


def set_dhcp_server(
    gateway_addr: RTIpv4Address,
    gateway_link_t: str,
) -> bool:
    print("\nSETTING DHCP SERVER:")

    if gateway_addr != None:
        dhcp_server = RTDhcpServer(gateway_addr, gateway_link_t)
        return (
            dhcp_server.install() and dhcp_server.configure() and dhcp_server.enable()
        )

    else:
        return False


def set_firewall() -> bool:
    print("\nSETTING FIREWALL:")
    firewall = RTFireWall()

    return (
        firewall.install()
        and firewall.allow_dhcp_traffic()
        and firewall.enable_package_forwarding()
    )


def main(params: argparse.Namespace) -> int:
    gateway_link_t = ""

    external_addr = init_address(params.external_network_bytes, params.external_addr)
    gateway_addr = init_address(params.gateway_network_bytes, params.gateway_addr)

    if params.link_t.startswith("wlan"):
        interface_number: str = params.link_t.split("wlan")[1]
        gateway_link_t = f"eth{interface_number}"
    elif params.link_t.startswith("eth"):
        interface_number: str = params.link_t.split("eth")[1]
        gateway_link_t = f"wlan{interface_number}"

    net_is_configured: bool = set_network(
        params.link_t,
        gateway_link_t,
        external_addr,
        gateway_addr,
    )

    if (
        net_is_configured
        and disable_dhcp_client()
        and set_dhcp_server(gateway_addr, gateway_link_t)
        and set_firewall()
    ):
        return 0

    return -1


if __name__ == "__main__":
    params = get_cl_parameters()
    print_cl_parameters(params)

    try:
        params.external_network_bytes = int(params.external_network_bytes)
        params.gateway_network_bytes = int(params.gateway_network_bytes)
    except ValueError:
        raise ValueError

    exit(main(params))
