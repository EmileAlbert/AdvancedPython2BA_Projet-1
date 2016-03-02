# Définition d'un serveur réseau gérant un système de CHAT simplifié.
# Utilise les threads pour gérer les connexions clientes en parallèle.

import socket, sys, threading

HOST = socket.gethostname()
PORT = 4444




class ThreadClient(threading.Thread):
    '''Dérivation d'un objet thread pour gérer la connexion avec un client'''

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn

    def run(self):
        # Dialogue avec le client :
        nom = self.getName()
        while 1:
            msgClient = self.connexion.recv(1024).decode("Utf8")
            if not msgClient or msgClient.upper() == "FIN" :
                break
            message = "%s > %s" % (nom, msgClient)
            print(message)
            # Faire suivre le messag à tous les autres clients :
            for cle in conn_client:
                if cle != nom :
                    conn_client[cle].send(message.encode("Utf8"))

        # Fermeture de la connexion :
        self.connexion.close()
        del conn_client[nom]
        print("Client %s déconnecté." % nom)
        # Le thread se termine ici.

# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try :
    mySocket.bind((HOST, PORT))
except socket.error :
    print("La liaison du socket à l'adresse choisie a échoué.")
    sys.exit()
print("Serveur prêt, en attente de requêtes ...")
mySocket.listen(5)

#Attente et prise en charge des connexions demandées par les clients :
conn_client = {}        # Dictionnaire des connections clients
while 1:
    connexion, adresse = mySocket.accept()
    # Créer un nouvel objet thread pour gérer la connexion :
    th = ThreadClient(connexion)
    th.start()
    # Mémoriser la connexion dans le dictionnaire :
    it = th.getName()       # Identifiant du thread
    conn_client[it] = connexion
    print("Client %s connecté, adresse IP %s, port %s." %\
          (it, adresse[0], adresse[1]))
    # Dialogue avec le client
    msg = "Vous êtes connecté. Envoyez vos messages."
    connexion.send(msg.encode("Utf8"))
