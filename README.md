# Cómo crear un Bot de descarga de TikTok en Python 🎥

Este repositorio es una guía práctica para construir tu propio bot de Telegram capaz de descargar videos de TikTok de forma automática.

## ¿Qué se utiliza?

Para que este proyecto funcione de manera estable y eficiente, utilizamos dos herramientas principales:

1.  **python-telegram-bot**: La librería estándar para interactuar con la API de Telegram de forma asíncrona.
2.  **yt-dlp**: Un fork potente de youtube-dl que se mantiene actualizado constantemente para soportar los cambios en los algoritmos de TikTok y otras plataformas.

## Estructura del Proyecto

El bot funciona siguiendo este flujo simple:
1.  **Escucha**: El bot recibe un mensaje de texto del usuario.
2.  **Validación**: Comprueba si el texto contiene un enlace de TikTok.
3.  **Descarga**: Utiliza `yt-dlp` para descargar el video en la mejor calidad disponible al servidor local.
4.  **Entrega**: Envía el archivo `.mp4` resultante a través del chat de Telegram.
5.  **Limpieza**: Borra el archivo temporal del servidor para no agotar el espacio.

## Cómo empezar

### 1. Variables de entorno
El código busca una variable llamada `TELEGRAM_TOKEN`. Puedes configurarla en tu terminal o sistema antes de ejecutar el bot:

```bash
export TELEGRAM_TOKEN="tu_token_aqui"
```

### 2. Instalación de dependencias
Asegúrate de tener Python instalado y ejecuta:

```bash
pip install -r requirements.txt
```

### 3. Ejecución
```bash
python main.py
```

## Ejemplos de uso de yt-dlp

La potencia de este bot reside en cómo configuramos `yt-dlp`. Aquí tienes algunos ejemplos de configuraciones comunes:

### Configuración básica (la usada en el bot)
```python
ydl_opts = {
    'format': 'best',           # Descarga la mejor calidad disponible
    'outtmpl': 'video.mp4',     # Nombre del archivo de salida
    'quiet': True,              # No muestra logs innecesarios
}
```

### Descargar solo el audio (MP3)
Si quisieras transformar el bot en un descargador de música:
```python
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'audio.mp3',
}
```

### Extraer información sin descargar
Útil para mostrar el título o la duración antes de enviar el video:
```python
with yt_dlp.YoutubeDL({}) as ydl:
    info = ydl.extract_info(url, download=False)
    titulo = info.get('title', 'Sin título')
    duracion = info.get('duration', 0)
```

## Consideraciones importantes

- **Marcas de agua**: Por defecto, la descarga incluye los metadatos y el formato que la plataforma entrega. Para versiones más avanzadas (sin marca de agua), se suelen usar APIs de terceros o scripts específicos que analizan el JSON de la respuesta de TikTok.
- **Renderizado**: En algunos casos, si el video es muy pesado, Telegram puede tardar en procesar la vista previa.
- **Seguridad**: Asegúrate de manejar los errores de descarga (excepciones) para que el bot no se detenga si un enlace está roto o es privado.
