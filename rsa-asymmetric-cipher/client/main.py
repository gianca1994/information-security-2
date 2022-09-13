import getopt
import socket
import sys

from protocol import protocol


def option_reading():
    (opt, arg) = getopt.getopt(sys.argv[1:], 'h:p:', [
        'host=', 'port='])

    if len(opt) != 2:
        print(f"Error: Se esperan 2 opciones: [-h] o [--host] y [-p] o [--port] y has ingresado {len(opt)} opciones.")
        sys.exit(0)

    for (op, arg) in opt:
        if op in ['-h', '--host']:
            host = str(arg)
        elif op in ['-p', '--port']:
            port = int(arg)
        else:
            print('Opciones invalidas')

    assert (host, port) is not None
    return host, port


def main():
    server_host, server_port = option_reading()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    protocol(client_socket)


if __name__ == '__main__':
    try:
        main()
    except getopt.GetoptError as error:
        print(error)
    except ConnectionRefusedError:
        print('Error: Connection refused')
    except socket.error:
        print('Failed to create a socket')
    except Exception as error:
        print(error)
