import xmlrpc.server
# import xmlrpc.client
import time
import threading
import logging

def cifrado(texto,desplazamiento):
    texto = texto.upper()
    alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    cifrado = ""
    for letra in texto:
        if letra in alfabeto:
            posicion = alfabeto.find(letra)
            nueva_posicion = (posicion + desplazamiento) % 27
            cifrado += alfabeto[nueva_posicion]
        else:
            cifrado += letra
    return cifrado

def descifrado(texto,desplazamiento):
    texto = texto.upper()
    alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    descifrado = ""
    for letra in texto:
        if letra in alfabeto:
            posicion = alfabeto.find(letra)
            nueva_posicion = (posicion - desplazamiento) % 27
            descifrado += alfabeto[nueva_posicion]
        else:
            descifrado += letra
    return descifrado

def linea():
    return "Servidor en linea 192.168.1.75 en puerto 3312"


def get_time():
    logging.debug(f"Obteniendo tiempo del local...")
    return time.time() * 1000

def get_server_time():
    logging.debug(f"HORA DEL SERVIDOR solicitada...")
    return get_time()


server = xmlrpc.server.SimpleXMLRPCServer(("192.168.1.183", 3313))
print("Esperando consultas de cifrado...")

server.register_function(cifrado, "cifrado")
server.register_function(descifrado, "descifrado")
server.register_function(linea, "linea")
server.register_function(get_server_time, "get_server_time")


server.serve_forever()


# import xmlrpc.server
# # import xmlrpc.client
# import time
# import threading
# import logging

# logging.basicConfig(filename='bitacoraServers.log', level=logging.DEBUG,filemode='w', 
#                     format='%(asctime)s | %(levelname)s:%(message)s | %(threadName)s | %(funcName)s | %(lineno)d|')

# def get_time():
#     logging.debug(f"Obteniendo tiempo del local...")
#     return time.time() * 1000

# def get_server_time():
#     logging.debug(f"HORA DEL SERVIDOR solicitada...")
#     return get_time()

# ptos = [3312, 3313, 3314, 3315, 3316, 3317, 3318, 3319]
# servers = []

# def run_server(port):
#     logging.debug(f"Iniciando servidor en el puerto {port}...")
#     server = xmlrpc.server.SimpleXMLRPCServer(("192.168.1.183", port))
#     logging.debug(f"Servidor iniciado en el puerto {port}...")
#     server.register_function(get_server_time, "get_server_time")
#     logging.debug(f"Servidor registrado en el puerto {port}...")
#     print(f"Servidor en ejecución en el puerto {port}...")
#     server.serve_forever()

# # Iniciamos los servidores en hilos separados
# threads = []
# for port in ptos:
#     logging.debug(f"Iniciando hilo para el puerto {port}...")
#     thread = threading.Thread(target=run_server, args=(port,))
#     logging.debug(f"Hilo iniciado para el puerto {port}...")
#     thread.start()
#     threads.append(thread)
#     logging.debug(f"Hilo agregado a la lista de hilos...")

# # Esperamos a que todos los hilos finalicen
# for thread in threads:
#     logging.debug(f"Esperando a que el hilo {thread} finalice...")
#     thread.join()
