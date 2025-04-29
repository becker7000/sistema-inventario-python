from modelo.producto import Producto
from modelo.inventario import Inventario
from util.admin_archivo import guardar_json, cargar_json

# Inventario global
invetario = Inventario()

# Cargando los productos desde un archivo JSON
datos = cargar_json("productos.json")
invetario.cargar_desde_dicts(datos)

def mostrar_menu():
    print("\n")
    print("\t +---------------MENÚ---------------+")
    print("\t | 1. Agregar producto              |")
    print("\t | 2. Listar productos              |")
    print("\t | 3. Buscar por nombre             |")
    print("\t | 4. Filtrar por categoria         |")
    print("\t | 5. Actualizar un producto        |")
    print("\t | 6. Eliminar un producto          |")
    print("\t | 7. Guardar y salir               |")
    print("\t +----------------------------------+")

if __name__=="__main__":

    while True: # Ciclo "infinito"

        mostrar_menu()
        opcion = input("\t Opción: ")

        if opcion=="1":
            _id = input("\t ID: ")
            nombre = input("\t Nombre: ")
            categoria = input("\t Categoría: ")
            proveedor = input("\t Proveedor: ")
            cantidad = int(input("\t Cantidad: "))
            precio = float(input("\t Precio: $ "))
            producto = Producto(_id,nombre,categoria,proveedor,cantidad,precio)
            invetario.agregar_producto(producto)
        elif opcion=="2":
            print("\n\n\t LISTA DE PRODUCTOS: ")
            for producto in invetario.listar_productos():
                print(producto.to_dict())
            # TODO: Mejorar la presentación de la lista de producto
        elif opcion=="3":
            nombre = input("\t Buscar por el nombre de: ")
            for producto in invetario.buscar_por_nombre(nombre):
                print(producto.to_dict())
        elif opcion=="4":
            categoria = input("\t Filtrar por categoría: ")
            for producto in invetario.filtrar_por_categoria(categoria):
                print(producto.to_dict())
        elif opcion=="5":
            _id = input("\t Id del producto a editar: ")
            # Solicitando el campo a editar:
            # TODO: crear la edición avanzada
            campo = input("\t Campo a editar: ").lower() # Transformamos a minúsculas
            valor = input("\t Nuevo valor: ") # Cadena "20"
            if campo in ["cantidad","precio"]:
                valor = float(valor) if campo == "precio" else int(valor)
            if invetario.actualizar_producto(_id,**{campo:valor}):
                print(f"\n\t El producto con id: {_id} ha sido actualizado.")
            else:
                print(f"\n\t El producto con id: {_id} no se encuentra en inventario.")
        elif opcion=="6":
            _id = input("\t Id del producto a eliminar: ")
            # Está a prueba de que no exista ese id
            # TODO: agregar un mensaje de confirmación para eliminar
            # TODO: enviar el producto eliminado a una lista de eliminados
            invetario.eliminar_producto(_id)
        elif opcion=="7":
            guardar_json("productos.json",invetario.to_dict_list())
            print("\n\t Productos guardados en formato JSON")
            break # Rompe con el while
        else: # Caso por defecto
            print("\n\t Opción no válida, selecciona una opción del 1 al 7.")











