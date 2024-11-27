import streamlit as st #importamos la librería
from groq import Groq

#Le damos un título a nuestra página web
st.set_page_config(page_title="matIAs", page_icon="🐼")
#posicion      0           1           2
MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#Nos conecta a la API, crear un usuario
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"] #Obteniendo la clave de nuestro archivo
    return Groq(api_key = clave_secreta) #Crea al usuario

#cliente = usuario de groq | modelo es la IA seleccionada | mensaje del usuario
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo, #Indica el modelo de la IA
        messages = [{"role":"user", "content": mensajeDeEntrada}],
        stream = True #Para que el modelo responda a tiempo
    )

#Simula un historial de mensajes
def inicializar_estado(): 
    #Si "mensajes" no está en st.session_state
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #Memoria de mensajes

def actualizar_historial(rol, contenido, avatar):
    #El metodo append() agrega un elemnto a la lista
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : 
            st.markdown(mensaje["content"])

#Contenedor del chat
def area_chat():
    contenedorDelChat = st.container(height= 400, border= True)
    #Agrupamos los mensajes en el área del chat
    with contenedorDelChat : mostrar_historial()

#CREANDO FUNCIÓN --> con diseño de la página
def configurar_pagina():

    st.title("Chatea con matIAs") #Titulo
    st.sidebar.title("Configuración") #Menú lateral
    seleccion = st.sidebar.selectbox(
        "Elegí un módulo", #Título
        MODELO, #Tienen que estar en una lista
        index = 0 #datoDefecto
    )

    return seleccion #Devuelve un dato

def generar_respuestas(chat_completo):
    respuesta_completa = "" #Texto vacío
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content

    return respuesta_completa #devuelve rta completa

def main():
    #INVOCACIÓN DE FUNCIONES
    modelo = configurar_pagina() #Llamamos a la función
    clienteUsuario = crear_usuario_groq() #Crea el usuario para usar la API
    inicializar_estado() #Crea el historial vacío de mensaje
    area_chat() #Creamos el sector para ver los mensajes
    mensaje = st.chat_input("Escribí tu mensaje...")

    #Verificar si el mensaje tiene contenido
    if mensaje:
        actualizar_historial("user", mensaje, "👾") #Visualizamos el mensaje del usuario
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant") :
                respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "👽")
                st.rerun()

#Indicamos que nuestra función principal es main()
if __name__ == "__main__":
    main()