import os
import importlib
import random

# Registro de estadísticas
estadisticas = {
    "correctas": 0,
    "incorrectas": 0,
    "fallos": {},  # Para almacenar cuántas veces fallaste cada pregunta
}

def limpiar_pantalla():
    """Limpia la pantalla dependiendo del sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")

def obtener_temas_disponibles():
    """Obtiene la lista de temas disponibles a partir de los archivos en el directorio 'temas'."""
    temas_dir = "temas"
    temas_disponibles = {}
    
    try:
        archivos = os.listdir(temas_dir)
        for archivo in archivos:
            if archivo.endswith(".py") and archivo != "__init__.py":
                tema_nombre = archivo.replace(".py", "")
                descripcion = tema_nombre.replace("_", " ").capitalize()
                temas_disponibles[tema_nombre] = descripcion
    except FileNotFoundError:
        print(f"Error: El directorio '{temas_dir}' no existe.")
    
    return temas_disponibles

def cargar_tema(nombre_modulo):
    """Carga el módulo correspondiente al tema seleccionado."""
    try:
        modulo = importlib.import_module(f"temas.{nombre_modulo}")
        return modulo.diccionario
    except ModuleNotFoundError:
        print(f"Error: El tema '{nombre_modulo}' no existe.")
        return None

def cargar_logica(nombre_modulo):
    """Carga la lógica correspondiente al tema seleccionado."""
    try:
        modulo = importlib.import_module(f"logica_preguntas.{nombre_modulo}")
        return modulo.generar_pregunta
    except ModuleNotFoundError:
        print(f"Error: No se encontró la lógica para el tema '{nombre_modulo}'.")
        return None

def realizar_pregunta(funcion_pregunta, pregunta, respuesta_correcta):
    """Realiza una pregunta utilizando la función específica del tema."""
    limpiar_pantalla()  # Limpiar la pantalla antes de la pregunta
    respuesta_correcta = funcion_pregunta(pregunta, respuesta_correcta)
    respuesta = input("Tu respuesta: ").strip().lower()
    
    if respuesta == respuesta_correcta:
        print("¡Correcto!")
        estadisticas["correctas"] += 1
    else:
        print(f"Incorrecto. La respuesta correcta es '{respuesta_correcta}'.")
        estadisticas["incorrectas"] += 1
        if pregunta not in estadisticas["fallos"]:
            estadisticas["fallos"][pregunta] = 0
        estadisticas["fallos"][pregunta] += 1
    input("\nPresiona Enter para continuar...")  # Pausa para que el usuario lea el resultado

def main():
    print("¡Bienvenido al programa de práctica de temas diversos!")
    
    temas_disponibles = obtener_temas_disponibles()
    
    if not temas_disponibles:
        print("No hay temas disponibles para practicar. Por favor, agrega temas al directorio 'temas'.")
        return
    
    # Mostrar temas disponibles
    print("Temas disponibles:")
    for idx, (clave, descripcion) in enumerate(temas_disponibles.items(), 1):
        print(f"{idx}. {descripcion}")
    
    tema_seleccionado = None
    while tema_seleccionado not in temas_disponibles:
        opcion = input("Selecciona un tema por su número: ")
        try:
            tema_seleccionado = list(temas_disponibles.keys())[int(opcion) - 1]
        except (ValueError, IndexError):
            print("Opción no válida. Intenta de nuevo.")
    
    descripcion_tema = temas_disponibles[tema_seleccionado]
    print(f"\nHas seleccionado el tema: {descripcion_tema}")
    
    diccionario_preguntas = cargar_tema(tema_seleccionado)
    if not diccionario_preguntas:
        print("No se pudo cargar el tema. Terminando programa.")
        return
    
    funcion_pregunta = cargar_logica(tema_seleccionado)
    if not funcion_pregunta:
        print("No se pudo cargar la lógica del tema. Terminando programa.")
        return
    
    cantidad_preguntas = int(input("¿Cuántas preguntas deseas responder? "))
    
    preguntas_restantes = cantidad_preguntas
    
    while preguntas_restantes > 0:
        palabra, respuesta = random.choice(list(diccionario_preguntas.items()))
        realizar_pregunta(funcion_pregunta, palabra, respuesta)
        preguntas_restantes -= 1
    
    print("\n=== Estadísticas ===")
    print(f"Respuestas correctas: {estadisticas['correctas']}")
    print(f"Respuestas incorrectas: {estadisticas['incorrectas']}")
    
    if estadisticas["fallos"]:
        print("\nPreguntas en las que fallaste:")
        for pregunta, veces in estadisticas["fallos"].items():
            print(f"- '{pregunta}': {veces} vez/veces")

if __name__ == "__main__":
    main()
