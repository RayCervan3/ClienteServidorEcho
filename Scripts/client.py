import socket
import threading
import time

from enums import TypesMessages

contador_mensajes = 0
contador_request = 0
contador_reply = 0
contador_error = 0


def enter_data():
    host = input(str("introduzca la dirección IP a la que se quiere conectar: "))
    port = int(input("introduzca su puerto de conexion: "))
    intentos = int(input("introduzca numero de peticiones: "))
    if is_valid_ip(host):
        conn(host, port, intentos)
    else:
        print("Ip invalida")


def is_valid_ip(ip):
    """Validates IP addresses.
    """
    return is_valid_ipv4(ip) or is_valid_ipv6(ip)


def is_valid_ipv4(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


def is_valid_ipv6(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True


def conn(host, port, intentos):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return cliente.connect((host, port))
    except:
        print("algo va mal")
    finally:
        escritura_mensaje(cliente, intentos)


def escritura_mensaje(cliente, intentos):
    contador = 0
    mensaje = f"{input('>. Ingrese mensaje: ')}"
    is_ok = validacion_bytes(mensaje)
    
    if is_ok:
        while True and contador < intentos:
            trama = construye_trama(TypesMessages.REQUEST, mensaje)
            print(f"> Enviando mensaje {trama}")
            cliente.send(trama.encode('utf-8'))
            mensaje_rcv = cliente.recv(1024).decode('utf-8')
            print(f"> Recibiendo mensaje: {mensaje_rcv}")
            time.sleep(2)
            contador += 1
    else:
        print("El mensaje supera los 40 bytes")

    hilo_escrito = threading.Thread(target=escritura_mensaje, args=(cliente, intentos))
    hilo_escrito.start()


def construye_trama(type, mensaje):
    if type == TypesMessages.REQUEST:
        global contador_request
        contador_request += 1
        if contador_request < 10:
            return "00" + str(contador_request) + " " + mensaje
        else:
            return "0" + str(contador_request) + " " + mensaje
    if type == TypesMessages.REPLY:
        global contador_reply
        if contador_reply < 10:
            return "10" + str(contador_reply) + " " + mensaje
        else:
            return "1" + str(contador_reply) + " " + mensaje
    if type == TypesMessages.ERROR:
        global contador_error
        if contador_error < 10:
            return "20" + str(contador_error) + " " + mensaje
        else:
            return "2" + str(contador_error) + " " + mensaje


def validacion_bytes(mensaje):
    tamano = len(mensaje.encode('utf-8'))
    if tamano <= 40:
        return True
    else:
        return False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    enter_data()
