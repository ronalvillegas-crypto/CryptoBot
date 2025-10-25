import requests
import time
import asyncio
from telegram import Bot
from telegram.constants import ParseMode

# --- CONFIGURACIÓN ---
TOKEN = "8446706346:AAHs8L2v2PkRTciwTEId-MhCoAQg6k8lQMs"
CHAT_ID = "1347933429"
bot = Bot(token=TOKEN)

# Parámetros de control
UMBRAL = 5          # Porcentaje mínimo de cambio para alertar (ej. ±5 %)
INTERVALO = 60 * 15 # Cada 15 minutos

def obtener_top100():
    """Obtiene las 100 criptomonedas más importantes por capitalización"""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "price_change_percentage": "24h"
    }
    return requests.get(url, params=params).json()

async def main():
    """Bucle principal del bot"""
    while True:
        monedas = obtener_top100()

        for m in monedas:
            nombre = m["name"]
            simbolo = m["symbol"].upper()
            precio = m["current_price"]
            cambio = m["price_change_percentage_24h"]

            if cambio and abs(cambio) >= UMBRAL:
                if cambio > 0:
                    mensaje = f"🚀 <b>{nombre}</b> ({simbolo}) ha subido +{cambio:.2f}% en 24 h — precio actual: ${precio}"
                else:
                    mensaje = f"🔻 <b>{nombre}</b> ({simbolo}) ha bajado {cambio:.2f}% en 24 h — precio actual: ${precio}"
                await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode=ParseMode.HTML)

        print("⏰ Revisión completada. Esperando el siguiente ciclo...")
        await asyncio.sleep(INTERVALO)

# --- EJECUCIÓN ---
if __name__ == "__main__":
    asyncio.run(main())
