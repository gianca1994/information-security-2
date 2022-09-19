import getopt
import socket
import sys
import threading

from protocol import protocol


def option_reading():
    (opt, arg) = getopt.getopt(sys.argv[1:], 'p:', ['port='])

    if len(opt) != 1:
        print(
            "Error: Se espera 1 opcion [-p] or [--port] ", len(opt), " recibidas")
        sys.exit(0)

    for (op, arg) in opt:
        if op in ['-p', '--port']:
            port = int(arg)
        else:
            print('Opcion invalida')
            sys.exit(0)

    assert port is not None
    return port


def main():
    port = option_reading()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    print("*************** SERVER ONLINE! ***************")

    while True:
        server_socket.listen()

        client_socket, client_address = server_socket.accept()
        print(f'\nCLIENTE: {client_address}, CONECTADO CORRECTAMENTE!')

        multithreading = threading.Thread(target=protocol, args=(client_socket, client_address))
        multithreading.start()


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
