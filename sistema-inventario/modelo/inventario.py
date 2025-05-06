from modelo.producto import Producto

class Inventario:

    def __init__(self):
        self.__productos = []

    # Indicamos que el objeto producto es de la clase Producto
    def agregar_producto(self,producto:Producto):
        self.__productos.append(producto)
        print(f"\n\t Se agregó el producto '{producto.nombre}' ") # Usando un getter

    def listar_productos(self):
        return self.__productos

    def buscar_por_nombre(self,nombre):
        return [ prod for prod in self.__productos if nombre.lower() in prod.to_dict()["nombre"].lower()]

    def filtrar_por_categoria(self,categoria):
        return [ prod for prod in self.__productos if prod.to_dict()["categoria"] == categoria]

    # kwargs (keywords arguments) pueden ser: nombre, categoria, proveedor, cantidad y precio
    def actualizar_producto(self,_id,**kwargs):
        for producto in self.__productos:
            if producto.to_dict()["id"] == _id:  # Comparamos si el id del producto es igual un id
                datos = producto.to_dict()       # Transformamos el objeto producto a diccionario
                datos.update(kwargs)            # Actualizamos los valores de las claves
                self.__productos.remove(producto)  # Eliminamos el producto antiguo
                producto_editado = Producto.from_dict(datos) # Crear un nuevo producto con el diccionario
                self.__productos.append(producto_editado) # Lo agregamos a la lista
                return True # En caso de que el producto existe y pudo modificar (termina el mé_todo)
        return False # En caso de que el id del producto no se haya encontrado

    # Se devuelve una lista con todos los productos, excepto el producto con un id especifico
    def eliminar_producto(self,_id):
        self.__productos = [prod for prod in self.__productos if prod.to_dict()["id"] != _id]

    # Transforma un lista de productos a una lista de diccionarios:
    # Para cada producto de la lista de productos, transformalo a diccionario y guardalo en
    # esta lista...
    def to_dict_list(self):
        return [ prod.to_dict() for prod in self.__productos] # Lista de diccionarios...

    # Transforma una lista de diccionarios a una lista de objetos:
    def cargar_desde_dicts(self,data_list):
        for data in data_list:
            self.agregar_producto(Producto.from_dict(data))





