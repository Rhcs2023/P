import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile

# Diccionario con palabras a traducir
diccionario = {
    # 'a': '1',
    # 'b': '2',
    # 'c': '3',
    # 'd': '4',
    # 'e': '5',
    # 'f': '6',
    # 'g': '7',
    # 'h': '8',
}

def traducir_oracion(oracion):
    palabras = oracion.split()
    oracion_traducida = " ".join([diccionario.get(palabra.lower(), palabra) for palabra in palabras])
    return oracion_traducida

def reconocer_voz():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Por favor, habla ahora...")
        with st.spinner("Escuchando..."):
            audio = r.listen(source)
        try:
            oracion = r.recognize_google(audio, language='es-ES')
            st.write(f"Has dicho: {oracion}")
            return oracion
        except sr.UnknownValueError:
            st.error("............... Intenta otra vez bro")
            return ""
        except sr.RequestError:
            st.error("Error al conectar con el servicio de reconocimiento de voz.")
            return ""

def reproducir_audio(texto, lang):
    tts = gTTS(text=texto, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
        tts.save(tmp.name)
        with open(tmp.name, 'rb') as audio_file:
            audio_bytes = audio_file.read()
    return audio_bytes

st.title("Traductor de Español a Mixteco de Chalcatongo")

# Estado de la sesión para la traducción
if 'oracion_traducida' not in st.session_state:
    st.session_state.oracion_traducida = ""

# Opción para introducir texto
oracion_usuario = st.text_input("Pronombres posesivos van después del sujeto, ejemplo: Padre mi va al centro:")

# Botón para usar el reconocimiento de voz
if st.button("Usar micrófono"):
    oracion_usuario = reconocer_voz()

# Traducir la oración ingresada por el usuario
if oracion_usuario:
    oracion_traducida = traducir_oracion(oracion_usuario)
    st.session_state.oracion_traducida = oracion_traducida
    st.write(f"Traducción: {oracion_traducida}")
    audio_bytes = reproducir_audio(oracion_traducida, 'es')  # Usando español por defecto
    st.audio(audio_bytes, format='audio/mp3')
