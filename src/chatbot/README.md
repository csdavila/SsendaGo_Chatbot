# SsendaGo_Chatbot

# 🤖 Asistente Virtual para venta de vehículos vía WhatsApp

Este proyecto implementa un **asistente virtual inteligente** para un negocio de venta de vehículos que responde mensajes de WhatsApp en tiempo real. Utiliza **Flask**, **Firebase**, **transformers de Hugging Face** y la **API de WhatsApp Business**.

---

## 🚀 Características

- 🧠 Respuestas inteligentes usando un modelo de lenguaje (Llama).
- 📱 Integración completa con la API de WhatsApp.
- 🔎 Consulta de precios y especificaciones desde Firestore.
- 📝 Listado dinámico de los modelos.
- 🗣️ Interacción conversacional natural con los usuarios.
- 🔐 Token de acceso largo a la API de Meta (Facebook).

---

## 📦 Requisitos

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

requirements.txt:
flask
transformers
requests
bitsandbytes
firebase_admin
torch

## 🔧 Configuración
Clona el repositorio y entra en el directorio:

```bash
git clone https://github.com/csdavila/SsendaGo_Chatbot.git
cd SsendaGo_Chatbot
```

Agrega tu archivo de credenciales Firebase:

Coloca el archivo JSON de servicio de Firebase en la raíz del proyecto y nómbralo:
ssendago-2dbb8-firebase-adminsdk-fbsvc-0bfb2b2425.json

Configura las variables de entorno:

Crea un archivo .env (o exporta en el entorno):
VERIFY_TOKEN=mi_token_unico_12345
ACCESS_TOKEN=tu_token_de_acceso_largo

Modifica el modelo si es necesario:
model_name = "csdavila/Llama-3.2.B.S2"

## ▶️ Ejecución

```bash
python main.py
```

## 🌐 Webhook de WhatsApp
La ruta /whatsapp acepta dos métodos:

GET: para la verificación del webhook de Meta.

POST: para recibir y procesar mensajes entrantes.

## 💬 Funcionalidades del Asistente
Consultas disponibles:
Precio de un modelo:

"¿Cuánto cuesta el SS200ZH-AIRE?"

Ingredientes:

"¿Qué especificaciones tiene el XTRAIL-200?"

Ver menú:

"¿Qué modelos de vehículos tienen?"

Hacer pedido:

"Quiero comprar un CHACARERA 200"

Otras preguntas:

El modelo responderá usando IA si no se detecta una intención específica.


## 🧾 Licencia
Este proyecto es de uso libre con fines educativos o personales.
Para uso comercial, consulta los términos de la API de Meta y Hugging Face.