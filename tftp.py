"""
TFTP Module.
"""

########################################################################
#                               Authors                                #
#                  Théo Morin : contact@theomorin.fr                   #
#           Théo Berthier : theo.berthier@etu.u-bordeaux.fr            #
########################################################################


import socket
import sys



########################################################################
#                          COMMON ROUTINES                             #
########################################################################

def createACK(count):
    return b'\x00\x04' + count.to_bytes(2, 'big')

########################################################################


def createDAT(count, data):
    # ToDo
    return b'\x00\x03' + count.to_bytes(2, 'big') + bytearray(data, 'utf-8')

########################################################################


def decode(data):
    frame = data                                            # sample of WRQ as byte array
    frame1 = frame[0:2]                                     # Contient l'OP Code
    frame2 = frame[2:]                                      # frame2 = b'test.txt\x00octet\x00'
    opcode = int.from_bytes(frame1, byteorder='big')        # opcode = 2
    if opcode == 1 or opcode == 2:
        args = frame2.split(b'\x00')                        # args = [b'test.txt', b'octet', b'']
        filename = args[0].decode('ascii')                  # filename = 'test.txt'
        mode = args[1].decode('ascii')                      # mode = 'octet'
        return [opcode, filename, mode]
    elif opcode == 3:
        # todo : b'\x00\x03\x00\x02BBBBBBBBBB'
        return [opcode, None, None]
    elif opcode == 4:
        num = int.from_bytes(args[0], byteorder='big')
        return [opcode, num, None]

########################################################################
#                             SERVER SIDE                              #
########################################################################

def runServer(addr, timeout, thread):
    # todo
    print("Lancement du serveur...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(addr)
        print("Serveur lancé sur le port ", addr[1])
    except Exception as e:
        print("Erreur lors du lancement du serveur.")

    while True:
        data, addrm = s.recvfrom(1500)
        print('[{}:{}] client request: {}'.format(addrm[0], addrm[1], data))
        opcode, filename, mode = decode(data)
        print(opcode)
        # s.sendto(data, addrm)
        # print(data)
    s.close()
    pass

########################################################################
#                             CLIENT SIDE                              #
########################################################################


def connect(addr):
    print("Connexion au serveur..")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Connexion au serveur établie.")
        return s
    except Exception as e:
        print("Erreur lors de la connexion au serveur.")
        return None
    pass

########################################################################


def put(addr, filename, targetname, blksize, timeout):
    s = connect(addr)
    # ToDo
    s.close()
    pass

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    s = connect(addr)
    req = b'\x00\x01' + bytearray(filename, 'utf-8') + b'\x00octet\x00'     # Exemple : b'\x00\x01hello.txt\x00octet\x00'
    print(req)
    s.sendto(req, addr)
    # ToDo
    # data, addr = s.recvfrom(1024)
    # print('[{}:{}] server reply: {}'.format(addr[0], addr[1], data))
    s.close()
    pass
# EOF