import sys # Importa librerías para salir del programa
import socket  # Importa librerías para la comunicación por red
import threading  # Importa librerías para manejar múltiples hilos
import os # Importa librerías del sistema operativo 
import time # Importa librerías para manejar tiempos de espera


# Configuración de la conexión

IP = '127.0.0.1'  # Dirección IP del servidor
PUERTO = 5501  # Puerto en el que el servidor escucha
BUFFER_SIZE = 1024  # Tamaño del buffer para recibir mensajes

def mostrar_instrucciones():  # Función para mostrar instrucciones de uso al usuario.

    print("\n\nInstrucciones de uso:")
    print("1. Para enviar un mensaje a todos los clientes, usa el formato: #mensaje")
    print("2. Para enviar un mensaje a un cliente específico, usa el formato: destinatario>mensaje")
    print("3. Para ver la lista de clientes conectados, usa el comando: ?")
    print("4. Para desconectarse del servidor, usa el comando: logout\n")

def recibir_mensajes(socket_cliente, detener_evento): # Función para recibir mensajes del servidor de forma continua.

    
    while not detener_evento.is_set(): # Bucle que se ejecuta mientras el evento de detener no esté activado
        try:            
            mensaje = socket_cliente.recv(BUFFER_SIZE).decode('utf-8') # Recibe un mensaje del servidor
            if mensaje:                
                if "desconectando servidor" in mensaje.lower() or "logout" in mensaje.lower(): # Si el mensaje contiene "desconectando servidor" o "logout"
                    print("\nDesconectado del servidor..")
                    detener_evento.set()  # Detine el bucle y desconeccta del servidor 
                else:
                    print(f"\r{mensaje}\n", end="") # Imprime el mensaje recibido
            else:
                detener_evento.set()  # Detiene el bucle si no hay mensaje
        except:
            detener_evento.set()  # Detiene el bucle si hay una excepción

    # Cierra el socket del cliente
    try:
        socket_cliente.shutdown(socket.SHUT_RDWR)  # Cierra el socket para lectura y escritura
        socket_cliente.close()  # Cierra el socket
    except:
        pass  # Ignora cualquier excepción al cerrar el socket

    
    time.sleep(2) # Muestra el mensaje de desconexión del servidor por 2 segundos

    
    os.system('cls') # Limpia la pantalla
    sys.exit()# Cierra programa

if len(sys.argv) < 2: # Verifica que se haya ingresado un nombre al iniciar el cliente
    print("\n\nPara iniciar como cliente debes ingresar con tu nombre, como en el siguiente formato:\n 'python cliente.py NOMBRE' \n")
    sys.exit()

nombre = sys.argv[1].capitalize()  # Obtiene el nombre del cliente y lo capitaliza (primera letra en mayúscula, el resto en minúscula)
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Crea un socket para el cliente
socket_cliente.connect((IP, PUERTO)) #se conecta al servidor
socket_cliente.send(nombre.encode('utf-8')) # Envía el nombre del cliente al servidor
mostrar_instrucciones() # Muestra las instrucciones de uso al usuario
detener_evento = threading.Event() # Crea un evento para detener la recepción de mensajes
thread_recibir = threading.Thread(target=recibir_mensajes, args=(socket_cliente, detener_evento)) # Crea un hilo nuevo para recibir mensaje
thread_recibir.start() # Inicia un hilo para recibir mensajes del servidor

try:  # bucle para enviar mensajes
    while not detener_evento.is_set():        
        mensaje = input()# Espera la entrada del usuario        
        if detener_evento.is_set():# Verifica si el evento de detener está activado 
            break        
        if mensaje.lower() == "logout" or mensaje == "?": # Si el usuario ingresa "logout" o "?", envía el mensaje al servidor
            socket_cliente.send(mensaje.encode('utf-8'))            
            if mensaje.lower() == "logout": # Si el mensaje es "logout", activa el evento de detener y sale del bucle
                detener_evento.set()
                break
        
        elif mensaje.startswith("#"): # Si el mensaje comienza con "#", envía el mensaje a todos los clientes conectados
            socket_cliente.send(mensaje.encode('utf-8'))        
        elif ">" in mensaje: # Si el mensaje contiene ">", se interpreta como un mensaje privado            
            dest, msj = mensaje.split(">", 1) # Divide el mensaje en destinatario y mensaje            
            mensaje = f"{dest.capitalize()}>{msj}" # Capitaliza el nombre del destinatario y reconstruye el mensaje
            try:                
                socket_cliente.send(mensaje.encode('utf-8'))# Envía el mensaje al servidor
            except OSError: # Capta un error y sale del bucle
                break
        else:
            # Mensaje de error si el formato no es correcto
            error_mensaje = "\n\nERROR: Mensaje sin destinatario. Usa el formato correcto:\n" \
                            "1. Para enviar un mensaje a todos los clientes: #mensaje\n" \
                            "2. Para enviar un mensaje a un cliente específico: destinatario>mensaje\n\n"
            print(error_mensaje)
            try:                
                socket_cliente.send(f"ERROR FORMATO: {mensaje}".encode('utf-8')) # Envía un mensaje de error al servidor
            except OSError: # Capta un error y sale del bucle
                break
except :
        pass # Ignora cualquier excepcion
finally:
    
    thread_recibir.join() # Espera a que el hilo de recepción de mensajes termine    
    os.system('cls') # Limpia la pantalla    
    sys.exit() # Cierra el programa