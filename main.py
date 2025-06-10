import streamlit as st 
import groq 

MODELOS = [
    'llama3-8b-8192',
    'llama3-70b-8192',
    'llama-3.1-8b-instant',
    'llama-3.3-70b-versatile',
    'gemma2-9b-it',
    'deepseek-r1-distill-llama-70b'
]


#CONFIGURAR PÁGINA ------------------------------------
def configurar_pagina():
    st.set_page_config(page_title="Mi primer Chatbot con Python")
    st.title("Bienvenido a Tu Asistente Virtual")
#  ----------------------------------------------------

#CREAR UN CLIENTE GROQ (NOSOTROS) ---------------------
def crear_un_cliente_groq():
    grok_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=grok_api_key)
#  ----------------------------------------------------

#MOSTRAR BARRA LATERAL --------------------------------
def mostrar_sidebar():
    st.sidebar.title("Elegí tu modelo de IA")
    modelo = st.sidebar.selectbox("Modelos a elección:", MODELOS, index=0)
    st.write(f"**Elegiste el modelo: {modelo}**")
    return modelo
#  ----------------------------------------------------

#INICIALIZAR EL ESTADO DEL CHAT -----------------------
def inicializar_estado_chat():
    if "mensajes" not in st.session_state:      # Funcion que crea una variable con una lista
        st.session_state.mensajes = [] 
#  ----------------------------------------------------

#MOSTRAR MENSAJES PREVIOS -----------------------------
def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes:    # Recorre los mensajes de la lista
        with st.chat_message(mensaje['role']):   # Rol de * quien * lo envia 
            st.markdown(mensaje['content'])      # Contenido enviado
#  ----------------------------------------------------

#OBTENER MENSAJES USUARIO -----------------------------
def obtener_mensaje_usuario():
    return st.chat_input("Envie un mensaje...")
#  ----------------------------------------------------

#GUARDAR LOS MENSAJES ---------------------------------
def agregar_mensajes_previos(role, content):
    st.session_state.mensajes.append({"role": role, "content": content})
#  ----------------------------------------------------

#MOSTRAR MENSAJES EN PANTALLA -------------------------
def mostrar_mensajes(role, content):
    with st.chat_message(role):
        st.markdown(content)
#  ----------------------------------------------------

#LLAMAR MODELO GROQ
def obtener_respuesta_modelo(cliente, modelo, mensaje):
    respuesta = cliente.chat.completions.create(
        model = modelo,
        messages = mensaje,
        stream = False,
    )
    return respuesta.choices[0].message.content 
#  ----------------------------------------------------



#EJECUTAR CHAT ----------------------------------------
def ejecutar_chat():
    configurar_pagina()
    cliente = crear_un_cliente_groq()
    modelo = mostrar_sidebar()
    
    inicializar_estado_chat()
    mensaje_usuario = obtener_mensaje_usuario()
    obtener_mensajes_previos()
    
    if mensaje_usuario:
        agregar_mensajes_previos("user", mensaje_usuario)
        mostrar_mensajes("user", mensaje_usuario)
        
        respuesta_contenido = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)
        
        agregar_mensajes_previos("assistant", respuesta_contenido)
        mostrar_mensajes("assistant", respuesta_contenido)
#  ----------------------------------------------------

#EJECUTAR LA APP --------------------------------------
if __name__ == '__main__':
    ejecutar_chat()
#  ----------------------------------------------------



