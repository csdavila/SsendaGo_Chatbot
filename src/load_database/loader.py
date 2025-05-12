import json
import firebase_admin
from firebase_admin import credentials, firestore

# Ruta al archivo de credenciales de Firebase
firebase_key_path = 'ssendago-2dbb8-firebase-adminsdk-fbsvc-0bfb2b2425.json'

# Inicializa la app de Firebase
cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred)

# Obtiene una instancia de Firestore
db = firestore.client()

# Lee los datos del archivo JSON
with open('data/productos_vehiculos.json', 'r', encoding='utf-8') as f:
    productos = json.load(f)

# Sube los productos a la colección "productos"
for producto in productos:
    # Puedes usar producto['id'] como ID del documento si está disponible
    doc_ref = db.collection('productos').document()
    doc_ref.set(producto)

print("✅ Productos cargados exitosamente en Firestore.")
