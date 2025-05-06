# main.py

from modelo.producto import Producto
import util.base_datos as db

def mostrar_menu():
    print("\t +---------------MENÚ---------------+")
    print("\t | 1. Agregar producto              |")
    print("\t | 2. Listar productos              |")
    print("\t | 3. Buscar por nombre             |")
    print("\t | 4. Filtrar por categoria         |")
    print("\t | 5. Actualizar un producto        |")
    print("\t | 6. Eliminar un producto          |")
    print("\t | 7. Guardar y salir               |")
    print("\t +----------------------------------+")

def input_producto():
    try:
        _id = int(input("ID: "))
        nombre = input("Nombre: ")
        categoria = input("Categoría: ")
        proveedor = input("Proveedor: ")
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
        return Producto(_id, nombre, categoria, proveedor, cantidad, precio)
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    db.crear_tabla()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n>> Agregar nuevo producto")
            producto = input_producto()
            if producto:
                db.insertar_producto(producto)
                print("Producto agregado con éxito.")
        elif opcion == "2":
            print("\n>> Lista de productos")
            productos = db.obtener_productos()
            for p in productos:
                print(f"{p.id} | {p.nombre} | {p.categoria} | {p.proveedor} | {p.cantidad} | ${p.precio:.2f}")
        elif opcion == "3":
            nombre = input("Ingrese nombre a buscar: ")
            resultados = db.buscar_por_nombre(nombre)
            for p in resultados:
                print(f"{p.id} | {p.nombre} | {p.categoria} | {p.proveedor} | {p.cantidad} | ${p.precio:.2f}")
        elif opcion == "4":
            categoria = input("Ingrese categoría a filtrar: ")
            resultados = db.filtrar_por_categoria(categoria)
            for p in resultados:
                print(f"{p.id} | {p.nombre} | {p.categoria} | {p.proveedor} | {p.cantidad} | ${p.precio:.2f}")
        elif opcion == "5":
            try:
                id_actualizar = int(input("ID del producto a actualizar: "))
                producto_nuevo = input_producto()
                if producto_nuevo:
                    producto_nuevo.id = id_actualizar
                    db.actualizar_producto(producto_nuevo)
                    print("Producto actualizado con éxito.")
            except ValueError:
                print("ID inválido.")
        elif opcion == "6":
            try:
                id_eliminar = int(input("ID del producto a eliminar: "))
                db.eliminar_producto(id_eliminar)
                print("Producto eliminado.")
            except ValueError:
                print("ID inválido.")
        elif opcion == "7":
            print("Guardando y saliendo...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
