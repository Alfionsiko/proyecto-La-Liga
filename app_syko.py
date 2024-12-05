import streamlit as st
import pandas as pd
from PIL import Image
import os


df = pd.read_csv("clasificacion_liga.csv")
df.set_index('Posición', inplace=True)
df2 = pd.read_csv("datos_curiosos.csv")
escudos_dir = os.path.join(os.getcwd(), 'escudos')
logo_dir = os.path.join(os.getcwd(), 'la-liga-santander-logo.png')
st.set_page_config(page_title="La Liga Santander",page_icon=logo_dir, layout="wide", initial_sidebar_state="collapsed")
st.image(logo_dir, width=180)

# Ruta al archivo CSV para guardar las puntuaciones
feedback_file = 'feedback.csv'
# Crear el archivo CSV si no existe
if not os.path.exists(feedback_file):
    df_feedback = pd.DataFrame({'Feedback': ['Me Gusta','No Me Gusta'], 'Count': [0, 0]})
    df_feedback.to_csv(feedback_file, index=False)
# Leer el archivo CSV
df_feedback = pd.read_csv(feedback_file)
# Funcion para registrar el feedback
def registrar_feedback(feedback):
    global df_feedback
    df_feedback.loc[df_feedback['Feedback'] == feedback, 'Count'] += 1 
    df_feedback.to_csv(feedback_file, index=False)
    

# Funcion para colorear columnas:
def color_columna(column): 
    if column.name == 'Equipo': 
        return ['background-color: silver'] * len(column) 
    else: 
        return ['background-color: #Add8E6'] * len(column)



# Aplicar estilos al DataFrame 
df_styled = df.style.apply(color_columna, axis=0)

          
def main():
    st.title("La Liga Santander")
    st.header("Clasificación")
    st.dataframe(df_styled)
    # Multiselect para seleccionar uno o más equipos
    equipos_seleccionados = st.multiselect("Selecciona un equipo", df2["Equipo"].unique())

    # Iterar sobre los equipos seleccionados y mostrar el dato curioso  
    for equipo in equipos_seleccionados:
        if equipo in df2["Equipo"].unique():
            dato_curioso = df2[df2["Equipo"] == equipo]["Dato Curioso"].values[0]
            escudo_path = os.path.join(escudos_dir, f'{equipo}.png') 
            if os.path.exists(escudo_path): 
                st.image(escudo_path, caption=equipo, width=100) 
            else: 
                st.write(f'No se encontró el escudo para {equipo}.')
            st.write(dato_curioso)
    
    # sidebar:
    st.sidebar.title("La Liga Santander")
    st.sidebar.write("Bienvenido a mi página de La Liga Santander")
    st.sidebar.write("En esta página encontraras toda la información sobre la clasificacion de La Liga")
    st.sidebar.write("Ademas de datos curiosos sobre los equipos de La Liga")
    st.sidebar.write("Espero que te diviertas navegando por ella y no te olvides de puntuarla")
    st.sidebar.title("Feedback")
    if st.sidebar.button("Me Gusta"):
        registrar_feedback("Me Gusta")
        st.sidebar.success("¡Gracias por tu feedback!")
    if st.sidebar.button("No Me Gusta"):
        registrar_feedback("No Me Gusta")
        st.sidebar.success("¡Gracias por tu feedback!")

    st.sidebar.write("Feedback recibido:") 
    st.sidebar.dataframe(df_feedback)
    
       
if __name__ == "__main__":
    main()


