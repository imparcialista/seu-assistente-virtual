import google.generativeai as genai

api_key = 'API_KEY_AQUI'

genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature"      : 0.7,
    "top_p"            : 0.95,
    "top_k"            : 64,
    "max_output_tokens": 65536,

    }

model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-thinking-exp-01-21",
        generation_config=generation_config,
        )

chat_session = model.start_chat(
        history=[
            ]
        )

response = chat_session.send_message("Sua mensagem aqui")

print(response.text)
