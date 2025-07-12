# 🧠 - Chatbot GenAI para Fintech + Módulo de Evaluación

**Chatbot** es una solución completa basada en IA generativa diseñada para asistir a usuarios de una **fintech** en temas relacionados con **tarjetas de débito**, **tarjetas de crédito** y **préstamos personales**. El proyecto incluye:

- Una interfaz conversacional (frontend con Streamlit)
- Una interfaz para la evaluación automática de la calidad de las respuestas (Ragas, ground-truth y LLM)
- Un motor de prompts estructurado
- Almacenamiento de conversaciones y resultados de las evaluaciones de los modelos


---

## 🧭 Estructura del proyecto

```
ITTI/
├── app.py                        # Interfaz principal con Streamlit para flujo conversacional y evaluación automática
├── coree/
│   ├── prompt_manager.py         # Carga y rellenado de prompts .md
├── services/
│   ├── model_client.py           # Cliente para invocar modelos LLM
├── prompts/
│   ├── system_prompt.md
│   ├── producto_contex_prompt.md
│   ├── evalua_respuesta.md
├── data/
│   ├── conversations/            # Conversaciones guardadas (.json)
│   └── reference_dataset.xlsx
├── evaluation/
│   ├── evaluator.py              # Orquestador para evaluación se llama desde app.py
│   ├── ground_truth_eval.py
│   ├── llm_eval.py
│   ├── ragas_eval.py
│   ├── utils.py
│   ├── results/
│   └── excel_to_reference_json.py
├── entregables/                # Entregables solicitado en la prueba, pdf, word, etc
└── requirements.txt
```

---

## 🚀 ¿Qué hace este proyecto?

| Módulo | Funcionalidad |
|--------|----------------|
| 💬 `app.py` | Frontend conversacional con Streamlit y modulo de evaluacion de las interaciones |
| 📦 `prompt_manager.py` | Manejo modular de prompts `.md` con placeholders |
| 🧠 `model_client.py` | Interfaz para enviar prompts al LLM seleccionado |
| 🗃️ `data/conversations/` | Guarda cada conversación como un `.json` estructurado |
| 📊 `evaluation/` | Contiene toda la lógica de evaluación del chatbot |
| 📑 `reference_dataset.xlsx` | Base editable (ground-truth) de preguntas y respuestas |
| 🔁 `excel_to_reference_json.py` | Convierte el Excel en un JSON estructurado para evaluar |
| ✅ `evaluator.py` | Orquesta las evaluaciones (ground-truth, LLM o Ragas) |

---

## 🛠️ Requisitos

Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

---

## 🔐 Variables de Entorno

Para garantizar la **reproducibilidad**, debes crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
AWS_REGION_NAME=your-region
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_SESSION_TOKEN=your-session-token
OPENAI_API_KEY=your-openai-key


---

## 💻 Cómo ejecutar la app conversacional o evaluación de modelos

```bash
streamlit run app.py
```

---

## 📥 ¿Cómo se guardan las conversaciones?

Cada interacción se guarda automáticamente al hacer clic en el botón `Finalizar chat` dentro de `app.py`. Esto genera un archivo `.json` dentro de:

```
data/conversations/
```

Con estructura estándar:

```json
{
  "timestamp": "...",
  "session_id": "...",
  "modelo": "...",
  "turns": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

---

## ✅ Evaluación de las conversaciones

### 1. Preparar el dataset de ground-truth

Edita `data/reference_dataset.xlsx` con columnas:

- `pregunta`
- `respuesta_esperada`

Luego, conviértelo a JSON:

```bash
python evaluation/excel_to_reference_json.py
```

Esto generará: `evaluation/reference_dataset.json`

---

### 2. Ejecutar evaluación, la evaluacion se puede realizar por Ragas, ground-truth, evaluacion de otro llm, o las 3 juntas.

```bash
# Evaluación comparando con respuestas esperadas
python app.py  ## en el front desde la pestaña de evaluacion de modelos

```

Los resultados se guardan en:

```
evaluation/results/
```

---

## 📊 Resultados generados

Cada evaluación produce un archivo `.json` con métricas como:

- `tipo_eval`,`session_id`,`respuesta`, `esperada`, `pregunta`
- `match_score` (ground-truth)
- `evaluacion_llm` (opinión estructurada de otro modelo)
- `faithfulness` y  `answer_relevancy` (Ragas)


Estos archivos pueden usarse para visualizaciones, dashboards o retroalimentación al equipo de producto.

---

## 🧠 Estilo del asistente (prompting)

El agente sigue principios de:
- Claridad, precisión y empatía
- Razonamiento tipo CoT ("Primero… Luego… Finalmente…")
- Few-shot prompting con ejemplos conversacionales
- No responde fuera del dominio financiero
- Usa placeholders como `{{nombre_fintech}}` para inyección dinámica y `{{contexto_productos}}` para agregar la informacion de los productos.

---

## 📌 Notas adicionales

- Puedes personalizar los prompts en la carpeta `/prompts`
- Puedes extender el evaluador para incluir anotación humana, RAG

---

## 🧑‍💻 Autor / Mantenimiento

Este repositorio fue diseñado para servir como base sólida para asistentes conversacionales financieros evaluables en entornos reales por Cristian Gaviria