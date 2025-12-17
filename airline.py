from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
import gradio as gr
import sqlite3
import traceback


load_dotenv(override=True)

MODEL = "gpt-4.1-mini"

instructions = "Eres un asistente útil para una aerolínea llamada FlightAI. "
instructions += "Usa tus herramientas para obtener precios de boletos y calcular descuentos. Los viajes a Londres tienen un 10% de descuento en el precio. "
instructions += "Sé siempre preciso. Si no sabes la respuesta, dilo."

DB = "prices.db"
initial_ticket_prices = {"london": 799, "paris": 899, "tokyo": 1400, "sydney": 2999}


with sqlite3.connect(DB) as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS prices (city TEXT PRIMARY KEY, price REAL)")
    for city, price in initial_ticket_prices.items():
        cursor.execute(f"INSERT OR IGNORE INTO prices (city, price) VALUES ('{city}', {price})")
    conn.commit()


@function_tool
def get_ticket_price(city: str) -> str:
    """Obtiene el precio de un boleto a una ciudad dada.

    Args:
        city: La ciudad a la que se desea obtener el precio del boleto
    """
    print(f"HERRAMIENTA INVOCADA: Obteniendo precio para {city}", flush=True)
    query = f"SELECT price FROM prices WHERE city = '{city.lower()}'"
    try:
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            return f"${result[0]}" if result else "No encontrado"
    except Exception as e:
        return f"Error: {traceback.format_exc()}"


@function_tool
def calculate(expr: str) -> str:
    """Evalúa una expresión numérica - usa esto, por ejemplo, para hacer cálculos sobre precios

    Args:
        expr: La expresión a evaluar
    """
    print(f"HERRAMIENTA INVOCADA: Calculando {expr}", flush=True)
    return str(eval(expr))


async def chat(message, history):
    messages = [{"role": m["role"], "content": m["content"]} for m in history]
    messages += [{"role": "user", "content": message}]
    agent = Agent(
        name="FlightAI", instructions=instructions, model=MODEL, tools=[get_ticket_price, calculate]
    )
    result = await Runner.run(agent, messages)
    return result.final_output


gr.ChatInterface(chat, type="messages").launch(inbrowser=True)
