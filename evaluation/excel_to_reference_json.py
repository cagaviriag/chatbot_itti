import pandas as pd
import json
from pathlib import Path

def excel_a_json(path_excel, path_salida="evaluation/reference_dataset.json"):
    
    df = pd.read_excel(path_excel)

    # Validar estructura esperada
    if not {'pregunta', 'respuesta_esperada'}.issubset(df.columns):
        raise ValueError("El Excel debe tener las columnas 'pregunta' y 'respuesta_esperada'.")

    # Eliminar filas vacías
    df = df.dropna(subset=["pregunta", "respuesta_esperada"])

    # Convertir a lista de diccionarios
    dataset = df.to_dict(orient="records")

    # Crear carpeta si no existe
    Path(path_salida).parent.mkdir(parents=True, exist_ok=True)

    # Guardar como JSON
    with open(path_salida, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"reference_dataset.json generado con {len(dataset)} entradas.")


if __name__ == "__main__":
    excel_a_json("data/reference_dataset.xlsx")
