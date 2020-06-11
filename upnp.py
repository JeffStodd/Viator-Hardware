import socket
import errno
import contextlib
import miniupnpc
import fileinput
import subprocess

def openPort(port):
        upnp = miniupnpc.UPnP()

        upnp.discoverdelay = 10
        upnp.discover()

        upnp.selectigd()

        # addportmapping(external-port, protocol, internal-host, internal-port, description, remote-host)
        upnp.addportmapping(port, 'TCP', upnp.lanaddr, port, 'testing', '')

def get_open_port(lowest_port = 0, highest_port = None, bind_address = '', *socket_args, **socket_kwargs):
        reserved_ports = set()
        if highest_port is None:
                highest_port = lowest_port + 100
        while lowest_port < highest_port:
                if lowest_port not in reserved_ports:
                        try:
                                with contextlib.closing(socket.socket(*socket_args, **socket_kwargs)) as my_socket:
                                        my_socket.bind((bind_address, lowest_port))
                                        this_port = my_socket.getsockname()[1]
                                        reserved_ports.add(this_port)
                                        return this_port
                        except socket.error as error:
                                if not error.errno == errno.EADDRINUSE:
                                        raise
                                assert not lowest_port == 0
                                reserved_ports.add(lowest_port)
                lowest_port += 1
        raise Exception('Could not find open port')

def changeConfig(port):
        subprocess.call(['sudo', 'python3', 'editConfig.py', str(port)])

def main():
        port = get_open_port(lowest_port = 8081, highest_port = 8999)
        print("Opening Port", port)
        openPort(port)
        changeConfig(port)

if __name__ == "__main__":
        main()
