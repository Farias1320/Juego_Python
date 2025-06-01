# Documentación del Videojuego

## Nombres

Cristopher Alexander Farias Ruiz  
Alejandro Oswaldo Leon Tello

---

## Especificaciones Técnicas

- **Lenguaje:** Python 3
- **Librerías principales:** pygame, opencv, mediapipe
- **Resolución recomendada:** 800x600
- **Carpeta de recursos:** sprites/

---

## Requisitos previos

- Python 3 instalado.
- Instalar dependencias con:
  ```
  pip install pygame opencv-python mediapipe
  ```
- Cámara web funcional para el control por movimiento de cabeza y disparo.

## ¿Cómo jugar?

### 1. Iniciar el juego

- Ejecuta el archivo `app.py`.
- Aparecerá la pantalla de inicio.  
  **No cierres la ventana mientras el juego está en curso.**

### 2. Selección de nivel

- Usa el mouse o las teclas indicadas para seleccionar el nivel que deseas jugar.

### 3. Controles durante el juego

- **Mover la nave:** Mueve tu cabeza de izquierda a derecha frente a la cámara (o usa las teclas si está habilitado).
- **Disparar:** Debes juntar los dedos pulgar e indice (mostrandolos hacia la camará) para disparar láseres.
- **Salir del juego:** Presiona `ESC` en cualquier momento para salir.

### 4. Objetivo

- **Sobrevive** el mayor tiempo posible y destruye los meteoritos con tus disparos.
- Gana puntos por cada meteorito esquivado o destruido.
- El juego termina cuando pierdes todas tus vidas o alcanzas la puntuación objetivo del nivel.

---

## Funcionamiento

- Los meteoritos caen desde la parte superior de la pantalla.
- Debes esquivarlos o destruirlos con tus disparos.
- Tienes un número limitado de vidas (3 por defecto).
- Si un meteorito toca tu nave, pierdes una vida.
- Cuando pierdes todas las vidas, la nave explota y el juego termina.

---

## Advertencias y recomendaciones

- **No cierres la ventana del juego** usando el botón de cerrar mientras está en curso; usa `ESC` para salir correctamente.
- **No pulses teclas al azar** durante la selección de nivel o el menú, ya que podrías saltar opciones importantes.
- **No muevas la carpeta `sprites`** ni borres archivos de sonido o imagen, ya que el juego depende de ellos.
- **No desconectes la cámara** si usas control por movimiento de cabeza, ya que el juego podría dejar de funcionar correctamente.

---

## Créditos

- Programación y diseño: Cristopher Alexander Farias Ruiz, Alejandro Oswaldo Leon Tello
- Recursos gráficos y de sonido: Use recursos de un gitlab ya creado (https://gitlab.com/tecnoprofe/python/-/tree/master/pygame) para los sonidos y ciertos gráficos

---

## Notas adicionales

- Si tienes problemas con el sonido, asegúrate de que tu dispositivo de audio esté correctamente configurado.
- Para agregar nuevos niveles o modificar la dificultad, edita el archivo `levels.py`.
- Si quieres cambiar los controles, revisa el archivo `game.py`.

---

¡Disfruta el juego!
