from coree.prompt_manager import load_prompt, fill_prompt

# Cargar plantilla con placeholders
template = load_prompt("system_prompt")



def init_context(nombre_fintech):
    
    diccionario = {"nombre_fintech": nombre_fintech}

    # Rellenar valores dinámicamente
    prompt_final = fill_prompt(template,diccionario)
    
    return [{"role": "system", "content": prompt_final}]


