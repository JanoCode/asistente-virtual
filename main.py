from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from agent import Agent

load_dotenv()

client = OpenAI()
agent = Agent()

while True:

    user_input = input("Tú: ").strip()

    #Validaciones
    if not user_input:
        continue

    if user_input.lower() in ("salir", "exit", "bye", "chao pescao"):
        print("Chao pescao")
        break

    #Agregar nuestro mensaje al historial
    agent.messages.append({"role": "user", "content": user_input})

    while True:
        response = client.responses.create(
            model="gpt-5-nano",
            input=agent.messages,
            tools=agent.tools
        )

        called_tool = agent.process_response(response)

        #si no se llamo herramienta, tenemos la respuesta final
        if not called_tool:
            break