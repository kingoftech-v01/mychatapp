import socket
import threading

# Configuration du serveur
HOST = '127.0.0.1'  # Adresse IP du serveur
PORT = 55555        # Port d'écoute

# Création du socket serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Listes pour stocker les clients et leurs pseudos
clients = []
pseudos = []

# Fonction pour diffuser un message à tous les clients
def diffuser(message):
    for client in clients:
        client.send(message)

# Fonction pour gérer les connexions des clients
def gerer_client(client):
    while True:
        try:
            message = client.recv(1024)
            diffuser(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            pseudo = pseudos[index]
            diffuser(f'{pseudo} a quitté le chat!'.encode('utf-8'))
            pseudos.remove(pseudo)
            break

# Fonction principale pour accepter les connexions
def recevoir():
    while True:
        client, address = server.accept()
        print(f"Connecté avec {str(address)}")

        client.send('PSEUDO'.encode('utf-8'))
        pseudo = client.recv(1024).decode('utf-8')
        pseudos.append(pseudo)
        clients.append(client)

        print(f"Le pseudo du client est {pseudo}")
        diffuser(f'{pseudo} a rejoint le chat!'.encode('utf-8'))
        client.send('Connecté au serveur!'.encode('utf-8'))

        thread = threading.Thread(target=gerer_client, args=(client,))
        thread.start()

print("Le serveur écoute...")
recevoir()
