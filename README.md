# RenfeAutoFormalizer

Este proyecto automatiza el proceso de formalización y reserva de trenes en la página web de Renfe utilizando Selenium en Python. Está diseñado para facilitar la búsqueda y selección de un tren con una hora de salida específica, realizando múltiples intentos de búsqueda si es necesario.

## Descripción

El script se encarga de:
- Iniciar sesión en la página de Renfe con las credenciales proporcionadas.
- Manejar la verificación en dos pasos (2FA) si se solicita.
- Navegar a la página de formalización de viajes.
- Buscar un tren con una hora de salida específica y seleccionar el tren si está disponible.
- Intentar la reserva múltiples veces hasta encontrar disponibilidad o hasta que se alcancen los intentos máximos.

## Requisitos

- Python 3.x
- Google Chrome y el controlador ChromeDriver compatible con tu versión de Chrome
- Paquetes de Python: `selenium`, `python-dotenv`

## Instalación

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura el archivo `.env`**:
   Crea un archivo `.env` en el directorio del proyecto y añade tus credenciales:
   ```env
   RENFE_CORREO=tu_correo@ejemplo.com
   RENFE_CONTRASENA=tu_contrasena
   RENFE_ABONO_LOCALIZADOR=localizador
   ```

4. **Asegúrate de tener ChromeDriver instalado y accesible en tu PATH**.

## Uso

1. **Ejecuta el script**:
   ```bash
   python bot.py
   ```

2. **Configuración personalizada**:
   - `FECHA_FORMALIZACION`: La fecha del viaje que deseas formalizar, en formato `DD/MM/AAAA`.
   - `HORA_SALIDA_DESEADA`: La hora de salida del tren que deseas, en formato `HH.MM`.
   - `MAX_INTENTOS`: Número máximo de intentos para buscar el tren.
   - `ES_VUELTA`: Define si es el trayecto de vuelta (`True`) o de ida (`False`).

## Características

- **Inicio de sesión automatizado**: Usa credenciales almacenadas de forma segura en variables de entorno.
- **Gestión de verificación 2FA**: Solicita el código de verificación solo si es necesario.
- **Búsqueda iterativa**: Intenta múltiples veces hasta encontrar el tren deseado.
- **Selección de trayecto**: Configura si es el trayecto de ida o de vuelta con la variable `ES_VUELTA`.

## Advertencias

- **Uso responsable**: Este script automatiza interacciones con la página de Renfe y debe usarse de manera ética y en cumplimiento con las políticas de uso de Renfe.
- **Actualizaciones del sitio web**: La funcionalidad puede verse afectada si la estructura de la página de Renfe cambia. Revisa y actualiza los selectores si es necesario.
