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


def writeInFile(filename,data):
    try:
        file = open(filename, "w")
        for contenu in data:
            file.write(contenu)
        file.close()
    except Exception as e:
        print("\033[91mProblème d'ecriture dans le fichier :",filename)

########################################################################


def addToFile(filename,data):
    try:
        # file = open(filename, "w")
        # for contenu in data:
        #     file.write(contenu)
        # file.close()
        file = open(filename, "a")
        file.write(data)
        file.close()
    except Exception as e:
        print("\033[91mProblème d'ecriture dans le fichier :",filename)

########################################################################


# code vérifé le contenue du fichier coté serveur s'envoie par paquet de taille blksize
def fileTreatment(sc,addr,filename,blksize):
    try:
        file = open(filename,'r')
        count = 1
        with open(filename,'r') as file:
            data = file.read(blksize)
            while len(data) == blksize or count == 1:
                try:
                    DAT = createDAT(count, data)
                    sc.sendto(DAT, addr)
                except:
                    print("\033[91mImpossible d'envoyer le packet au client.")
                # sc.sendall(createDAT(count,data))
                count = count + 1
                data = file.read(blksize)
        file.close() 
    except Exception as e:
        print("\033[91mImpossible de lire dans le fichier.\n")

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
        return [opcode, filename, mode, int(blksize)]
    elif opcode == 3:
        # todo : b'\x00\x02BBBBBBBBBB'
        num = int.from_bytes(frame2[0:2], byteorder='big')
        data = frame2[2:].decode()
        return [opcode, num, data, None]
    elif opcode == 4:
        num = int.from_bytes(args[0], byteorder='big')
        return [opcode, num, None, None]

########################################################################
#                             SERVER SIDE                              #
########################################################################

def runServer(addr, timeout, thread):
    # todo
    print("\033[93mLancement du serveur...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(addr)
        print("\033[92mServeur lancé sur le port", addr[1])
    except Exception as e:
        print("\033[91mErreur lors du lancement du serveur.")

    while True:
        data, addrm = s.recvfrom(1500)
        print('\033[0m[{}:{}] client request: {}'.format(addrm[0], addrm[1], data))
        opcode, filename, mode, blksize = decode(data)
        if opcode == 1:
            # la fonction write coté client ecrie dans un nouveau fichier le contenu reçu
            # les ACK seront envoyer du côté client vers le serveur pour confirmer la récéption. 
            fileTreatment(s,addrm,filename,blksize)
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
    print("\033[93mConnexion au serveur..")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("\033[92mConnexion au serveur établie.")
        return s
    except Exception as e:
        print("\033[91mErreur lors de la connexion au serveur.")
        return None
    pass

########################################################################


def put(addr, filename, targetname, blksize, timeout):
    s = connect(addr)
    req = b'\x00\x02' + bytearray(targetname, 'utf-8') + b'\x00blksize\x00'
    s.sendto(req, addr, blksize)
    # ToDo
    s.close()

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    s = connect(addr)
    req = b'\x00\x01' + bytearray(filename, 'utf-8') + b'\x00octet\x00' + b'blksize' +b'\x00' + bytearray(str(blksize),"utf-8") +b'\x00' # Exemple : b'\x00\x01hello.txt\x00octet\x00'
    s.sendto(req, addr)
    # ToDo
    if len(targetname) == 0:
        targetname = filename
    while True:
        data, addr = s.recvfrom(1024)
        opcode, num, data, _ = decode(data)
        if opcode == 3:
            writeInFile(targetname, data)
            req = createACK(num)
            s.sendto(req, addr)
            if len(data) < blksize:
                print("\033[92mL'intégralité du fichier vient d'être récupéré !")
                break
    # print('[{}:{}] server reply: {}'.format(addr[0], addr[1], data))
    s.close()
    pass
# EOF