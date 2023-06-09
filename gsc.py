import logging
import xmlrpc.server
import xmlrpc.client
import time
import concurrent.futures
import datetime


logging.basicConfig(filename='bitacoraGSC.log', level=logging.DEBUG,filemode='w', 
                    format='%(asctime)s | %(levelname)s:%(message)s | %(threadName)s | %(funcName)s | %(lineno)d|')

listaServidores = [[1,"http://192.168.1.183:3313/RPC2"],[1,"http://192.168.1.183:3314/RPC2"],[1,"http://192.182.1.161:3312/RPC2"]]
listaActivosG = []

def format_time(synced_time):
    synced_time2 = synced_time
    synced_time_seconds = synced_time2 / 1000  # Convertir a segundos

    # Crear objeto datetime a partir del tiempo sincronizado en segundos
    synced_datetime = datetime.datetime.fromtimestamp(synced_time_seconds)

    # Formatear el objeto datetime como una cadena legible
    formatted_time = synced_datetime.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_time

def get_time():
    logging.debug("Obteniendo tiempo actual...")
    return time.time() * 1000

def sync_time(host):
    # Creamos el proxy del servidor RPC
    server = xmlrpc.client.ServerProxy(host)
    logging.debug(f"Conectando con {host}...")

    # Obtenemos el tiempo del servidor
    server_time = server.get_server_time()
    logging.debug(f"Tiempo del servidor: {server_time}")

    # Calculamos el tiempo de latencia (ida y vuelta) de la solicitud
    latency = (get_time() - float(server_time)) / 2.0
    logging.debug(f"Latencia: {latency}")
    # Calculamos el tiempo actual del servidor
    current_time = get_time() - latency
    logging.debug(f"Tiempo actual: {current_time}")

    # Devolvemos el tiempo actual del servidor
    return current_time

def Servidores():
    while(1):
        for i in range(len(listaServidores)):
            try:
                serverStat(i)
                listaServidores[i][0] = 1
            except:
                print("Servidor caido")
                logging.debug(f"Servidor {listaServidores[i][1]} caido")
                print(listaServidores[i][1])
                listaServidores[i][0] = 0
            if i == 1:
                time.sleep(1)
            #print(listaServidores[i][0])

def serverLocal():
    try:
        logging.debug("Iniciando servidor")
        server = xmlrpc.server.SimpleXMLRPCServer(("192.168.1.183", 3312))
        logging.debug("Servidor iniciado")
    except:
        logging.debug("No se pudo iniciar el servidor")
        print("No se pudo iniciar el servidor")

    server.register_function(handle_connection, "_dispatch")
    server.register_function(ServerFree, "libres")
    server.register_function(solicitud, "solicitud")
    server.serve_forever()
    
def solicitud(texto,desplazamiento):
    logging.debug(f"ESTAS EN GSC EN LA FUNCION SOLICITUD ...")
    i=0
    while i<=len(listaServidores):
        logging.debug(f"PROBANDO SERVIDOR {listaServidores[i][1]} ...")
        if (listaServidores[i][0]==1):
            logging.debug(f"EL SERVIDOR {listaServidores[i][1]} ESTA LIBRE ...")
            listaServidores[i][0]==0
            logging.debug(f"ENVIANDO SOLICITUD AL SERVIDOR {listaServidores[i][1]} ...")
            proxy = xmlrpc.client.ServerProxy(listaServidores[i][1])
            logging.debug(f"CONECTADO AL SERVIDOR: {listaServidores[i][1]} Y ENVIANDO EL TEXTO...")
            cifrado = proxy.cifrado(texto,desplazamiento)
            #print(resultado)
            logging.debug(f"RECIBIENDO TEXTO CIFRADO DEL SERVIDOR {listaServidores[i][1]} ...")
            listaServidores[i][0]==1
            logging.debug(f"EL SERVIDOR {listaServidores[i][1]} ESTA LIBRE ...")
            i=len(listaServidores)
            logging.debug(f"RETORNANDO TEXTO CIFRADO AL CLIENTE ...")
            return cifrado
        
        else:
            i=i+1

def serverStat(a):
    # Crear proxy
    #logging.debug(f"Conectando con {listaServidores[a][1]}...")
    #print("CONECTANDO CON VM...")
    #http://192.168.1.75:3312/RPC2
    proxy = xmlrpc.client.ServerProxy(listaServidores[a][1])
    #print("CONECTADO CON VM...\n")
    # Llamar función del servidor
    resultado = proxy.linea()
    # Imprimir resultado
    #print(resultado)
    #return resultado


#la funcion linea manda a quien la invoca un hola mundo
def ServerFree():
    listaActivos = []
    for i in range(len(listaServidores)):
        if listaServidores[i][0] == 1:
            listaActivos.append(listaServidores[i][1])
    return listaActivos

def handle_connection(client_ip):
    # Registra la conexión en la bitácora
    logging.info(f"Cliente {client_ip} se ha conectado")



def christian(listaActivosG):
    listaActivosG = ServerFree()
    #print (listaActivosG[0])
    i=0
    while i <= len(listaActivosG):
        logging.debug(f"Sincronizando tiempo con servidor {listaActivosG[i]}...")
        logging.debug(f"Conectando con {listaActivosG[i]}...")
        #realizamos un try para ver si el servidor esta activo
        synced_time = sync_time(listaActivosG[i])
        logging.debug(f"Tiempo sincronizado del servidor {listaActivosG[i]}: {synced_time}")
        formatted_time = format_time(synced_time)
        logging.debug(f"Tiempo sincronizado del servidor {listaActivosG[i]}: {formatted_time}")
        print(f"Tiempo sincronizado del servidor {listaActivosG[i]}: {formatted_time}")
        i=i+1


print("SERVIDOR GSC CORRIENDO...")


logging.debug("Iniciando executor de hilos")
ejecutaHilo = concurrent.futures.ThreadPoolExecutor()

logging.debug("Ejecutando hilo 2")
mi_hilo = ejecutaHilo.submit(Servidores)

logging.debug("Ejecutando hilo 1")
mi_hilo2 = ejecutaHilo.submit(serverLocal)

logging.debug("Ejecutando sincronizacion de tiempo")
mi_hilo3 = ejecutaHilo.submit(christian,listaActivosG)


