# Sala de Chat en Python

El proyecto es de una sala de chat sencilla utilizando sockets en Python,con dos componentes principales: un servidor ('server.py') y múltiples clientes('cliente.py').

## Requisitos

- Python 3.x

## Instrucciones

### 1. Iniciar el Servidor

El servidor maneja las conexiones de los clientes y gestiona la comunicación entre ellos.

#### Pasos para Iniciar el Servidor

    Abre una terminal.
    Navega al directorio donde se encuentra `server.py`.
    Ejecuta el servidor con el siguiente comando: `python server.py`.


### 2. Iniciar el Cliente
El cliente se conecta al servidor para enviar y recibir mensajes. Se pueden ejecutar varios clientes en diferentes terminales para crear la sala de chat e intercambiar mensajes.

#### Pasos para Iniciar el Cliente
    Abre una nueva terminal.
    Navega al directorio donde se encuentra `cliente.py`.
    Ejecuta el cliente con el siguiente comando, reemplazando NOMBRE con el nombre del cliente: `python cliente.py NOMBRE`.

# Comandos

## Comandos del Servidor
 LOGOUT: Cierra el servidor y desconecta a todos los clientes.
 
## Comandos del Cliente
 DESTINATARIO>MENSAJE: Envía un mensaje a un cliente específico.

 '#MENSAJE' : Envía un mensaje a todos los clientes conectados.

 '?' : Muestra la lista de clientes conectados. 

 LOGOUT: Desconecta el cliente del servidor.




## Authors

- [@Gaston Murua](ttps://github.com/JGastonMurua)

