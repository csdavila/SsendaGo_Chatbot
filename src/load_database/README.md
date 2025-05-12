# 🚀 Cargar Productos a Firebase Firestore

Este proyecto permite cargar un archivo JSON con datos de productos a una base de datos Firestore en Firebase usando Python.

## 📁 Estructura esperada

- `productos.json`: Archivo que contiene los productos en formato JSON.
- `clave-firebase.json`: Archivo de credenciales de Firebase (clave privada del servicio).
- `loader.py`: Script Python para cargar los datos.

## 🛠 Requisitos

- Python 3.6 o superior
- Cuenta y proyecto en [Firebase](https://console.firebase.google.com/)
- Base de datos **Firestore** habilitada
- Archivo de clave privada descargado desde Firebase Console

### 📦 Instalar dependencias

```bash
pip install firebase-admin
```

### ⚙️ Configuración
Descarga tu archivo de clave de servicio desde Firebase:

Ve a Configuración del proyecto > Cuentas de servicio.

Haz clic en "Generar nueva clave privada".

Guarda el archivo como clave-firebase.json o como prefieras.

Asegúrate de tener un archivo productos.json con los datos que quieres cargar. Ejemplo de formato:

```bash
[
    {
        "nombre": "GOL 125",
        "descripcion": "La GOL 125 es una motocicleta tipo scooters de 125cc, ideal para uso urbano y mixto.",
        "especificaciones": [
            "Motor 125cc monocilíndrico",
            "Encendido eléctrico y a pedal",
            "Sistema de frenos: disco delantero y tambor posterior",
            "Suspensión telescópica delantera y doble amortiguador posterior",
            "Colores disponibles: azul y rojo"
        ],
        "precio": 4490.0,
        "disponibilidad": true
    },
    {
        "nombre": "LEO 110 N V2",
        "descripcion": "La LEO 110 N V2 es una motocicleta tipo motos paseo de 110cc, ideal para uso urbano y mixto.",
        "especificaciones": [
            "Motor 110cc monocilíndrico",
            "Encendido eléctrico y a pedal",
            "Sistema de frenos: disco delantero y tambor posterior",
            "Suspensión telescópica delantera y doble amortiguador posterior",
            "Colores disponibles: azul y rojo"
        ],
        "precio": 3690.0,
        "disponibilidad": true
    },
]
```

### 🚀 Ejecución
Edita el archivo loader.py y asegúrate de que las rutas al JSON y la clave sean correctas. Luego, ejecuta:


```bash
python loader.py
```


### 📌 Notas
Si deseas usar el campo "id" como ID del documento en Firestore, modifica esta línea:

```bash
doc_ref = db.collection('productos').document(str(producto['id']))
```

Esto evitará duplicados si vuelves a ejecutar el script.

### 📬 Soporte
Si tienes dudas, errores o necesitas adaptar este script a otro formato, no dudes en pedir ayuda.