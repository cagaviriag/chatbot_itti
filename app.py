import streamlit as st
from coree.chat import init_context
from services.model_client import get_model_response, MODEL_ALIASES
from evaluation.evaluator import main_evaluador
from pathlib import Path
import uuid
import json
from datetime import datetime
import pandas as pd
import io
import numpy as np

st.set_page_config(page_title="ITTI ChatBot")

pag = st.sidebar.selectbox("Seleccione pagina", ["ChatBot Fintech", "Evaluación de resultados"])

if pag == "ChatBot Fintech":

    # Sidebar 
    st.sidebar.title("ITTIAssisten fintech")
    st.sidebar.markdown("""
    ### 📝 Instrucciones

    1. Escribe tu pregunta en el cuadro de texto.
    2. Presiona **Enviar** para recibir una respuesta.
    3. Puedes consultar temas relacionados con:

    - 💳 **Tarjetas de débito**
    - 💰 **Tarjetas de crédito**
    - 🏦 **Préstamos**

    4. Puedes seleccionar el **modelo de IA** que deseas que responda a tu pregunta.
                                                            
    ¡Estamos aquí para ayudarte!
    """)

    modelo = st.sidebar.selectbox("Seleccione modelo", list(MODEL_ALIASES.keys()))

    nombre_fintech = st.text_input("Escribe el nombre fintech (solo diponible para configuracion interna):")

    # paginta inicial
    st.image("media/itti_ico-min.png", width=150)
    st.title("Bienvenidos a ITTIAssisten fintech")

    if nombre_fintech != '':

        # Inicializar contexto
        if "messages" not in st.session_state:
            st.session_state.messages = init_context(nombre_fintech)
            st.session_state.resultado = None

        # Mostrar conversación
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.write(f"**Usuario:** {msg['content']}")
            elif msg["role"] == "assistant":
                st.write(f"**ChatBot:** {msg['content']}")

        # Input
        user_input = st.text_input("Escribe tu mensaje:",key="user_input")

        col1, col2 = st.columns([4, 1])

        with col1:
            if st.button("Enviar") and st.session_state.user_input.strip():
                st.session_state.messages.append({"role": "user", "content": user_input})
                _, st.session_state.messages = get_model_response(modelo, st.session_state.messages)
                st.rerun()
                st.rerun()


        with col2:
            if st.button('Finalizar chat'):
                output_dir = Path("data/conversations")
                output_dir.mkdir(parents=True, exist_ok=True)
                
                session_id = str(uuid.uuid4())
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = output_dir / f"{timestamp + "_" + modelo}.json"

                conversation_data = {
                    "timestamp": timestamp,
                    "session_id": session_id,
                    "modelo": modelo,
                    "turns": st.session_state.messages
            }
            
                #Guardar archivo JSON
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(conversation_data, f, indent=2, ensure_ascii=False)

                st.success(f"✅ Conversación guardada correctamente como: {filename.name}")
                
                #Reiniciar el contexto
                st.session_state.messages = []
                st.rerun()
else:

    st.title("Evaluación de resultados")

    st.markdown("""
    ### 📝 Instrucciones

    1. Selecciona el tipo de evaluacion que desea realizar:
    **Ragas**, **Ground truth**, **Otro LLM** o **Todas**.
    2. Presiona **Ejecutar** para que se inicie el proceso de evaluación o **Cargar resultados de evaluaciones anteriores** para mostrar los resultados guardados.
    3. Los resultados se mostrarán tanto en un tabla como en un json.
    4. Puedes descargar los resultados tanto en excel como json.
    5. El proceso toma las conversaciones de la carpeta `data/conversations` que fueron guardadas automaticamente déspues de 
    precionar finalizar chat de la pagina ChatBot Fintech.

    """)

        # Inicializar contexto
    if "resultado" not in st.session_state:
        st.session_state.resultado = None

    if "mostrar_resultados" not in st.session_state:
        st.session_state.mostrar_resultados = False
    
    tipo_eval = st.selectbox("Seleccione tipo de evaluación", ["","ragas", "ground-truth","llm", "todas"], key="evaluation_type")

    col3, col4 = st.columns([1, 1])
    
    with col3:
        if st.button("Ejecutar"):
            if tipo_eval != "":
                st.session_state.resultado = main_evaluador(tipo_eval)
                st.success(f"Evaluación completada con éxito.")
            else:
                st.warning("Por favor, selecciona un tipo de evaluación y presiona 'Ejecutar'.")

        if st.session_state.resultado: 
            conversaciones = []
            data_frames = pd.DataFrame()
            
            data_dir = Path("evaluation/results")
            
            for file in data_dir.glob("*.json"):
                with open(file, "r", encoding="utf-8") as f:
                    contenido = json.load(f)
                    conversaciones.append(contenido)
                    df = pd.DataFrame(contenido)
                    data_frames = pd.concat([data_frames, df], ignore_index=True)
            
            st.session_state.mostrar_resultados = True
        
    with col4:
        if st.button("Cargar resultados de evaluaciones anteriores"):
            conversaciones = []
            data_frames = pd.DataFrame()
            
            data_dir = Path("evaluation/results")
            
            for file in data_dir.glob("*.json"):
                with open(file, "r", encoding="utf-8") as f:
                    contenido = json.load(f)
                    conversaciones.append(contenido)
                    df = pd.DataFrame(contenido)
                    data_frames = pd.concat([data_frames, df], ignore_index=True)

            st.session_state.mostrar_resultados = True
    
    st.warning("Presiona Ejecutar si deseas realizar una nueva evaluación o Cargar resultados de evaluaciones anteriores si deseas ver los resultados de evaluaciones previas.")

    if st.session_state.mostrar_resultados:
        
        st.subheader("Resumen resultados evaluación")
        resumen = data_frames.copy()
        columnas_objetivo = ['match_score', 'faithfulness', 'answer_relevancy', 'context_precision','context_recall','evaluacion_llm']

        # Validar y crear columnas faltantes con NaN
        for col in columnas_objetivo:
            if col not in resumen.columns:
                resumen[col] = np.nan
                    
        resumen[['match_score', 'faithfulness', 'answer_relevancy', 'context_precision','context_recall','evaluacion_llm']] = resumen[['match_score', 'faithfulness', 'answer_relevancy', 'context_precision','context_recall','evaluacion_llm']].apply(pd.to_numeric, errors='coerce')
        resumen = resumen.groupby(['tipo_evaluacion','modelo']).agg({'match_score': 'mean', 'faithfulness': 'mean', 
                                                                         'answer_relevancy': 'mean','context_precision': 'mean',
                                                                         'context_recall': 'mean','evaluacion_llm': 'mean'}).reset_index()
        st.dataframe(resumen)
        
        st.subheader("Tabla detallada evaluación")
        st.dataframe(data_frames)
        excel_buffer = io.BytesIO()
        data_frames.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)  # Importante: regresar al inicio del buffer

        # Botón de descarga
        st.download_button(
            label="Descargar resultados en Excel",
            data=excel_buffer,
            file_name='resultados_evaluacion.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
            
            
        st.subheader("Json de la evaluación:")
        st.json(conversaciones)
        st.download_button(
            label="Descargar resultados en JSON",
            data=json.dumps(conversaciones, indent=2, ensure_ascii=False),
            file_name='resultados_evaluacion.json',
            mime='application/json'
        )

        st.session_state.mostrar_resultados = False

