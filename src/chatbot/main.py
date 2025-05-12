import os
import unicodedata
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask import Flask, request
import torch

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "mi_token_unico_12345")
PHONE_ID     = "668397103018966"
WHATSAPP_API = f"https://graph.facebook.com/v13.0/{PHONE_ID}/messages"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "EAAS6ZAZCyHX2EBO4OtQxEXDj4yRM7CxlZBgWGtcoGjmpms6iFjlhgUZAqJNtXxnAzSShDwZActLXZBBzdJyuHAW5fmtcCSvzLiD8N98rDJU6E7AoHRCaOQa5SJvrl4inuQ0FaDUb2XBS045O64fP69qXjnADbpVLq3hQPo3v7A58Kr8TcX9CZCvZCQZDZD")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("./ssendago-2dbb8-firebase-adminsdk-fbsvc-0bfb2b2425.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Cargar modelo de Hugging Face
model_name = "csdavila/Llama-3.2.B.S2"
tokenizer  = AutoTokenizer.from_pretrained(model_name)
device     = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model      = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    low_cpu_mem_usage=True,
    torch_dtype=torch.float32
).to(device)


def obtener_contexto():
    return (
        "Eres un **asistente virtual** de un **e-commerce de vehículos de la marca Ssenda en Perú**. "
        "Estás capacitado para responder preguntas y brindar información detallada sobre nuestra **amplia gama de modelos**, "
        "incluyendo scooters, motos de paseo, motos urbanas, pisteras, naked, custom, todo terreno, así como mototaxis y trimotos/cargueros. "
        "Tu entrenamiento con ajuste fino (fine-tuning) te permite generar descripciones de productos, respuestas a clientes y contenido promocional relevante y culturalmente contextualizado para el mercado peruano. "
        "Puedes proporcionar información específica sobre: "
        "los **modelos disponibles** y sus **precios** en Soles peruanos (S/), "
        "las **especificaciones técnicas** como el motor (cilindrada en cc), encendido, sistema de frenos (disco delantero y tambor posterior) y suspensión (telescópica delantera y doble amortiguador posterior), "
        "los **colores disponibles** (azul y rojo), "
        "las **promociones vigentes** (por ejemplo, aceite, casco, linterna, polo camisero, cajuela, holder), "
        "los **medios de pago aceptados** (efectivo, transferencia bancaria, Yape, Plin, tarjeta de crédito física en tienda o por link de pago seguro), "
        "las **opciones de financiamiento**, incluyendo el **financiamiento directo con Cálidda** para titulares del servicio con crédito preaprobado de hasta S/ 5,000, y la **cuota inicial** que generalmente es del 30 por ciento del valor del vehículo, "
        "los **plazos y métodos de entrega** (48 horas hábiles en Lima Metropolitana, 3 días hábiles para provincias por agencia de transporte), "
        "y la posibilidad de **recojo el mismo día en tienda** en Av. Nicolás Ayllón 4671 - Ate, Lima, "
        "así como el **proceso y tiempo estimado para obtener la tarjeta de propiedad y placa** (realizado por Ssenda, aproximadamente 15 días hábiles desde la firma de documentos). "
        "Responde siempre de manera **amable, clara y servicial**, guiando al usuario en su experiencia de compra de vehículos Ssenda."
    )

def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return texto

def extraer_producto(mensaje):
    mensaje_norm = normalizar(mensaje)
    productos_ref = db.collection("productos").stream()

    for doc in productos_ref:
        nombre_producto = doc.to_dict().get("nombre")
        nombre_norm = normalizar(nombre_producto)

        if nombre_norm in mensaje_norm:
            return doc.id
    return None

def buscar_precio(producto):
    ref = db.collection("productos").document(producto)
    doc = ref.get()

    if doc.exists:
        # Obtiene los datos del producto
        data = doc.to_dict()
        producto = data.get("nombre")
        precio = data.get("precio")

        # Devuelve el precio del producto
        return f"Claro, lleva el {producto} a solo S/{precio}."
    else:
        return "Lo siento, no pude encontrar el precio solicitado."


def buscar_especificaciones(producto):
    ref = db.collection("productos").document(producto)
    doc = ref.get()

    if doc.exists:
        # Obtiene los datos del producto
        data = doc.to_dict()
        producto = data.get("nombre")
        especificaciones = data.get("especificaciones")

        # Devuelve las especificaciones del producto
        especificaciones_str = ", ".join(especificaciones) if especificaciones else "No se especificaron ingredientes."
        return f"Claro, el modelo {producto} tiene las siguientes especificaciones: {especificaciones_str}."
    else:
        return "Lo siento, no pude encontrar las especificaciones solicitadas."

def obtener_nombres_productos():
    productos_ref = db.collection("productos").stream()
    nombres = []

    for doc in productos_ref:
        data = doc.to_dict()
        nombre = data.get("nombre")
        if nombre:
            nombres.append(nombre)

    return nombres

def send_whatsapp_message(to: str, body: str) -> dict:
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type":  "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to":                to,
        "text":              {"body": body}
    }
    resp = requests.post(WHATSAPP_API, headers=headers, json=payload)
    try:
        return resp.json()
    except ValueError:
        return {"error": resp.text}


# ———————— FLASK APP ————————
app = Flask(__name__)

@app.route("/whatsapp", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode      = request.args.get("hub.mode")
        token     = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("Webhook verificado")
            return challenge, 200
        return "Token no coincide", 403

    data = request.get_json(force=True)
    try:
        msg_obj      = data["entry"][0]["changes"][0]["value"]["messages"][0]
        incoming_msg = msg_obj["text"]["body"]
        from_number  = msg_obj["from"]
    except Exception:
        return "OK", 200  # ignorar otros eventos

    print("Mensaje recibido:", incoming_msg)

    texto = incoming_msg.lower()

    if "precio" in incoming_msg or "cuanto cuesta" in incoming_msg or "costo" in incoming_msg:
        producto = extraer_producto(incoming_msg)
        if producto:
            respuesta = buscar_precio(producto)
            if not respuesta:
                respuesta = f"Lo siento, no encontré el precio del modelo '{producto}'."
        else:
            respuesta = "¿De qué modelo deseas saber el precio?"
    if "especificacion" in incoming_msg or "detalle" in incoming_msg or "caracteristica" in incoming_msg:
        producto = extraer_producto(incoming_msg)
        if producto:
            respuesta = buscar_especificaciones(producto)
            if not respuesta:
                respuesta = f"Lo siento, no encontré los detalles del modelo '{producto}'."
        else:
            respuesta = "¿De qué modelo deseas saber más?"
    if "envio" in incoming_msg or "stock" in incoming_msg or "venta" in incoming_msg:
      respuesta = (
        "Para ayudarte con mayor precisión, por favor indícame lo siguiente:\n"
        "- Modelo del producto\n"
        "- Dirección de entrega\n"
        "- Medio de pago (efectivo, tarjeta, Yape, etc.)"
      )
    if "catalogo" in incoming_msg or "modelo" in incoming_msg:
        productos = obtener_nombres_productos()
        respuesta = "Estos son nuestros modelos disponibles:\n"
        for producto in productos:
            respuesta += f"- {producto}\n"
    else:
        prompt = f"{obtener_contexto()}\nUsuario: {incoming_msg}\nAsistente:"
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        out    = model.generate(**inputs, max_new_tokens=100, do_sample=True, temperature=0.7)
        gen    = tokenizer.decode(out[0], skip_special_tokens=True)
        respuesta = gen.replace(prompt, "").strip()

    print("Respuesta generada:", respuesta)

    # Limpiar número y enviar respuesta
    to   = from_number.replace("whatsapp:", "").replace("+", "").strip()
    print("Enviando a:", to)
    resp = send_whatsapp_message(to, respuesta)
    print("WhatsApp API response:", resp)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)