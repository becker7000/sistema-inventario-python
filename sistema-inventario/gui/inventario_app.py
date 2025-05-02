import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import messagebox

from modelo.producto import Producto
from modelo.inventario import Inventario
from util.admin_archivo import guardar_json, cargar_json
from .analisis_inventario import AnalisisInventario

class InventarioApp:

    def __init__(self, root):  # Root es una ventana raíz
        self.root = root
        self.root.title("Sistema de inventario")
        self.root.geometry("800x600")  # Tamaño
        self.root.resizable(False, False)  # Restringiendo el ajuste ancho y altura

        # Centramos la ventana
        self.root.update_idletasks()
        ancho = self.root.winfo_width()  # Obtenemos la información de la anchura de la ventana
        altura = self.root.winfo_height()  # Obtenemos la información de la altura de la ventana
        # Serán las coordenadas de la esquina superior izquierda de la ventana
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (altura // 2)
        # Inicia las coordenadas de la esquina superior izquierda de la ventana
        self.root.geometry(f"+{x}+{y}")

        # Creamos un objeto inventario y cargamos los productos desde un JSON
        self.inventario = Inventario()  # Inventario vacío...
        productos_guardados = cargar_json("inventario.json")  # Se crea un diccionario
        self.inventario.cargar_desde_dicts(productos_guardados)  # Se pasa al inventario

        # Elementos de input para guardar los atributos
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.proveedor_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.precio_var = tk.StringVar()

        # Creamos de forma modular el formulario y
        # una tabla (lista) de productos
        self.crear_formulario()
        self.crear_tabla()
        self.llenar_tabla()

    def crear_formulario(self):

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="ID").grid(row=0, column=0)
        tk.Entry(frame, textvariable=self.id_var).grid(row=0, column=1)

        tk.Label(frame, text="Nombre").grid(row=1, column=0)
        tk.Entry(frame, textvariable=self.nombre_var).grid(row=1, column=1)

        tk.Label(frame, text="Categoría").grid(row=2, column=0)
        tk.Entry(frame, textvariable=self.categoria_var).grid(row=2, column=1)

        tk.Label(frame, text="Proveedor").grid(row=3, column=0)
        tk.Entry(frame, textvariable=self.proveedor_var).grid(row=3, column=1)

        tk.Label(frame, text="Cantidad").grid(row=4, column=0)
        tk.Entry(frame, textvariable=self.cantidad_var).grid(row=4, column=1)

        tk.Label(frame, text="Precio $").grid(row=5, column=0)
        tk.Entry(frame, textvariable=self.precio_var).grid(row=5, column=1)

        # Botones para las operaciones del inventario

        tk.Button(
            frame,
            text="Registrar producto",
            command=self.agregar_producto
        ).grid(row=6, column=0, pady=10)

        tk.Button(
            frame,
            text="Editar producto",
            command=self.editar_producto,
        ).grid(row=6, column=1, pady=10)

        tk.Button(
            frame,
            text="Eliminar producto",
            command=self.eliminar_producto,
        ).grid(row=8, column=0, pady=10)

        tk.Button(
            frame,
            text="Exportar a Excel",
            command=self.exportar_excel
        ).grid(row=8, column=1, pady=10)

        tk.Button(
            frame,
            text="Ver análisis de productos",
            command=self.abrir_analisis
        ).grid(row=9, column=0, columnspan=2, pady=10)


    def crear_tabla(self):
        self.tabla = ttk.Treeview(self.root,
                                  columns=("ID", "Nombre", "Categoría", "Proveedor", "Cantidad", "Precio"),
                                  show="headings")
        # Asignando encabezados y columnas:
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Categoría", text="Categoría")
        self.tabla.heading("Proveedor", text="Proveedor")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Precio", text="Precio $")
        # Configuración columnas:
        self.tabla.column("ID", width=48)
        self.tabla.column("Nombre", width=160)
        self.tabla.column("Categoría", width=100)
        self.tabla.column("Proveedor", width=100)
        self.tabla.column("Cantidad", width=80)
        self.tabla.column("Precio", width=80)
        self.tabla.pack(pady=20)
        self.tabla.bind("<ButtonRelease-1>",self.seleccionar_producto)

    def seleccionar_producto(self,event):
        item = self.tabla.selection()
        if not item:
            return
        item_values = self.tabla.item(item, "values")
        if item_values:
            self.id_var.set(item_values[0])
            self.nombre_var.set(item_values[1])
            self.categoria_var.set(item_values[2])
            self.proveedor_var.set(item_values[3])
            self.cantidad_var.set(item_values[4])
            self.precio_var.set(item_values[5])

    def agregar_producto(self):
        try:
            producto = Producto(
                _id=self.id_var.get(),
                nombre=self.nombre_var.get(),
                categoria=self.categoria_var.get(),
                proveedor=self.proveedor_var.get(),
                cantidad=int(self.cantidad_var.get()),
                precio=float(self.precio_var.get())
            )
            self.inventario.agregar_producto(producto)
            self.llenar_tabla()  # Mé_todo pendiente
            guardar_json("inventario.json", self.inventario.to_dict_list())
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
        except ValueError:
            messagebox.showerror(
                "Error en los datos",
                "La cantidad debe ser un entero y el precio real"
            )
            return  # Finaliza el mé_todo sin hacer nada

    def llenar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for producto in self.inventario.listar_productos():
            self.tabla.insert("", "end", values=(
                producto.id,
                producto.nombre,
                producto.categoria,
                producto.proveedor,
                producto.cantidad,
                producto.precio
            ))

    def editar_producto(self):
        try:
            id_seleccionado = self.id_var.get()
            if not id_seleccionado:  # Validamos si existe un producto seleccionado
                messagebox.showwarning("Sin selección", "Para editar un producto, por favor, selecciona uno")
                return  # Termina el mé_todo
            # El usuario deberá aparte seleccionar
            # cambiar los valores de los campos que requiera modificar
            producto_actualizado = Producto(
                _id=self.id_var.get(),
                nombre=self.nombre_var.get(),
                categoria=self.categoria_var.get(),
                proveedor=self.proveedor_var.get(),
                cantidad=int(self.cantidad_var.get()),  # Casteo de string a int
                precio=float(self.precio_var.get()) # Precio: Hola
            )
            if self.inventario.actualizar_producto(id_seleccionado,**producto_actualizado.to_dict()):
                self.llenar_tabla()
                guardar_json("inventario.json",self.inventario.to_dict_list())
                messagebox.showinfo("Producto editado","Producto actualizado correctamente.")
            else:
                messagebox.showerror("Producto no encotrado","Error, el producto que se desea editar no existe.")
        except ValueError:
            messagebox.showerror("Error","No se pudo editar el producto (verificar los valores de entrada).")

    def eliminar_producto(self):
        try:
            id_seleccionado = self.id_var.get()
            if not id_seleccionado:
                messagebox.showwarning("Sin selección","Para poder eliminar un producto, por favor, selecciona uno.")
                return # Termina el mé_todo
            self.inventario.eliminar_producto(id_seleccionado)
            self.llenar_tabla()
            guardar_json("inventario.json",self.inventario.to_dict_list())
            messagebox.showinfo("Producto eliminado","Producto eliminado correctamente.")
        except Exception:
            messagebox.showerror("Error","No se pudo editar el producto (verificar los valores de entrada).")

    def exportar_excel(self):
        try:
            lista_diccionarios = self.inventario.to_dict_list()
            if not lista_diccionarios:
                messagebox.showinfo("Sin productos","No hay productos para exportar a Excel")
                return # Termina el mé_todo
            dataframe_productos = pd.DataFrame(lista_diccionarios)
            dataframe_productos.to_excel("inventario.xlsx",index=False)
            messagebox.showinfo("Inventario exportado","La lista de producto se exportó a un Excel correctamente")
        except Exception as ex:
            messagebox.showerror("Error",f"No se pudo exportar a Excel ({ex})")

    def abrir_analisis(self):
        ventana_analisis = tk.Toplevel(self.root)
        AnalisisInventario(ventana_analisis)


# Aprender Linux(Ubuntu)
# Redes de computadoras
# Tenembuam
