
class Producto:

    def __init__(self,_id,nombre,categoria,proveedor,cantidad,precio):
        self.__id = _id
        self.__nombre = nombre
        self.__categoria = categoria
        self.__proveedor = proveedor
        self.__cantidad = cantidad
        self.__precio = precio

    # Getters y setters
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, _id):
        self.__id = _id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self,nombre):
        self.__nombre = nombre

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self,categoria):
        self.__categoria = categoria

    @property
    def proveedor(self):
        return self.__proveedor

    @proveedor.setter
    def proveedor(self,proveedor):
        self.__proveedor = proveedor

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self,cantidad):
        if isinstance(cantidad,int) and cantidad >= 0:
            self.__cantidad = cantidad
        else:
            raise ValueError("\n\t La cantidad debe de ser un entero positivo.")

    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self,precio):
        if isinstance(precio,(int,float)) and precio >=0:
            self.__precio = precio
        else:
            raise ValueError("\n\t El precio debe ser un número real positivo.")

    """
        to_dict()
        facilita la serialización (convertir a bits) de un objeto
        transforma un objeto en diccionario, sirve entonces para
        guardar en un formato el objeto (json, csv, etc)
        funciona directamente cuando los atributos son públicos
    """

    # Transforma un objeto a diccionario
    def to_dict(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "categoria": self.__categoria,
            "proveedor": self.__proveedor,
            "cantidad": self.__cantidad,
            "precio": self.__precio
        }

    # Transforma un diccionario a objeto
    @staticmethod
    def from_dict(data):
        return Producto(
            data["id"],
            data["nombre"],
            data["categoria"],
            data["proveedor"],
            data["cantidad"],
            data["precio"]
        )
