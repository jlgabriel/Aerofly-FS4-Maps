# Contributing to Aerofly FS4 Maps

¡Gracias por tu interés en contribuir a Aerofly FS4 Maps! Este documento proporciona las pautas para contribuir al proyecto.

## 🌟 Cómo Contribuir

Hay muchas formas de contribuir a este proyecto:

- 🐛 Reportar bugs
- 💡 Sugerir nuevas características
- 📝 Mejorar la documentación
- 🔧 Enviar correcciones de código
- ✨ Implementar nuevas características

## 📋 Proceso de Contribución

### 1. Fork y Clone

1. Haz fork del repositorio
2. Clona tu fork localmente:
   ```bash
   git clone https://github.com/tu-usuario/Aerofly-FS4-Maps.git
   cd Aerofly-FS4-Maps
   ```

### 2. Crea una Rama

Crea una rama para tu contribución:

```bash
git checkout -b feature/nombre-de-tu-feature
# o
git checkout -b fix/nombre-del-bug
```

### 3. Realiza tus Cambios

- Escribe código limpio y bien documentado
- Sigue las convenciones de estilo de Python (PEP 8)
- Añade comentarios donde sea necesario
- Actualiza la documentación si es relevante

### 4. Commits

Usa mensajes de commit descriptivos:

```bash
git commit -m "Add: Nueva funcionalidad de zoom automático"
git commit -m "Fix: Corrección de error en el cálculo de rumbo"
git commit -m "Docs: Actualización de README con nuevas instrucciones"
```

Prefijos recomendados:
- `Add:` - Nueva funcionalidad
- `Fix:` - Corrección de bug
- `Update:` - Actualización de código existente
- `Docs:` - Cambios en documentación
- `Refactor:` - Refactorización de código
- `Test:` - Añadir o modificar tests
- `Style:` - Cambios de formato

### 5. Push y Pull Request

1. Push a tu fork:
   ```bash
   git push origin feature/nombre-de-tu-feature
   ```

2. Abre un Pull Request en GitHub
3. Describe claramente los cambios realizados
4. Referencia cualquier issue relacionado

## 🐛 Reportar Bugs

Si encuentras un bug, por favor abre un issue con:

- **Título descriptivo**
- **Descripción del problema**
- **Pasos para reproducir**
- **Comportamiento esperado**
- **Comportamiento actual**
- **Información del sistema**:
  - Sistema operativo
  - Versión de Python
  - Versión de Aerofly FS4
- **Capturas de pantalla** (si aplica)
- **Logs o mensajes de error**

### Plantilla de Bug Report

```markdown
**Descripción del Bug**
Una descripción clara y concisa del bug.

**Pasos para Reproducir**
1. Ve a '...'
2. Haz clic en '...'
3. Observa el error

**Comportamiento Esperado**
Lo que esperabas que sucediera.

**Capturas de Pantalla**
Si aplica, añade capturas de pantalla.

**Información del Sistema:**
 - OS: [e.g. Windows 10, Ubuntu 22.04]
 - Python Version: [e.g. 3.10.5]
 - Aerofly FS4 Version: [e.g. 1.0.0.0]
```

## 💡 Sugerir Características

Para sugerir nuevas características, abre un issue con:

- **Título claro**
- **Descripción detallada** de la característica
- **Caso de uso**: ¿Por qué es útil esta característica?
- **Mockups o ejemplos** (si aplica)

## 🔧 Guía de Estilo

### Python

- Sigue [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Usa 4 espacios para indentación
- Nombres de variables y funciones en `snake_case`
- Nombres de clases en `PascalCase`
- Constantes en `UPPER_CASE`
- Añade docstrings a clases y funciones

Ejemplo:

```python
class MyClass:
    """Brief description of the class.

    More detailed description if needed.
    """

    def my_method(self, param: str) -> int:
        """Brief description of the method.

        Args:
            param: Description of the parameter

        Returns:
            Description of the return value
        """
        pass
```

### Type Hints

Usa type hints cuando sea posible:

```python
from typing import Optional, Dict, List

def process_data(data: List[str]) -> Dict[str, int]:
    """Process the data and return a dictionary."""
    pass
```

### Comentarios

- Escribe comentarios claros y concisos
- Explica el "por qué", no el "qué"
- Mantén los comentarios actualizados

## 🧪 Testing

Si añades nueva funcionalidad:

- Considera añadir tests
- Asegúrate de que el código existente no se rompa
- Prueba con diferentes configuraciones

## 📝 Documentación

Si modificas la funcionalidad:

- Actualiza el README.md
- Actualiza los comentarios del código
- Actualiza los docstrings

## 🤝 Código de Conducta

### Nuestro Compromiso

Nos comprometemos a hacer que la participación en nuestro proyecto sea una experiencia libre de acoso para todos.

### Nuestros Estándares

**Comportamiento aceptable:**
- Usar lenguaje acogedor e inclusivo
- Respetar diferentes puntos de vista
- Aceptar críticas constructivas
- Enfocarse en lo mejor para la comunidad

**Comportamiento inaceptable:**
- Lenguaje o imágenes sexualizadas
- Trolling, comentarios insultantes
- Acoso público o privado
- Publicar información privada de otros

## ❓ Preguntas

Si tienes preguntas sobre cómo contribuir, puedes:

- Abrir un issue con la etiqueta "question"
- Contactar al mantenedor del proyecto

## 📜 Licencia

Al contribuir, aceptas que tus contribuciones serán licenciadas bajo la Licencia MIT del proyecto.

## 🙏 Reconocimientos

Todos los contribuidores serán reconocidos en el proyecto. ¡Gracias por tu contribución!

---

**¡Happy coding! ✈️**
