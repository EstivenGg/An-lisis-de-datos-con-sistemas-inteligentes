# database.py
"""
Inicializa y migra la base de datos SQLite para el proyecto MCP CRUD.
Crea la tabla 'productos' con las columnas:
id, nombre, categoria, cantidad, precio, ph

Si la tabla ya existe pero no tiene la columna 'ph', la agrega automáticamente.
"""

import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).with_name("inventory.db")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    with closing(conn.cursor()) as cur:
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (table,),
        )
        return cur.fetchone() is not None


def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    with closing(conn.cursor()) as cur:
        cur.execute(f"PRAGMA table_info({table});")
        cols = [row[1] for row in cur.fetchall()] 
        return column in cols


def _create_schema(conn: sqlite3.Connection) -> None:
    with closing(conn.cursor()) as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS productos (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre    TEXT    NOT NULL,
                categoria TEXT,
                cantidad  INTEGER DEFAULT 0,
                precio    REAL    DEFAULT 0.0,
                ph        REAL
            );
            """
        )
        cur.execute("CREATE INDEX IF NOT EXISTS idx_productos_nombre ON productos(nombre);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_productos_categoria ON productos(categoria);")
    conn.commit()


def _migrate_add_ph_if_missing(conn: sqlite3.Connection) -> None:
    """Si la tabla 'productos' existe sin columna 'ph', la agrega."""
    if _table_exists(conn, "productos") and not _column_exists(conn, "productos", "ph"):
        with closing(conn.cursor()) as cur:
            cur.execute("ALTER TABLE productos ADD COLUMN ph REAL;")
        conn.commit()


def init_db() -> None:
    """
    Inicializa la base de datos:
    - Crea archivo inventory.db si no existe.
    - Crea tabla 'productos' si no existe.
    - Migra para agregar columna 'ph' si faltara.
    """
    DB_PATH.touch(exist_ok=True)
    with _get_conn() as conn:
        _create_schema(conn)
        _migrate_add_ph_if_missing(conn)


# Ejecutar directamente para inicializar desde la terminal:
if __name__ == "__main__":
    init_db()
    print(f"Base de datos lista en: {DB_PATH.resolve()}")
