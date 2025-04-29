import json

# Sirve para guardar los productos en formato json
def guardar_json(nombre_archivo, data):
    with open(nombre_archivo,'w',encoding='UTF-8') as archivo:
        json.dump(data,archivo,indent=4)

# Sirve para extraer los productos desde un archivo json
def cargar_json(nombre_archivo):
    try: # Intentar hacer lo siguiente
        with open(nombre_archivo,'r',encoding='UTF-8') as archivo:
            return json.load(archivo)
    except FileNotFoundError: # En caso de archivo no encontrado
        print("\n\t Inventario vacío \n")
        return [] # Retorna una lista vacía