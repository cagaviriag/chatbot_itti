
from evaluation.ground_truth_eval import evaluar_con_ground_truth
from evaluation.llm_eval import evaluar_con_llm
from evaluation.ragas_eval import evaluar_con_ragas
import streamlit as st


def main_evaluador(modo: str):
    if modo == "ground-truth":
        archivo, resultados = evaluar_con_ground_truth()
        st.success(f"Evaluacion Ground Truth completada ({len(resultados)} evaluaciones)")
        print(f"Archivo guardado: {archivo}")
        return True

    elif modo == "llm":
        archivo, resultados = evaluar_con_llm()
        st.success(f"Evaluacion LLM completada ({len(resultados)} evaluaciones)")
        print(f"Archivo guardado: {archivo}")
        return True

    elif modo == "ragas":
        results = evaluar_con_ragas()
        st.success(f"Evaluacion Ragas completada")
        return True

    elif modo == "todas":
        archivo1, res1 = evaluar_con_ground_truth()
        archivo2, res2 = evaluar_con_llm()
        results = evaluar_con_ragas()
        st.success(f"Evaluacion combinada completada")
        print(f"Ground Truth → {archivo1} ({len(res1)})")
        print(f"LLM Autoeval  → {archivo2} ({len(res2)})")
        print(f"Evaluacion Ragas")
        return True
    
    else:
        print("Modo no reconocido. Usa: ground-truth | llm | ragas |todas")
        return False
