# server.py
"""
Servidor MCP para Inventario con soporte de pH y reportes en español.
"""

import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from database import init_db

DB_PATH = Path(__file__).with_name("inventory.db")

def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Inicializar la base de datos
init_db()

mcp = FastMCP("InventarioDB")

# --- Auxiliares ---
RANGO_IDEAL_PH = (5.5, 6.5)

def _clasificar_ph(ph: Optional[float]) -> str:
    if ph is None:
        return "Desconocido (sin dato de pH)"
    bajo, alto = RANGO_IDEAL_PH
    if ph < bajo:
        return "Bajo (ácido)"
    if ph > alto:
        return "Alto (alcalino)"
    return "Óptimo (dentro del rango)"

def _fila_a_dicc(fila: tuple) -> Dict[str, Any]:
    return {
        "id": fila[0],
        "nombre": fila[1],
        "categoria": fila[2],
        "cantidad": fila[3],
        "precio": fila[4],
        "ph": fila[5],
    }

# --- CRUD ---
@mcp.tool()
def crear_producto(nombre: str, categoria: str, cantidad: int, precio: float, ph: Optional[float] = None) -> Dict[str, Any]:
    with _get_conn() as conn, closing(conn.cursor()) as cur:
        cur.execute(
            "INSERT INTO productos (nombre, categoria, cantidad, precio, ph) VALUES (?, ?, ?, ?, ?)",
            (nombre, categoria, cantidad, precio, ph),
        )
        conn.commit()
        nuevo_id = cur.lastrowid
        cur.execute("SELECT * FROM productos WHERE id = ?", (nuevo_id,))
        fila = cur.fetchone()
    return {"mensaje": "Producto creado exitosamente", "producto": _fila_a_dicc(fila)}

@mcp.tool()
def consultar_producto(id: int) -> Dict[str, Any]:
    with _get_conn() as conn, closing(conn.cursor()) as cur:
        cur.execute("SELECT * FROM productos WHERE id = ?", (id,))
        fila = cur.fetchone()
    if not fila:
        return {"error": "Producto no encontrado"}
    return _fila_a_dicc(fila)

@mcp.tool()
def actualizar_producto(id: int, cantidad: Optional[int] = None, ph: Optional[float] = None) -> Dict[str, Any]:
    campos = []
    valores = []
    if cantidad is not None:
        campos.append("cantidad = ?")
        valores.append(cantidad)
    if ph is not None:
        campos.append("ph = ?")
        valores.append(ph)
    if not campos:
        return {"mensaje": "Nada que actualizar"}
    valores.append(id)
    with _get_conn() as conn, closing(conn.cursor()) as cur:
        cur.execute(f"UPDATE productos SET {', '.join(campos)} WHERE id = ?", valores)
        conn.commit()
        cur.execute("SELECT * FROM productos WHERE id = ?", (id,))
        fila = cur.fetchone()
    if not fila:
        return {"error": "Producto no encontrado"}
    return {"mensaje": "Producto actualizado correctamente", "producto": _fila_a_dicc(fila)}

@mcp.tool()
def eliminar_producto(id: int) -> Dict[str, Any]:
    with _get_conn() as conn, closing(conn.cursor()) as cur:
        cur.execute("DELETE FROM productos WHERE id = ?", (id,))
        afectados = cur.rowcount
        conn.commit()
    if afectados == 0:
        return {"error": "Producto no encontrado"}
    return {"mensaje": "Producto eliminado correctamente", "id": id}

@mcp.tool()
def listar_productos() -> Dict[str, Any]:
    with _get_conn() as conn, closing(conn.cursor()) as cur:
        cur.execute("SELECT * FROM productos")
        filas = cur.fetchall()
    return {"productos": [_fila_a_dicc(f) for f in filas]}


@mcp.tool()
def reporte_estado() -> Dict[str, Any]:
    with _get_conn() as conn, closing(conn.cursor()) as cur:
        cur.execute("SELECT * FROM productos")
        filas = cur.fetchall()

    items = []
    for f in filas:
        item = _fila_a_dicc(f)
        item["estado"] = _clasificar_ph(item["ph"])
        items.append(item)

    return {
        "resumen": {
            "total_productos": len(items),
            "rango_ideal": RANGO_IDEAL_PH,
        },
        "productos": items,
    }

if __name__ == "__main__":
    print(f"Base de datos: {DB_PATH.resolve()}")
