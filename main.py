from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

messages =[
    {"role": "system", "content": "Eres Jarvis y tu creador es Jano"}
]

while True:

    user_input = input("Tú: ").strip()

    #Validaciones
    if not user_input:
        continue

    if user_input.lower() in ("salir", "exit", "bye", "chao pescao"):
        print("Chao pescao")
        break

    #Agregar nuestro mensaje al historial
    messages.append({"role": "user", "content": user_input})

    response = client.responses.create(
        model="gpt-5-nano",
        input=messages
    )

    assistant_reply = response.output_text
    messages.append({"role": "assistant", "content": assistant_reply})

    print(f"Asistente: {assistant_reply}")
    