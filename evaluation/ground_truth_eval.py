from evaluation.utils import cargar_conversaciones, cargar_referencias
from difflib import SequenceMatcher
import json
from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')


def comparar_respuesta_exacta(pregunta, respuesta_modelo, referencias):
    for ref in referencias:
        if ref["pregunta"].strip().lower() == pregunta.strip().lower():
            referencia = ref["respuesta_esperada"]
            score = SequenceMatcher(None, respuesta_modelo.lower(), referencia.lower()).ratio()
            return {
                "match_score": round(score, 3),
                "esperada": referencia,
                "respuesta": respuesta_modelo
            }
    return None



def comparar_respuesta_embedding(pregunta, respuesta_modelo, referencias, model, umbral=0.65):
    embedding_pregunta = model.encode(pregunta.strip().lower())

    mejor_score = 0
    mejor_referencia = None

    # Buscar la mejor coincidencia entre preguntas
    for ref in referencias:
        embedding_ref = model.encode(ref["pregunta"].strip().lower())
        score = util.cos_sim(embedding_pregunta, embedding_ref).item()

        if score > mejor_score:
            mejor_score = score
            mejor_referencia = ref

    # Si el mejor score supera el umbral, compara las respuestas
    if mejor_score >= umbral:
        embedding_respuestas = model.encode([
            respuesta_modelo.strip().lower(),
            mejor_referencia["respuesta_esperada"].strip().lower()
        ])
        score_respuesta = util.cos_sim(embedding_respuestas[0], embedding_respuestas[1]).item()

        return {
            "respuesta": respuesta_modelo,
            "match_score": round(score_respuesta, 3),
            "pregunta_comparada": mejor_referencia["pregunta"],
            "respuesta_esperada": mejor_referencia["respuesta_esperada"],
        }
    
    return None





def evaluar_con_ground_truth():
    referencias = cargar_referencias()
    conversaciones = cargar_conversaciones()
    resultados = []

    for conv in conversaciones:
        session_id = conv.get("session_id")
        modelo = conv.get("modelo")
        turns = conv.get("turns", [])
        for i in range(0, len(turns)):  # user → assistant
            if turns[i]["role"] == "user" and turns[i+1]["role"] == "assistant":
                pregunta = turns[i]["content"]
                respuesta = turns[i+1]["content"]
                comparacion = comparar_respuesta_embedding(pregunta, respuesta, referencias,model)
                if comparacion:
                    resultados.append({
                        "tipo_evaluacion": "ground_truth",
                        "session_id": session_id,
                        "modelo": modelo,
                        "pregunta": pregunta,
                        **comparacion
                    })

    output_dir = Path("evaluation/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "ground_truth_eval.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    return output_file, resultados
