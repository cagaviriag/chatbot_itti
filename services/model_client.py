import litellm

MODEL_ALIASES = {
    "claude-3.5-sonnet": "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
    "claude-opus": "bedrock/anthropic.claude-3-opus-20240229-v1:0",
    "claude-sonnet": "bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
    "claude-haiku": "bedrock/anthropic.claude-3-haiku-20240307-v1:0",
    "mistral-7b": "mistral.mistral-7b-instruct-v0:2",
    "titan-express": "bedrock/amazon.titan-text-express-v1",
    "titan-lite": "bedrock/amazon.titan-text-lite-v1",
    "llama3-70b": "bedrock/meta.llama3-70b-instruct-v1:0",
    "llama3-8b": "bedrock/meta.llama3-8b-instruct-v1:0",
}

def get_model_response(model_alias, context):
    real_model = MODEL_ALIASES.get(model_alias)
    if not real_model:
        return f"Alias de modelo inválido: '{model_alias}'", context

    try:
        response = litellm.completion(
            model=real_model,
            messages=context,
            temperature=0.28,
            top_p=0.6,
            max_tokens=400
        )
        result = response["choices"][0]["message"]["content"]
        context.append({"role": "assistant", "content": result})
        return result, context
    except Exception as e:
        error_msg = f"Error usando el modelo '{real_model}': {str(e)}"
        context.append({"role": "assistant", "content": error_msg})
        return error_msg, context
