import sys # Importa librerías para salir del programa
import socket  # Importa librerías para la comunicación por red
import threading  # Importa librerías para manejar múltiples hilos
import os # Importa librerías del sistema operativo 
import time # Importa librerías para manejar tiempos de espera


# Configuración de la conexión

IP = '127.0.0.1'  # Dirección IP del servidor
PUERTO = 5501  # Puerto en el que el servidor escucha
BUFFER_SIZE = 1024  # Tamaño del buffer para recibir mensajes


# Variables globales

clientes = {}  # Diccionario para almacenar los clientes conectados
servidor_corriendo = True  # Servidor corriendo
errores_mensajes = []  # Lista para almacenar errores de mensajes


def manejar_cliente(socket_cliente, direccion): # Función para manejar la comunicación con un cliente conectado
    
    nombre_cliente = socket_cliente.recv(BUFFER_SIZE).decode('utf-8').capitalize() # Recibe el nombre del cliente y lo capitaliza (primera letra en mayúscula, el resto en minúscula)    
    clientes[nombre_cliente] = socket_cliente # Guarda el cliente en el diccionario 'clientes' usando el nombre como clave y el socket como valor
    print(f"[SERVIDOR] Se ha conectado el cliente \"{nombre_cliente}\" - IP: {direccion[0]} || Puerto: {direccion[1]}\n") # Imprime que cliente se conecto , de que IP y de cual PUERTO

    try:
        while servidor_corriendo:  # Bucle que se ejecuta mientras el servidor esté corriendo            
            mensaje = socket_cliente.recv(BUFFER_SIZE).decode('utf-8') # Recibe un mensaje del cliente
            if mensaje:  # Si el mensaje no está vacío
                if mensaje.lower() == "logout":  # Si el cliente quiere desconectarse
                    break  # Sale del bucle
                if mensaje == "?":  # Solicita la lista de clientes
                    lista_clientes = ", ".join(clientes.keys())  # Crea una lista de clientes conectados                   
                    socket_cliente.send(f"Clientes conectados: {lista_clientes}\n".encode('utf-8')) # Envía la lista de clientes conectados al cliente solicitante
                elif mensaje.startswith("#"):  # Envia mensaje a todos los clientes                    
                    msj_general(mensaje[1:], nombre_cliente) # Llama a la función para enviar el mensaje a todos los clientes
                elif ">" in mensaje:  # Envia mensaje a un cliente específico                    
                    dest, msj = mensaje.split(">", 1) # Divide el mensaje en destinatario y mensaje
                    dest = dest.capitalize()  # Capitaliza el nombre del destinatario (pone en mayuscula la primer letra y deja en minuscula las demas)
                    if dest in clientes:  # Si el destinatario existe en la lista de clientes                       
                        clientes[dest].send(f"{nombre_cliente}: {msj}\n".encode('utf-8'))  # Envía el mensaje al destinatario                       
                        print(f"{nombre_cliente} --> {dest} : '{msj}'") # Imprime en el servidor el mensaje enviado
                    else:                        
                        socket_cliente.send(f"Cliente inexistente {dest}\n".encode('utf-8')) # Si el cliente ingresado no existe, muestra mensaje de error al remitente                        
                        print(f"Mensaje a cliente inexistente: {nombre_cliente} --> {dest} : '{msj}'") # Imprime en el servidor el intento de envío a un cliente inexistente
                elif mensaje.startswith("ERROR FORMATO:"):  # Si el formato ingresado no es válido                    
                    errores_mensajes.append((nombre_cliente, mensaje))# Añade el mensaje de error a la lista de errores                    
                    print(f"Error de mensajes de {nombre_cliente}: {mensaje}") # Imprime en el servidor el mensaje de error
                else:  # Para cualquier otro error de mensaje                    
                    errores_mensajes.append((nombre_cliente, mensaje)) # Añade el mensaje de error a la lista de errores                    
                    print(f"Error de mensajes de {nombre_cliente}: {mensaje}") # Imprime en el servidor el mensaje de error
            else:  # Si el mensaje está vacío, sale del bucle
                break
    except ConnectionError:
        pass  # Si hay un error de conexión, lo ignora y continúa
    finally:
        if nombre_cliente in clientes:  # Si el cliente sigue en la lista de clientes
            del clientes[nombre_cliente]  # Elimina al cliente de la lista        
        print(f"Cliente \"{nombre_cliente}\" desconectado.") # Imprime en el servidor que el cliente se ha desconectado       
        socket_cliente.close() # Cierra el socket del cliente


def msj_general(mensaje, remitente): # Función para enviar un mensaje a todos los clientes excepto al remitente.
        
    for nombre, cliente in clientes.items(): # Itera sobre todos los clientes conectados        
        if nombre != remitente: # Verifica que el cliente no sea el remitente            
            cliente.send(f"{remitente}: {mensaje}\n".encode('utf-8')) # Envía el mensaje al cliente            
            print(f"{remitente} --> Todos : '{mensaje}'") # Imprime en el servidor el mensaje enviado a todos los clientes


def cerrar_servidor(): # Función para cerrar el servidor y desconectar a todos los clientes.
    
    global servidor_corriendo
    
    servidor_corriendo = False  # Cambia el estado del servidor a no corriendo
    print("\n[SERVIDOR] Desconectando todos los clientes y cerrando el servidor...")
    
    for cliente in list(clientes.values()): # Itera sobre todos los clientes conectados
        try:            
            cliente.send("Desconectando servidor\n".encode('utf-8')) # Envía un mensaje de desconexión a cada cliente            
            cliente.close() # Cierra la conexión con el cliente
        except:
            pass  # Ignora cualquier excepción
    clientes.clear()  # Vacía el diccionario de clientes
    time.sleep(2)  # Añade un retraso de 2 segundos para la lectura del mensaje
    os.system('cls')  # Limpia la pantalla
    sys.exit()  # Cierra el programa


def aceptar_conexiones(server_socket): # Función para aceptar conexiones entrantes.
    
    global servidor_corriendo
    
    while servidor_corriendo:
        try:
            
            conn, addr = server_socket.accept() # Acepta una conexión entrante
            if not servidor_corriendo:
                conn.close()  # Cierra la conexión si el servidor no está corriendo
                break
            
            thread = threading.Thread(target=manejar_cliente, args=(conn, addr)) # Crea un hilo para manejar la nueva conexión
            thread.start()  # Inicia el hilo
        except OSError:
            break  # Sale del bucle si hay una excepción de sistema operativo


def main(): # Función principal para iniciar el servidor y aceptar conexiones entrantes.

    global servidor_corriendo

    print("\n\n[SERVIDOR] Iniciando\n")
   
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP/IP    
    server_socket.bind((IP, PUERTO)) # Asocia el socket a la dirección IP y puerto    
    server_socket.listen() # El servidor puede escuchar el maximo permitido por el sistema operativo de conexiones entrantes
    
    print(f"[SERVIDOR] Escuchando en IP: {IP} || Puerto: {PUERTO}\n")

    
    aceptar_conexiones_thread = threading.Thread(target=aceptar_conexiones, args=(server_socket,))  # Crea un hilo para aceptar conexiones entrantes
    aceptar_conexiones_thread.start()  # Inicia el hilo

    try:
        while servidor_corriendo:  # Bucle que se ejecuta mientras el servidor esté corriendo
            comando = input()  # Espera a que el usuario ingrese un comando
            if comando.lower() == "logout":  # Si el usuario ingresa "logout"
                cerrar_servidor()  # Llama a la función para cerrar el servidor
            else:
                print("Comando no válido. El único comando permitido es 'logout' para cerrar el servidor.")
    except :
        pass
    finally:
        servidor_corriendo = False  # Cambia el estado del servidor a no corriendo
        if server_socket:  # Si el socket del servidor existe
            server_socket.close()  # Cierra el socket del servidor
        aceptar_conexiones_thread.join()  # Espera a que el hilo de aceptar conexiones termine
        os.system('cls')  # Limpia la pantalla
        sys.exit()  # Cierra el programa


if __name__ == "__main__": # verifica si se esta ejecutando directamente y da inicio al servidor
    main()