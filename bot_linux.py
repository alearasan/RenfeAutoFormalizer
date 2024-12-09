from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import logging
from webdriver_manager.chrome import ChromeDriverManager
 
# Configuración de datos
FECHA_FORMALIZACION = "10/12/2024"
HORA_SALIDA_DESEADA = "08.51"
URL_LOGIN = "https://venta.renfe.com/vol/loginParticular.do"
URL_FORMALIZACION = "https://venta.renfe.com/vol/myPassesCard.do?c=_zT4x"
MAX_INTENTOS = 1000
TIEMPO_ESPERA = 10
ES_VUELTA = False

# Configuración del entorno y opciones de navegador
logging.basicConfig(level=logging.WARNING)
load_dotenv()

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--log-level=3")
ruta_perfil = os.path.join(os.path.dirname(__file__), "perfil_sesion")
options.add_argument(f"user-data-dir={ruta_perfil}")

# Variables de entorno
correo = os.getenv("RENFE_CORREO", "")
contrasena = os.getenv("RENFE_CONTRASENA", "")
abono_localizador = os.getenv("RENFE_ABONO_LOCALIZADOR", "")

# Iniciar el navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL_LOGIN)

# Inicio de sesión
WebDriverWait(driver, TIEMPO_ESPERA).until(EC.presence_of_element_located((By.ID, "num_tarjeta"))).send_keys(correo)
driver.find_element(By.ID, "pass-login").send_keys(contrasena)
driver.find_element(By.ID, "pass-login").send_keys(Keys.RETURN)

# Verificación en dos pasos
try:
    codigo_2fa = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "codigoValidaLogin2F")))
    code = input("Ingresa el código de verificación enviado a tu dispositivo: ")
    codigo_2fa.send_keys(code)
    driver.find_element(By.ID, "idBotonValDispositivo").click()
    print("Verificación de dos pasos completada.")
except:
    print("No se requiere verificación de dos pasos.")

# Navegar a la página de formalización
driver.get(URL_FORMALIZACION)

# Nueva formalización
nueva_formalizacion_button = WebDriverWait(driver, TIEMPO_ESPERA).until(
    EC.element_to_be_clickable((By.ID, "new"+abono_localizador+"            "))
)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nueva_formalizacion_button)
driver.execute_script("arguments[0].click();", nueva_formalizacion_button)

# Formalización del viaje
if ES_VUELTA:
    journey_station_destin = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "journeyStationDestin"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", journey_station_destin)
    driver.execute_script("arguments[0].click();", journey_station_destin)

fecha_field = WebDriverWait(driver, TIEMPO_ESPERA).until(EC.presence_of_element_located((By.ID, "fecha1")))
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fecha_field)
fecha_field.clear()
fecha_field.send_keys(FECHA_FORMALIZACION)
print("Formalización del viaje completada.")

# Acceso a la vista de trenes
submitSiguiente = WebDriverWait(driver, TIEMPO_ESPERA).until(EC.element_to_be_clickable((By.ID, "submitSiguiente")))
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submitSiguiente)
driver.execute_script("arguments[0].click();", submitSiguiente)
print("Acceso vista trenes")

# Búsqueda del tren
intentos = 0
while intentos < MAX_INTENTOS:
    try:
        driver.refresh()
        WebDriverWait(driver, TIEMPO_ESPERA).until(EC.presence_of_element_located((By.ID, "listTrainsTableTbodyNEW")))
        filas = WebDriverWait(driver, TIEMPO_ESPERA).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody[@id='listTrainsTableTbodyNEW']/tr"))
        )
        time.sleep(3)
        tren_encontrado = False
        print(f"🔄 Intento {intentos + 1} de {MAX_INTENTOS} - Buscando tren a las {HORA_SALIDA_DESEADA} 🕒")

        for fila in filas:
            try:
                hora_salida = fila.find_element(By.XPATH, ".//td[@data-label='Salida']").text
                if hora_salida == HORA_SALIDA_DESEADA:
                    print("Misma hora encontrada")
                    boton_seleccionar = fila.find_element(By.XPATH, ".//button[contains(text(), 'Seleccionar')]")
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_seleccionar)
                    WebDriverWait(driver, TIEMPO_ESPERA).until(
                        EC.element_to_be_clickable((By.XPATH, ".//button[contains(text(), 'Seleccionar')]"))
                    )
                    driver.execute_script("arguments[0].click();", boton_seleccionar)
                    print(f"Tren de salida a las {HORA_SALIDA_DESEADA} seleccionado.")

                    submitSiguiente = WebDriverWait(driver, TIEMPO_ESPERA).until(
                        EC.element_to_be_clickable((By.ID, "submitSiguiente"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submitSiguiente)
                    driver.execute_script("arguments[0].click();", submitSiguiente)

                    try:
                        WebDriverWait(driver, TIEMPO_ESPERA).until(EC.visibility_of_element_located((By.ID, "myModalBody")))
                        print("Mensaje de error encontrado: No hay disponibilidad de plazas.")
                        driver.back()
                        break
                    except:
                        print("Reserva completada exitosamente sin mensajes de error.")
                        tren_encontrado = True
                        break
            except:
                None

        if tren_encontrado:
            break

        print("No se encontró el tren con la hora de salida especificada o el tren no está disponible. Reiniciando búsqueda...")
        intentos += 1

    except:
        continue

if intentos == MAX_INTENTOS:
    print("No se encontró el tren con la hora de salida especificada después de múltiples intentos.")
else:
    print("Tren encontrado y seleccionado exitosamente.")

driver.quit()
