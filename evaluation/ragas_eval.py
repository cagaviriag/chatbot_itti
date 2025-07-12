from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset
from coree.prompt_manager import load_prompt
from evaluation.utils import cargar_conversaciones
from pathlib import Path
from datetime import datetime
import json
import pandas as pd
from ragas.metrics import faithfulness, answer_relevancy,context_precision, context_recall

def estructurar_conversacion_ragas():

    contexto_prompt  = load_prompt("producto_contex_prompt")
    conversaciones = cargar_conversaciones()
    
    muestras_turnos = []

    for conv in conversaciones:
        session_id = conv.get("session_id")
        modelo = conv.get("modelo")
        turnos = conv.get("turns", [])

        muestras = []
    
        for i in range(1, len(turnos) - 1, 2):
            if turnos[i]["role"] == "user" and turnos[i+1]["role"] == "assistant":
                muestras.append({
                    "session_id":session_id,
                    "modelo": modelo,
                    "question": turnos[i]["content"],
                    "answer": turnos[i+1]["content"],
                    "context": [contexto_prompt],
                    "retrieved_contexts": [contexto_prompt],
                    "reference": turnos[i+1]["content"],
                    
                })
        
        muestras_turnos.extend(muestras)
    
    dataset = Dataset.from_list(muestras_turnos)

    return dataset

import ragas
ragas.__version__

def evaluar_con_ragas():
    
    dataset = estructurar_conversacion_ragas()

    dataset_filtrado = dataset.remove_columns([
        col for col in dataset.column_names
        if col not in ["question", "answer", "context","retrieved_contexts","reference"]
        ])
    
    results = evaluate(dataset_filtrado,
                    metrics=[
                        faithfulness,
                        answer_relevancy,
                        context_precision,
                        context_recall
                        #correctness
                    ])
    
  
    scores_df = pd.DataFrame(results.scores)
    
    session_id = dataset["session_id"]
    modelo = dataset["modelo"]
    preguntas = dataset["question"]
    respuestas = dataset["answer"]

    # Convertir a DataFrame
    data = pd.DataFrame({
        "session_id": session_id,
        "modelo": modelo,
        "pregunta": preguntas,
        "respuesta": respuestas
    })

    resultados_completos = pd.concat([data, scores_df], axis=1)
    
    lista_resultados = []

    for _, row in resultados_completos.iterrows():
        resultado = {
            "tipo_evaluacion": "Ragas",
            "session_id": row["session_id"],
            "modelo": row["modelo"],
            "pregunta": row["pregunta"],
            "respuesta": row["respuesta"],
            "faithfulness":  row["faithfulness"],
            "answer_relevancy": row["answer_relevancy"],
            "context_precision": row["context_precision"],
            "context_recall": row["context_recall"],

        }
        lista_resultados.append(resultado)

    output_dir = Path("evaluation/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "ragas_eval.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(lista_resultados, f, indent=2, ensure_ascii=False)
    
    return results