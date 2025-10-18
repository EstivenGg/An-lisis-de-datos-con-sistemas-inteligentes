# server.py
"""
Servidor MCP para Inventario con soporte de pH y reportes bilingües (ES/EN).

Requisitos:
  pip install fastmcp

Ejecución:
  python server.py
"""

import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Dict, Any, Optional, Literal
from mcp.server.fastmcp import FastMCP

from database import init_db

# --- Configuración de base de datos ---
DB_PATH = Path(__file__).with_name("inventory.db")

def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Inicializar la base de datos (crea tabla si no existe)
init_db()

# --- Servidor MCP ---
mcp = FastMCP("InventarioDB")

# --- Funciones auxiliares ---
RANGO_IDEAL_PH = (5.5, 6.5)

def _clasificar_ph(ph: Optional[float]) -> str:
    if ph is None:
        return "desconocido"
    bajo, alto = RANGO_IDEAL_PH
    if ph < bajo:
        return "bajo"
    if ph > alto:
        return "alto"
    return "óptimo"

def _traducir_estado(estado: str, idioma: Literal["es", "en"]) -> str:
    tabla = {
        "óptimo": {"es": "Óptimo (dentro del rango)", "en": "Optimal (within range)"},
        "bajo": {"es": "Bajo (ácido)", "en": "Low (acidic)"},
        "alto": {"es": "Alto (alcalino)", "en": "High (alkaline)"},
        "desconocido": {"es": "Desconocido (sin dato de pH)", "en": "Unknown (no pH data)"},
    }
    return tabla[estado][idioma]

def _fila_a_dicc(fila: tuple) -> Dict[str, Any]:
    return {
        "id": fila[0],
        "nombre": fila[1],
        "categoria": fila[2],
        "cantidad": fila[3],
        "precio": fila[4],
        "ph": fila[5],
    }

# --- Herramientas CRUD ---
@mcp.tool()
def crear_producto(nombre: str, categoria: str, cantidad: int, precio: float, ph: Optional[float] = None) -> Dict[str, Any]:
    """Crea un producto en el inventario con soporte de pH."""
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
    """Consulta un producto por su ID."""
    with _get_conn() as conn, closing(conn.cursor()) as cur:
        cur.execute("SELECT * FROM productos WHERE id = ?", (id,))
        fila = cur.fetchone()
    if not fila:
        return {"error": "Producto no encontrado"}
    return _fila_a_dicc(fila)

@mcp.tool()
def actualizar_producto(id: int, cantidad: Optional[int] = None, ph: Optional[float] = None) -> Dict[str, Any]:
    """Actualiza cantidad o pH de un producto existente."""
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
    """Elimina un producto por ID."""
    with _get_conn() as conn, closing(conn.cursor()) as cur:
        cur.execute("DELETE FROM productos WHERE id = ?", (id,))
        afectados = cur.rowcount
        conn.commit()
    if afectados == 0:
        return {"error": "Producto no encontrado"}
    return {"mensaje": "Producto eliminado correctamente", "id": id}

@mcp.tool()
def listar_productos() -> Dict[str, Any]:
    """Lista todos los productos del inventario."""
    with _get_conn() as conn, closing(conn.cursor()) as cur:
        cur.execute("SELECT * FROM productos")
        filas = cur.fetchall()
    return {"productos": [_fila_a_dicc(f) for f in filas]}

# --- Reporte del estado del invernadero ---
@mcp.tool()
def reporte_estado(idioma: Literal["es", "en"] = "es") -> Dict[str, Any]:
    """Genera un reporte del estado del invernadero según pH en español o inglés."""
    with _get_conn() as conn, closing(conn.cursor()) as cur:
        cur.execute("SELECT * FROM productos")
        filas = cur.fetchall()

    items = []
    for f in filas:
        item = _fila_a_dicc(f)
        estado = _clasificar_ph(item["ph"])
        item["estado"] = _traducir_estado(estado, idioma)
        items.append(item)

    return {
        "resumen": {
            "total_productos": len(items),
            "rango_ideal": RANGO_IDEAL_PH,
        },
        "productos": items,
    }

# --- Recursos ---
@mcp.resource("productos://listado")
def recurso_listado() -> Dict[str, Any]:
    return listar_productos()

@mcp.resource("reporte://estado-es")
def recurso_reporte_es() -> Dict[str, Any]:
    return reporte_estado(idioma="es")

@mcp.resource("reporte://estado-en")
def recurso_reporte_en() -> Dict[str, Any]:
    return reporte_estado(idioma="en")

# --- Arranque del servidor ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:mcp", host="127.0.0.1", port=8000, reload=True)
