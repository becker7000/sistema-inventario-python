import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from modelo.producto import Producto
from modelo.inventario import Inventario
from util.admin_archivo import guardar_json, cargar_json
import pandas as pd

class InventarioApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Registro de producto")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Centrado de ventana
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        altura = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (altura // 2)
        self.root.geometry(f"+{x}+{y}")

        # Inicializar inventario y cargar desde JSON
        self.inventario = Inventario()
        productos_guardados = cargar_json("inventario.json")
        self.inventario.cargar_desde_dicts(productos_guardados)

        # Variables del formulario
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.proveedor_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.precio_var = tk.StringVar()

        # Crear interfaz
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

        tk.Button(frame, text="Registrar producto", command=self.agregar_producto).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Editar producto", command=self.editar_producto).grid(row=7, column=0, columnspan=2, pady=5)
        tk.Button(frame, text="Eliminar producto", command=self.eliminar_producto).grid(row=8, column=0, columnspan=2, pady=5)
        tk.Button(frame, text="Exportar a Excel", command=self.exportar_excel).grid(row=9, column=0, columnspan=2, pady=5)

    def crear_tabla(self):
        self.tabla = ttk.Treeview(self.root, columns=(
            "ID", "Nombre", "Categoría", "Proveedor", "Cantidad", "Precio"), show="headings")
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Categoría", text="Categoría")
        self.tabla.heading("Proveedor", text="Proveedor")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Precio", text="Precio $")

        self.tabla.column("ID", width=50)
        self.tabla.column("Nombre", width=150)
        self.tabla.column("Categoría", width=100)
        self.tabla.column("Proveedor", width=120)
        self.tabla.column("Cantidad", width=80)
        self.tabla.column("Precio", width=80)

        self.tabla.pack(pady=20)

        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_producto)

    def seleccionar_producto(self, event):
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
            self.llenar_tabla()
            guardar_json("inventario.json", self.inventario.to_dict_list())
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
        except ValueError as e:
            messagebox.showerror("Error en los datos", str(e))

    def editar_producto(self):
        try:
            selected_id = self.id_var.get()
            if not selected_id:
                messagebox.showwarning("Selección", "Por favor, seleccione un producto primero.")
                return
            producto_actualizado = Producto(
                _id=self.id_var.get(),
                nombre=self.nombre_var.get(),
                categoria=self.categoria_var.get(),
                proveedor=self.proveedor_var.get(),
                cantidad=int(self.cantidad_var.get()),
                precio=float(self.precio_var.get())
            )
            if self.inventario.actualizar_producto(selected_id, **producto_actualizado.to_dict()):
                self.llenar_tabla()
                guardar_json("inventario.json", self.inventario.to_dict_list())
                messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            else:
                messagebox.showerror("Error", "Producto no encontrado.")
        except ValueError as e:
            messagebox.showerror("Error en los datos", str(e))

    def eliminar_producto(self):
        try:
            selected_id = self.id_var.get()
            if not selected_id:
                messagebox.showwarning("Selección", "Por favor, seleccione un producto primero.")
                return
            self.inventario.eliminar_producto(selected_id)
            self.llenar_tabla()
            guardar_json("inventario.json", self.inventario.to_dict_list())
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto:\n{e}")

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

    def exportar_excel(self):
        try:
            lista_dicts = self.inventario.to_dict_list()
            if not lista_dicts:
                messagebox.showinfo("Exportar", "No hay productos para exportar.")
                return
            df = pd.DataFrame(lista_dicts)
            df.to_excel("inventario.xlsx", index=False)
            messagebox.showinfo("Éxito", "Inventario exportado a 'inventario.xlsx' exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el archivo:\n{e}")

# Pruebas de escritorio:
ventana_inventario = tk.Tk()
# Se configura la ventana con los elementos de gui necesarios
app = InventarioApp(ventana_inventario)
ventana_inventario.mainloop()