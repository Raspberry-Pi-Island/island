from rpi_router.router_cmd import *
from rpi_router.router_data import *

from sys import exit
from pathlib import Path
import argparse


def get_cl_parameters() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("client_link_t", help="external link type")
    parser.add_argument("client_addr", help="external ip address")
    parser.add_argument("client_addr_network_bytes", help="netmask bytes number")
    parser.add_argument("gateway_link_t", help="internal link type")
    parser.add_argument("gateway_addr", help="internal gateway ip address")
    parser.add_argument("gateway_addr_network_bytes", help="netmask bytes number")

    args = parser.parse_args()

    return args


def print_cl_parameters(params: argparse.Namespace):
    print("-" * 50)
    print(f"CLIENT LINK TYPE: {params.client_link_t}")
    print(f"CLIENT ADDRESS: {params.client_addr}")
    print(f"CLIENT NETMASK BYTES: {params.client_addr_network_bytes}")
    print(f"GATEWAY LINK TYPE: {params.gateway_link_t}")
    print(f"GATEWAY ADDRESS: {params.gateway_addr}")
    print(f"GATEWAY NETMASK BYTES: {params.gateway_addr_network_bytes}")
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
    client_addr: RTIpv4Address,
    gateway_addr: RTIpv4Address,
) -> bool:
    print("\nSETTING NETWORK INTERFACES:")

    if client_addr != None and gateway_addr != None:
        conf_directory = RTPath(Path("/", "etc", "network", "interfaces.d"))

        conf_directory.append(RTNetFile(client_addr, client_link_t, True))
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
    client_addr = init_address(params.client_addr_network_bytes, params.client_addr)
    gateway_addr = init_address(params.gateway_addr_network_bytes, params.gateway_addr)

    net_is_configured: bool = set_network(
        params.client_link_t,
        params.gateway_link_t,
        client_addr,
        gateway_addr,
    )

    if (
        net_is_configured
        and disable_dhcp_client()
        and set_dhcp_server(gateway_addr, params.gateway_link_t)
        and set_firewall()
    ):
        return 0

    return -1


if __name__ == "__main__":
    params = get_cl_parameters()
    print_cl_parameters(params)

    if params.client_link_t == params.gateway_link_t:
        print("link_t cannot be equal!")
        exit(-1)

    try:
        params.client_addr_network_bytes = int(params.client_addr_network_bytes)
        params.gateway_addr_network_bytes = int(params.gateway_addr_network_bytes)
    except ValueError:
        raise ValueError

    exit(main(params))
