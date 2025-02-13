# exposekit

`exposekit` A library to expose your localhost server to a more wider network. You can utilize this library to host your loopback server to LAN, or even the internet.

## Installation

```bash
pip3 install exposekit
```

# To customize this build before installing,
```bash
apt install git && git clone https://github.com/pulse-empire/exposekit && cd exposekit && pip3 install -e .
```

# How to use
** A simple proxy server that binds client to server socket and forwards all incoming and outgoing requests to your localhost **
```python
import exposekik.proxy as eproxy
if __name__="__main__":
  proxy_server = eproxy.setup(proxy_interface="0.0.0.0", proxy_port=8080, loopback_address='127.0.0.1', loopback_port=5000)
```

** A simple approach that channels your localhost to send and receive requests via a tunnel service **
```python
import exposekit
```