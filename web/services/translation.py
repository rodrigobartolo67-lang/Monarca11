import os

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


def translate_text(text: str, target_language: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return (
            "[MODO DEMO] Traducción no ejecutada porque falta OPENAI_API_KEY o la librería openai.\n\n"
            f"Destino solicitado: {target_language}\n\n"
            "Contenido original:\n"
            + text[:4000]
        )

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Eres un traductor jurídico experto. Mantén numeración, citas y formato legal.",
            },
            {
                "role": "user",
                "content": f"Traduce al idioma: {target_language}. Texto:\n\n{text[:30000]}",
            },
        ],
    )
    return response.output_text
