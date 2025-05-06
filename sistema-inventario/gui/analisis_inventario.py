import tkinter as tk  # Librería para la interfaz gráfica
from tkinter import ttk  # Widgets con estilo (como pestañas y tablas)
import pandas as pd  # Manejo de datos tabulares
import matplotlib.pyplot as plt  # Para crear gráficas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Para integrar gráficas en Tkinter

from util.admin_archivo import cargar_json  # Cargar los datos del inventario desde JSON

class AnalisisInventario:

    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de inventario")  # Título de la ventana
        self.lista_productos = cargar_json("inventario.json")  # Carga el inventario como lista de diccionarios
        self.df = pd.DataFrame(self.lista_productos)  # Convierte la lista a un DataFrame de pandas

        # Si el inventario está vacío, muestra un mensaje
        if self.df.empty:
            tk.Label(self.root, text="Inventario vacío. No hay datos para analizar.", font=("Arial", 14)).pack(pady=20)
        else:
            self.crear_interfaz()  # Si hay datos, crea la interfaz con pestañas y gráficas

    def crear_interfaz(self):
        notebook = ttk.Notebook(self.root)  # Crea un contenedor con pestañas
        notebook.pack(fill='both', expand=True)  # Ocupa todo el espacio disponible

        # Se crean los marcos para cada pestaña
        self.frame_barras = ttk.Frame(notebook)
        self.frame_tabla = ttk.Frame(notebook)
        self.frame_distribucion = ttk.Frame(notebook)
        self.frame_pastel = ttk.Frame(notebook)

        # Se agregan las pestañas con sus respectivos títulos
        notebook.add(self.frame_barras, text="Barras por categoría")
        notebook.add(self.frame_tabla, text="Análisis de precios")
        notebook.add(self.frame_distribucion, text="Distribución de precios")
        notebook.add(self.frame_pastel, text="Participación por categoría")

        # Se llaman los métodos que construyen cada visualización
        self.grafica_barras_por_categoria()
        self.mostrar_tabla_analisis_precios()
        self.grafica_distribucion_precios()
        self.grafica_pastel_categoria_valor_total()

    def grafica_barras_por_categoria(self):
        conteo = self.df["categoria"].value_counts()  # Cuenta cuántos productos hay por categoría
        fig, ax = plt.subplots(figsize=(6, 4))  # Crea una figura y un eje
        conteo.plot(kind="bar", ax=ax, color="skyblue")  # Dibuja una gráfica de barras
        ax.set_title("Cantidad de productos por categoría")
        ax.set_xlabel("Categoría")
        ax.set_ylabel("Cantidad")
        ax.grid(True, axis='y')
        ax.set_xticklabels(conteo.index, rotation=45)  # ← ROTA los nombres de categoría 45 grados
        self.mostrar_canvas(fig, self.frame_barras)  # Muestra la figura en la pestaña correspondiente

    def mostrar_tabla_analisis_precios(self):
        frame = tk.Frame(self.frame_tabla)
        frame.pack(pady=10)

        tabla = ttk.Treeview(frame, columns=("Métrica", "Valor"), show="headings")  # Crea tabla con dos columnas
        tabla.heading("Métrica", text="Métrica")
        tabla.heading("Valor", text="Valor")
        tabla.pack()

        # Cálculo de métricas estadísticas del precio
        precio_promedio = round(self.df["precio"].mean(), 2)
        precio_max = self.df.loc[self.df["precio"].idxmax()]  # Producto con precio más alto
        precio_min = self.df.loc[self.df["precio"].idxmin()]  # Producto con precio más bajo
        desviacion = round(self.df["precio"].std(), 2)  # Desviación estándar del precio

        # Lista de métricas a mostrar
        datos = [
            ("Precio promedio", f"${precio_promedio}"),
            ("Producto más caro", f"{precio_max['nombre']} (${precio_max['precio']})"),
            ("Producto más barato", f"{precio_min['nombre']} (${precio_min['precio']})"),
            ("Desviación estándar", f"${desviacion}")
        ]

        # Se insertan los valores en la tabla
        for metrica, valor in datos:
            tabla.insert("", "end", values=(metrica, valor))

    def grafica_distribucion_precios(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        self.df["precio"].plot(kind="hist", bins=10, color="orange", edgecolor="black", ax=ax)  # Histograma de precios
        ax.set_title("Distribución de precios")
        ax.set_xlabel("Precio")
        ax.set_ylabel("Frecuencia")
        ax.grid(True, axis='y')
        self.mostrar_canvas(fig, self.frame_distribucion)

    def grafica_pastel_categoria_valor_total(self):
        self.df["valor_total"] = self.df["precio"] * self.df["cantidad"]  # Calcula el valor total por producto
        valores_categoria = self.df.groupby("categoria")["valor_total"].sum()  # Agrupa por categoría
        top5 = valores_categoria.sort_values(ascending=False).head(5)  # Selecciona las 5 categorías más valiosas

        fig, ax = plt.subplots(figsize=(6, 4))
        top5.plot(kind="pie", autopct='%1.1f%%', startangle=140, ax=ax)  # Gráfica de pastel
        ax.set_title("Participación por categoría (valor total)")
        ax.set_ylabel("")  # Elimina el texto del eje Y
        self.mostrar_canvas(fig, self.frame_pastel)

    def mostrar_canvas(self, figura, contenedor):
        canvas = FigureCanvasTkAgg(figura, master=contenedor)  # Crea el lienzo que integra la gráfica
        canvas.draw()  # Dibuja la figura
        canvas.get_tk_widget().pack(fill='both', expand=True)  # Inserta en el contenedor Tkinter
