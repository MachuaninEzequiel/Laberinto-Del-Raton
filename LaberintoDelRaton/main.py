import random
import tkinter as tk
from tkinter import messagebox
import time

# Definir el tamaño del laberinto
ancho = 10
alto = 10

# Lista de movimientos válidos
movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Posición inicial del robot (siempre la esquina inferior izquierda)
x_robot = 0
y_robot = alto - 1

# Posición objetivo (inicialmente será una celda aleatoria)
x_objetivo = random.randint(0, ancho - 1)
y_objetivo = random.randint(0, alto - 1)

# Crear el laberinto como una matriz
laberinto = None

# Tiempo inicial y contador de pasos
tiempo_inicial = None
pasos = 0

# Función para generar un laberinto utilizando el algoritmo de Prim
def generar_laberinto():
    global laberinto

    # Inicializar todas las celdas como paredes
    laberinto = [[1 for _ in range(ancho)] for _ in range(alto)]

    # Establecer la posición inicial del robot como un pasaje
    laberinto[y_robot][x_robot] = 2

    # Establecer la posición objetivo como un pasaje
    laberinto[y_objetivo][x_objetivo] = 2

    # Lista de celdas visitadas
    visitadas = [(x_robot, y_robot), (x_objetivo, y_objetivo)]

    # Mientras haya celdas sin visitar
    while visitadas:
        # Elegir una celda aleatoria de las celdas visitadas
        x, y = random.choice(visitadas)

        # Lista de celdas vecinas no visitadas
        vecinos_no_visitados = []

        # Verificar celdas vecinas no visitadas
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x_nuevo = x + dx
            y_nuevo = y + dy
            if 0 <= x_nuevo < ancho and 0 <= y_nuevo < alto and laberinto[y_nuevo][x_nuevo] == 1:
                vecinos_no_visitados.append((x_nuevo, y_nuevo))

        # Si hay celdas vecinas no visitadas
        if vecinos_no_visitados:
            # Elegir una celda vecina aleatoria
            x_vecino, y_vecino = random.choice(vecinos_no_visitados)

            # Hacer un pasaje entre la celda actual y la celda vecina
            laberinto[y][x] = 0
            laberinto[y_vecino][x_vecino] = 0

            # Agregar la celda vecina a la lista de celdas visitadas
            visitadas.append((x_vecino, y_vecino))

        # Eliminar la celda actual de la lista de celdas visitadas
        visitadas.remove((x, y))

# Función para dibujar el laberinto
def dibujar_laberinto(canvas):
    for i in range(alto):
        for j in range(ancho):
            if laberinto[i][j] == 1:
                canvas.create_line(j * 40, i * 40, (j + 1) * 40, (i + 1) * 40, dash=(4, 2))
            elif laberinto[i][j] == 2:
                canvas.create_rectangle(j * 40, i * 40, (j + 1) * 40, (i + 1) * 40, fill="green")
            else:
                canvas.create_rectangle(j * 40, i * 40, (j + 1) * 40, (i + 1) * 40, fill="white")

# Función para rellenar la casilla objetivo con color verde
def pintar_objetivo(canvas):
    canvas.create_rectangle(x_objetivo * 40, y_objetivo * 40, (x_objetivo + 1) * 40, (y_objetivo + 1) * 40, fill="green")

# Función para rellenar las paredes recorridas
def rellenar_pared(canvas, x, y, direccion):
    canvas.create_rectangle(x * 40, y * 40, (x + 1) * 40, (y + 1) * 40, fill="black")

# Función para mover el robot
def mover_robot(direccion, canvas, ventana):
    global x_robot, y_robot, pasos

    dx, dy = movimientos[direccion]
    x_nuevo = x_robot + dx
    y_nuevo = y_robot + dy

    if 0 <= x_nuevo < ancho and 0 <= y_nuevo < alto and laberinto[y_nuevo][x_nuevo] == 0:
        x_robot = x_nuevo
        y_robot = y_nuevo

        # Rellenar la pared recorrida
        rellenar_pared(canvas, x_robot - dx, y_robot - dy, direccion)

        # Actualizar la posición del robot en el lienzo
        canvas.move(robot, 40 * dx, 40 * dy)

        # Refrescar el lienzo
        ventana.update()

        # Incrementar contador de pasos
        pasos += 1

        # Verificar si el robot llegó al objetivo
        if x_robot == x_objetivo and y_robot == y_objetivo:
            # Calcular tiempo transcurrido
            tiempo_transcurrido = time.time() - tiempo_inicial

            # Mostrar un mensaje con el tiempo y los pasos
            messagebox.showinfo("¡Felicidades!", f"El robot llegó al objetivo en {tiempo_transcurrido:.2f} segundos con {pasos} pasos.")

            # Detener el movimiento
            detener_movimiento()

# Función para iniciar el movimiento del robot
def iniciar_movimiento():
    global robot_moviendose, tiempo_inicial, pasos
    robot_moviendose = True
    tiempo_inicial = time.time()
    pasos = 0
    while robot_moviendose:
        direccion = random.randint(0, 3)
        mover_robot(direccion, canvas, ventana)

# Función para detener el movimiento del robot
def detener_movimiento():
    global robot_moviendose
    robot_moviendose = False

# Función principal
def main():
    global ventana, canvas, robot

    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Simulación de laberinto")

    # Crear el lienzo
    canvas = tk.Canvas(ventana, width=ancho * 40, height=alto * 40)
    canvas.pack()

    # Generar el laberinto
    generar_laberinto()

    # Dibujar el laberinto
    dibujar_laberinto(canvas)

    # Pintar el objetivo
    pintar_objetivo(canvas)

    # Crear el robot
    robot = canvas.create_rectangle(x_robot * 40, y_robot * 40, (x_robot + 1) * 40, (y_robot + 1) * 40, fill="red")

    # Botón para iniciar el movimiento
    boton_iniciar = tk.Button(ventana, text="Iniciar", command=iniciar_movimiento)
    boton_iniciar.pack(side="left", padx=5)

    # Botón para detener el movimiento
    boton_detener = tk.Button(ventana, text="Detener", command=detener_movimiento)
    boton_detener.pack(side="left", padx=5)

    # Ejecutar el bucle de eventos de la ventana
    ventana.mainloop()

    # Mostrar la matriz del laberinto por consola
    for i, fila in enumerate(laberinto):
        fila_texto = ""
        for j, valor in enumerate(fila):
            if (j, i) == (x_robot, y_robot) or (j, i) == (x_objetivo, y_objetivo):
                fila_texto += "2"
            else:
                fila_texto += str(valor)
        print(fila_texto)

# Ejecutar la función principal
main()