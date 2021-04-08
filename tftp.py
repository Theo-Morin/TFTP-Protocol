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


def write(filename,data):
    try:
        file = open(filename, "w")
    except Exception as e:
        print("problème d'ecriture dans le fichier :",filename)
    for contenu in data:
        file.write(contenu)
    file.close()
    
# code vérifé le contenue du fichier coté serveur s'envoie par paquet de taille blksize
def fileTreatment(sc,filename,blksize):       
    try:
        file = open(filename,'r')
    except Exception as e:
        print("Erreur de fichier\n")
    count = 1
    with open(filename,'r') as file:
        data = file.read(blksize)
        while len(data) == blksize:
            print(data)
            sc.send(createDAT(count,data.encode()))
            data = file.read(blksize)
    file.close() 
        
        


########################################################################

def sendRequest():
    # ToDo
    pass


########################################################################

def createACK(count):
    return b'\x00\x04' + count.to_bytes(2, 'big')

########################################################################


def createDAT(count, data):
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
        blksize = args[3].decode('ascii')
        print(blksize)
        return [opcode, filename, mode, int(blksize)]
    elif opcode == 3:
        # todo : b'\x00\x02BBBBBBBBBB'
        num = int.from_bytes(frame2[0:2], byteorder='big')
        data = int.from_bytes(frame2[2:], byteorder='big')
        return [opcode, num, data]
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
        opcode, filename, mode, blksize = decode(data)
        print(opcode)
        print(blksize)
        if opcode == 1:
            #ici la finaliter serai de recupérer la socket client pour envoyer le fichier lu il suffira d'utiliser
            # la fonction write coté client pour ecrire dans un nouveau fichier le contenu reçu
            # les ACK seront envoyer du côté client vers le serveur pour confirmer la récéption. 
            fileTreatment(socketclient,filename,blksize)
        if opcode == 2:
            pass
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
    req = b'\x00\x02' + bytearray(targetname, 'utf-8') + b'\x00blksize\x00'
    print(req)
    s.sendto(req, addr, blksize)
    # ToDo
    s.close()

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    s = connect(addr)
    req = b'\x00\x01' + bytearray(filename, 'utf-8') + b'\x00octet\x00' + b'blksize' +b'\x00' + bytearray(str(blksize),"utf-8") +b'\x00' # Exemple : b'\x00\x01hello.txt\x00octet\x00'
    print(req)
    s.sendto(req, addr)
    # ToDo
    # data, addr = s.recvfrom(1024)
    # print('[{}:{}] server reply: {}'.format(addr[0], addr[1], data))
    s.close()
    pass
# EOF