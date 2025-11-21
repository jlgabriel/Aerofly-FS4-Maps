# Aerofly FS4 Maps - Aircraft Tracker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

Un rastreador de aeronaves en tiempo real de código abierto para el simulador de vuelo **Aerofly FS4**. Visualiza la posición de tu aeronave en un mapa interactivo con información detallada de vuelo.

![Aircraft Tracker Demo](https://via.placeholder.com/800x400?text=Aircraft+Tracker+Demo)

## 🚀 Características

- **Recepción de datos UDP** desde Aerofly FS4 en tiempo real
- **Mapa interactivo** que muestra la posición de la aeronave
- **Información de vuelo en vivo**: latitud, longitud, altitud, velocidad sobre el suelo, rumbo, pitch y roll
- **Múltiples estilos de mapas**: OpenStreetMap, Google Maps (Normal, Satélite, Terreno, Híbrido), ESRI, CartoDB y más
- **Actualización en tiempo real** de la posición y orientación de la aeronave
- **Interfaz gráfica amigable** con Tkinter
- **Estado de conexión** visible para saber si está recibiendo datos del simulador
- **Icono de aeronave rotativo** que refleja el rumbo real del avión

## 📋 Requisitos Previos

- Python 3.7 o superior
- Aerofly FS4 Flight Simulator
- Sistema operativo: Windows, Linux o macOS

## 🔧 Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/jlgabriel/Aerofly-FS4-Maps.git
   cd Aerofly-FS4-Maps
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Asegúrate de tener el archivo de ícono de aeronave**:
   - El proyecto requiere un archivo `aircraft_icon.png` en el directorio raíz
   - Puedes crear o descargar un ícono de aeronave (32x32 píxeles recomendado)

## 🎮 Configuración de Aerofly FS4

Para que este tracker funcione, debes habilitar la transmisión UDP en Aerofly FS4:

1. Abre Aerofly FS4
2. Ve a **Settings** (Configuración)
3. Busca la opción de **UDP Output** o **Data Output**
4. Habilita el envío de datos GPS (XGPS) y actitud (XATT)
5. Configura el puerto UDP a **49002** (o modifica la constante `UDP_PORT` en el código)
6. Asegúrate de que los datos se envíen a `localhost` o `broadcast`

## 🚁 Uso

1. **Inicia Aerofly FS4** y carga un vuelo

2. **Ejecuta el tracker**:
   ```bash
   python aerofly_fs4_maps.py
   ```

3. **Interacción con la interfaz**:
   - El mapa mostrará automáticamente la posición de tu aeronave cuando detecte datos
   - Selecciona diferentes estilos de mapa desde el panel lateral
   - El panel de información muestra los datos de vuelo en tiempo real
   - El indicador de estado muestra "Connected" (verde) cuando recibe datos

4. **Cierra la aplicación**:
   - Haz clic en el botón "Close Map"
   - O cierra la ventana normalmente

## 📊 Datos Visualizados

El tracker muestra la siguiente información:

| Parámetro | Unidad | Descripción |
|-----------|--------|-------------|
| Latitude | Grados | Latitud actual |
| Longitude | Grados | Longitud actual |
| Altitude | Pies (ft) | Altitud sobre el nivel del mar |
| Ground Speed | Nudos (kts) | Velocidad respecto al suelo |
| True Heading | Grados | Rumbo verdadero |
| Pitch | Grados | Ángulo de cabeceo |
| Roll | Grados | Ángulo de alabeo |

## 🗺️ Mapas Disponibles

El tracker incluye 13 estilos de mapas diferentes:

- **OpenStreetMap** (estándar, DE, FR)
- **OpenTopoMap** (topográfico)
- **Google Maps** (Normal, Satélite, Terreno, Híbrido)
- **CartoDB** (Dark Matter, Positron)
- **ESRI** (World Imagery, Street Map, Topo Map)

## 🛠️ Estructura del Código

```
aerofly_fs4_maps.py
├── UDPReceiver          # Clase para recibir y parsear datos UDP
│   ├── start_receiving()
│   ├── _receive_data()
│   ├── _parse_gps_data()
│   └── _parse_attitude_data()
│
└── AircraftTrackerApp   # Clase principal de la aplicación GUI
    ├── setup_ui()
    ├── setup_aircraft_marker()
    ├── update_aircraft_position()
    ├── update_map_and_marker()
    └── update_info_display()
```

## 🔧 Configuración Avanzada

Puedes modificar las siguientes constantes en `aerofly_fs4_maps.py`:

```python
UDP_PORT = 49002              # Puerto UDP para recibir datos
WINDOW_SIZE = "1000x600"      # Tamaño de la ventana
MAP_SIZE = (800, 600)         # Tamaño del widget de mapa
UPDATE_INTERVAL = 100         # Intervalo de actualización (ms)
RECEIVE_TIMEOUT = 5.0         # Timeout de conexión (segundos)
```

## 🐛 Resolución de Problemas

### El tracker no muestra "Connected"
- Verifica que Aerofly FS4 esté enviando datos UDP en el puerto 49002
- Asegúrate de que el firewall no esté bloqueando el puerto
- Comprueba que la configuración de UDP en Aerofly FS4 esté habilitada

### Error: "aircraft_icon.png not found"
- Crea o descarga un archivo de ícono de aeronave (PNG)
- Colócalo en el directorio raíz del proyecto con el nombre `aircraft_icon.png`

### El mapa no se carga
- Verifica tu conexión a Internet (los tiles del mapa se descargan online)
- Algunos mapas pueden tener limitaciones de uso, prueba con otro estilo

## 📝 Versión

**Versión 25**: Agregado indicador de estado de conexión y manejo mejorado de errores para la recepción de datos UDP.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, lee [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles sobre nuestro código de conducta y el proceso para enviar pull requests.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Juan Luis Gabriel** - [@jlgabriel](https://github.com/jlgabriel)

## 🙏 Agradecimientos

- [IPACS](https://www.aerofly.com/) por crear Aerofly FS4 Flight Simulator
- [TkinterMapView](https://github.com/TomSchimansky/TkinterMapView) por el widget de mapas
- Comunidad de OpenStreetMap y otros proveedores de tiles

## ⚠️ Disclaimer

Este software no está afiliado, asociado, autorizado, respaldado por, ni en modo alguno oficialmente conectado con IPACS GbR, o cualquiera de sus filiales o afiliados. El nombre oficial "Aerofly FS4" así como los nombres, marcas, emblemas e imágenes relacionadas son marcas registradas de sus respectivos propietarios.

---

**¿Te gusta este proyecto?** Dale una ⭐ en GitHub y compártelo con la comunidad de simulación de vuelo.
