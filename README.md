# Raspberry Pi: Network Island

## About
--------------

`Raspberry Pi: Network Island` is a script that bridges your device's network interface to a switch or router.

Using automation and relying on linux, `Raspberry Pi: Network Island` sets a subnetwork
out of a static IP address, working as a proxy between your device and the external network.
Converting an interface to another.

Example:

Imagine that your device doesn't have a wireless adapter. You could connect 
to your Raspberry Pi by cable, run this script and be online in a few minutes!

## Usage:
--------------

``` bash
sudo python3 rpi_island.py --help
```

- `link_t`: external server connection with Raspberry Pi
- `external_addr`: Raspberry Pi's external IP address
- `external_network_bytes`: number of bytes to represent Raspberry Pi's external network
>
- `gateway_addr`: internal gateway IP address (that is, Raspberry Pi's address as a gateway)
- `gateway_network_bytes`: number of bytes to represent Raspberry Pi's network as a gateway

> You may need to reboot for configurations to be set...
