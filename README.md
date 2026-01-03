# 🖼️ Background Remover

Una aplicación de escritorio moderna y elegante para eliminar fondos de imágenes de forma rápida y sencilla, desarrollada con Python y Flet.

![Background Remover](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Características

- 🎨 **Interfaz moderna**: Diseño intuitivo con tema oscuro y colores vibrantes
- 📁 **Procesamiento por lotes**: Procesa múltiples imágenes simultáneamente
- 🎯 **Formatos soportados**: PNG, JPG, JPEG, BMP, WEBP
- 📂 **Carpeta personalizable**: Elige dónde guardar tus imágenes procesadas
- 📊 **Barra de progreso**: Visualiza el estado del procesamiento en tiempo real
- 🔄 **Organización automática**: Las imágenes se guardan con timestamp y estructura organizada

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/background-remover.git
cd background-remover
```

2. Crea un entorno virtual (recomendado):
```bash
python -m venv venv
```

3. Activa el entorno virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instala las dependencias:
```bash
pip install flet rembg pillow
```

## 💻 Uso

1. Ejecuta la aplicación:
```bash
python Remover_Ui.py
```

2. **Configura la carpeta de salida**:
   - Marca "Usar carpeta por defecto" para guardar en `Carpeta_Defecto/`
   - O ingresa una ruta personalizada

3. **Selecciona imágenes**:
   - Haz clic en "Seleccionar Imagenes"
   - Elige una o varias imágenes

4. **Procesa**:
   - Haz clic en "Remover fondo"
   - Observa el progreso en tiempo real

## 📁 Estructura del Proyecto

```
Background Remover/
├── background_remover.py    # Lógica de procesamiento de imágenes
├── Remover_Ui.py            # Interfaz gráfica con Flet
├── .gitignore               # Archivos ignorados por Git
├── README.md                # Este archivo
└── Carpeta_Defecto/         # Carpeta de salida por defecto
```

## 🛠️ Tecnologías Utilizadas

- **[Flet](https://flet.dev/)**: Framework para crear interfaces gráficas multiplataforma
- **[rembg](https://github.com/danielgatis/rembg)**: Librería para remover fondos con AI
- **[Pillow](https://python-pillow.org/)**: Procesamiento de imágenes en Python

## 📝 Notas

- Las imágenes procesadas se guardan con un timestamp único
- Se mantienen las imágenes originales en una subcarpeta
- Las imágenes procesadas se guardan en formato PNG con transparencia

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Haz commit de tus cambios (`git commit -m 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Autor

**Alexis**

---

⭐ Si te gustó este proyecto, dale una estrella en GitHub!
