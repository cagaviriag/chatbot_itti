from pathlib import Path



def load_prompt(prompt_name: str) -> str:
    path = Path(f"prompts/{prompt_name}.md")
    template_str = path.read_text(encoding="utf-8")

    if "{{contexto_productos}}" in template_str:
        contexto_path = Path("prompts/producto_contex_prompt.md")
        contexto_str = contexto_path.read_text(encoding="utf-8").strip()
        template_str = template_str.replace("{{contexto_productos}}", contexto_str)

    return template_str


def fill_prompt(template_str: str, values: dict) -> str:
    for key, val in values.items():
        template_str = template_str.replace(f"{{{{{key}}}}}", str(val))
    return template_str