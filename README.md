# Control de Acceso Inteligente mediante Reconocimiento Facial

Este proyecto implementa un sistema de control de acceso mediante reconocimiento facial, basado en el uso de la cámara ESP32-CAM y comunicación con una API Django para la autenticación. Este sistema permite el control de acceso en instituciones educativas, capturando la imagen de los estudiantes y validando su identidad a través de una API de reconocimiento facial.

---

## Proyecto de IoT - Comunicación de Datos

**Alumnos:**
- Aloisio, Carolina
- Gimenez, Martiniano
- Mare, Fernando
- Quintero, Fabricio
- Viotti, Luca

---

## Introducción

### Propósito
El propósito de este proyecto es diseñar e implementar un sistema de control de acceso mediante reconocimiento facial, con el objetivo de optimizar la asistencia y seguridad en instituciones educativas.

### Alcance
Este sistema captura una imagen del estudiante al presionar un botón. La imagen es enviada a una API que valida si el estudiante tiene autorización para ingresar. Un LED RGB indica el estado de la autenticación (permitido, denegado, en proceso).

## Componentes

### Hardware Necesario
- Placa ESP32-CAM WIFI
- Protoboard de 400 puntos
- Botón pulsador touch de 3 pines
- Cable micro USB
- LED RGB de 5mm con 4 pines
- Cables PTB801 (22 cm, macho a hembra)
- Notebook

### Software Necesario
- Arduino IDE 2.3.3 para programar la ESP32-CAM: [Descargar](https://www.arduino.cc/en/software)
- Librería `esp32` de Espressif Systems
- Python y Django para ejecutar la API

## Repositorios

- **Repositorio ESP32-CAM:** [esp32_auth](https://github.com/FabriQuinteros/esp32_auth)
- **Repositorio API:** [facial_recognition](https://github.com/FabriQuinteros/facial_recognition)

## Configuración y Ejecución

### Requisitos Previos
Asegúrate de tener Python 3.x, pip y Django instalados para la API.

### Clona el Repositorio
Clona el repositorio de la API en tu máquina local:
```bash
git clone https://github.com/FabriQuinteros/facial_recognition.git
cd facial_recognition
```
### Instala las Dependencias
Si el repositorio tiene un archivo requirements.txt, instálalo con el siguiente comando:

``` bash
pip install -r requirements.txt
```

### Realiza las Migraciones
Ejecuta las migraciones para configurar la base de datos:

``` bash
python manage.py migrate
```

### Levanta el Servidor
Inicia el servidor de la API en el puerto 8000:

``` bash
python manage.py runserver 0.0.0.0:8000
```
El servidor de la API estará disponible en http://0.0.0.0:8000.


