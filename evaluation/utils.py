import json
from pathlib import Path
from collections import Counter
import re
import unicodedata

def cargar_conversaciones():
    conversaciones = []
    data_dir = Path("data/conversations")
    for file in data_dir.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            conversaciones.append(json.load(f))
    return conversaciones



def cargar_referencias(path="evaluation/reference_dataset.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)




def limpiar_respuesta(texto: str) -> str:
    # Normaliza (acentos, emojis, tildes)
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ASCII", "ignore").decode("utf-8")  # quita emojis y tildes
    texto = texto.replace("\\n", "\n")

    # Elimina saltos excesivos y espacios extra
    texto = re.sub(r"\n{2,}", "\n", texto)
    texto = re.sub(r"\s{2,}", " ", texto)

    # Remueve separadores y etiquetas decorativas
    texto = re.sub(r"\n*---+\n*", "\n", texto)
    texto = re.sub(r"\*\*(RESPUESTA|PREGUNTAS|FIN)\*\*", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\*\*Nota:.*?\n?", "", texto, flags=re.IGNORECASE)
    texto = texto.replace("*", "")

    # Elimina frases basura comunes y patrones decorativos
    frases = [
        "eso es todo", "buena suerte", "como agente virtual",
        "estoy aqui para ayudarte", "comienza a hacer preguntas",
        "en tu aventura", "hasta luego", "espero que hayas disfrutado",
        "soy tu agente", "¡", "!",

        # Regex adicionales
        r"¡Eso es todo!.*?experiencia",
        r"¡Buena suerte!.*?virtual",
        r"¡Hasta luego!?",
        r"Estoy aquí para ayudarte",
        r"¡Vamos a empezar!",
        r"Comienza a hacer preguntas",
        r"¿En qué puedo ayudarte\??",
        r"¿Hay algo más en lo que te pueda ayudar\??",
        r"\(Puedes hacer preguntas.*?\)",
        r"¡Buena suerte!?",
        r"¡!+",
        r"\*+\s?Nota:.*",
        r"¡Buena suerte en tu aventura como.*",
    ]
    for frase in frases:
        texto = re.sub(frase, "", texto, flags=re.IGNORECASE)

    # Fracciona en oraciones y filtra repeticiones
    oraciones = re.split(r'(?<=[.!?])\s+', texto)
    conteo = Counter(oraciones)
    oraciones_filtradas = [s for s in oraciones if conteo[s] <= 3]

    # Reconstruye y limpia final
    texto = " ".join(oraciones_filtradas)
    texto = re.sub(r"\s{2,}", " ", texto)

    return texto.strip()

