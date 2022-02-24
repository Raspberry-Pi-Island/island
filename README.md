# Raspberry Pi: Network Island

## About
--------------

`Raspberry Pi: Network Island` is a script that bridges your device's network interface
and the network switch you're connecting to.

Whether `ethernet` or `wireless` connection is available, but your device doesn't match
the switch interface, `Raspberry Pi: Network Island` allows you to be online either way!

Using native Raspberry Pi network and relying on automation, `Raspberry Pi: Network Island` builds different subnetworks,
also allowing different types of interfaces.

## Usage:
--------------

``` bash
sudo python3 rpi_island.py --help
```

- `client_link_t`: external server connection with Raspberry Pi
- `client_addr`: Raspberry Pi's external IP address
- `client_addr_network_bytes`: number of bytes to represent Raspberry Pi's external network
>
- `gateway_link_t`: internal Raspberry Pi's clients connection
- `gateway_addr`: internal gateway IP address (that is, Raspberry Pi's address as a gateway)
- `gateway_addr_network_bytes`: number of bytes to represent Raspberry Pi's network as a gateway

> You may need to reboot for configurations to be set...
