import sqlite3
from modelo.producto import Producto

DATABASE_NAME = "productos.db"

def crear_tabla():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                proveedor TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        conn.commit()

def insertar_producto(producto: Producto):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (id, nombre, categoria, proveedor, cantidad, precio)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            producto.id,
            producto.nombre,
            producto.categoria,
            producto.proveedor,
            producto.cantidad,
            producto.precio
        ))
        conn.commit()

def obtener_productos():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos')
        rows = cursor.fetchall()
        return [Producto.from_dict({
            "id": row[0],
            "nombre": row[1],
            "categoria": row[2],
            "proveedor": row[3],
            "cantidad": row[4],
            "precio": row[5]
        }) for row in rows]

def buscar_por_nombre(nombre):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
        rows = cursor.fetchall()
        return [Producto.from_dict({
            "id": row[0],
            "nombre": row[1],
            "categoria": row[2],
            "proveedor": row[3],
            "cantidad": row[4],
            "precio": row[5]
        }) for row in rows]

def filtrar_por_categoria(categoria):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE categoria = ?", (categoria,))
        rows = cursor.fetchall()
        return [Producto.from_dict({
            "id": row[0],
            "nombre": row[1],
            "categoria": row[2],
            "proveedor": row[3],
            "cantidad": row[4],
            "precio": row[5]
        }) for row in rows]

def actualizar_producto(producto: Producto):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE productos
            SET nombre = ?, categoria = ?, proveedor = ?, cantidad = ?, precio = ?
            WHERE id = ?
        ''', (
            producto.nombre,
            producto.categoria,
            producto.proveedor,
            producto.cantidad,
            producto.precio,
            producto.id
        ))
        conn.commit()

def eliminar_producto(producto_id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conn.commit()
