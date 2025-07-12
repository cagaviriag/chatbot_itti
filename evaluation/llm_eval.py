from coree.prompt_manager import load_prompt
from services.model_client import get_model_response
from evaluation.utils import cargar_conversaciones,limpiar_respuesta
import json
from pathlib import Path
from datetime import datetime
import re

def evaluar_con_turno(pregunta, respuesta, modelo="claude-3.5-sonnet"):
    template = load_prompt("evalua_respuesta")
    prompt = f"""Pregunta: 
                {pregunta}.
                Respuesta del asistente: 
                {respuesta}"""

    messages = [{"role": "system", "content": template}]
    messages.append({"role": "user", "content": prompt})
    evaluacion, _ = get_model_response(modelo, messages)
    return evaluacion


def evaluar_con_llm(modelo_eval="claude-3.5-sonnet"):
    conversaciones = cargar_conversaciones()
    
    resultados = []

    for conv in conversaciones:
        session_id = conv.get("session_id")
        modelo = conv.get("modelo")
        turns = conv.get("turns", [])
        for i in range(1, len(turns)):
            if turns[i]["role"] == "user" and turns[i+1]["role"] == "assistant":
                pregunta = turns[i]["content"]
                respuesta = turns[i+1]["content"]
                #respuesta = limpiar_respuesta(respuesta)
                evaluacion = evaluar_con_turno(pregunta, respuesta, modelo_eval)
                evaluacion = evaluacion.replace("\\n", "\n")
                evaluacion = evaluacion.split("\n", 1)
                if len(evaluacion) < 2:
                    evaluacion.append('')
   
                resultados.append({
                    "tipo_evaluacion": "llm",
                    "session_id": session_id,
                    "modelo": modelo,
                    "pregunta": pregunta,
                    "respuesta": respuesta,
                    "evaluacion_llm": evaluacion[0].split(":", 1)[-1].strip(),
                    "justificacion_llm": evaluacion[1].replace("justificacion:", "", 1).strip()
                })

    output_dir = Path("evaluation/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "llm_eval.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    return output_file, resultados

