# Análisis de datos con sistemas inteligentes

Este proyecto corresponde a la Actividad 6 – Sistemas Cognitivos basados en Big Data.  
Implementa un servidor MCP en Python con operaciones CRUD sobre una base de datos SQLite para gestionar un inventario agrícola.  

Se agregó la variable pH como parámetro clave en los productos del invernadero y se generó un reporte en español que clasifica el estado de cada producto según su nivel de pH.  

## Características
- CRUD completo sobre productos (crear, consultar, actualizar, eliminar).  
- Base de datos SQLite (inventory.db).  
- Variable pH integrada para control del invernadero.  
- Reporte del estado del invernadero en español.  
- Scripts de prueba incluidos.  

## Estructura del proyecto
```
mcp_crud_inventory/
├── database.py         # Inicialización de la base de datos
├── server.py           # Servidor MCP con CRUD y reporte
├── test_carga.py       # Script para cargar productos de ejemplo
├── test_operaciones.py # Pruebas de consulta, actualización y eliminación
├── test_reporte.py     # Generación de reporte en español
└── inventory.db        # Base de datos (se crea automáticamente)
```

## Tecnologías utilizadas
- Python 3.8+  
- SQLite3 (incluido en Python)  
- fastmcp  

## Instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/EstivenGg/An-lisis-de-datos-con-sistemas-inteligentes.git
   cd An-lisis-de-datos-con-sistemas-inteligentes
   ```

2. Crear entorno virtual (opcional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install fastmcp
   ```

## Ejecución de pruebas

### 1. Cargar productos de ejemplo
```bash
python test_carga.py
```

**Salida esperada:**
```
=== Creación de productos ===
{'id': 1, 'nombre': 'Tomate', 'categoria': 'Hortalizas', 'cantidad': 50, 'precio': 1.2, 'ph': 6.2}
{'id': 2, 'nombre': 'Lechuga', 'categoria': 'Hortalizas', 'cantidad': 80, 'precio': 0.9, 'ph': 5.6}
{'id': 3, 'nombre': 'Fresa', 'categoria': 'Frutas', 'cantidad': 40, 'precio': 2.5, 'ph': 3.5}
{'id': 4, 'nombre': 'Pepino', 'categoria': 'Hortalizas', 'cantidad': 60, 'precio': 1.1, 'ph': 7.0}
{'id': 5, 'nombre': 'Arándano', 'categoria': 'Frutas', 'cantidad': 30, 'precio': 3.2, 'ph': 5.9}

=== Listado total ===
{'id': 1, 'nombre': 'Tomate', 'categoria': 'Hortalizas', 'cantidad': 50, 'precio': 1.2, 'ph': 6.2}
{'id': 2, 'nombre': 'Lechuga', 'categoria': 'Hortalizas', 'cantidad': 80, 'precio': 0.9, 'ph': 5.6}
{'id': 3, 'nombre': 'Fresa', 'categoria': 'Frutas', 'cantidad': 40, 'precio': 2.5, 'ph': 3.5}
{'id': 4, 'nombre': 'Pepino', 'categoria': 'Hortalizas', 'cantidad': 60, 'precio': 1.1, 'ph': 7.0}
{'id': 5, 'nombre': 'Arándano', 'categoria': 'Frutas', 'cantidad': 30, 'precio': 3.2, 'ph': 5.9}
```

### 2. Operaciones CRUD
```bash
python test_operaciones.py
```

**Salida esperada:**
```
=== Consultar producto ===
{'id': 1, 'nombre': 'Tomate', 'categoria': 'Hortalizas', 'cantidad': 50, 'precio': 1.2, 'ph': 6.2}

=== Actualizar producto ===
{'mensaje': 'Producto actualizado correctamente', 'producto': {'id': 1, 'nombre': 'Tomate', 'categoria': 'Hortalizas', 'cantidad': 100, 'precio': 1.2, 'ph': 6.0}}

=== Eliminar producto ===
{'mensaje': 'Producto eliminado correctamente', 'id': 5}

=== Listado final ===
{'productos': [{'id': 1, 'nombre': 'Tomate', 'categoria': 'Hortalizas', 'cantidad': 100, 'precio': 1.2, 'ph': 6.0}, {'id': 2, 'nombre': 'Lechuga', 'categoria': 'Hortalizas', 'cantidad': 80, 'precio': 0.9, 'ph': 5.6}, {'id': 3, 'nombre': 'Fresa', 'categoria': 'Frutas', 'cantidad': 40, 'precio': 2.5, 'ph': 3.5}, {'id': 4, 'nombre': 'Pepino', 'categoria': 'Hortalizas', 'cantidad': 60, 'precio': 1.1, 'ph': 7.0}]}
```

### 3. Generar reporte
```bash
python test_reporte.py
```

**Salida esperada:**
```
=== Reporte del invernadero (ES) ===
{'total_productos': 4, 'rango_ideal': (5.5, 6.5)}
{'id': 1, 'nombre': 'Tomate', 'categoria': 'Hortalizas', 'cantidad': 100, 'precio': 1.2, 'ph': 6.0, 'estado': 'Óptimo (dentro del rango)'}
{'id': 2, 'nombre': 'Lechuga', 'categoria': 'Hortalizas', 'cantidad': 80, 'precio': 0.9, 'ph': 5.6, 'estado': 'Óptimo (dentro del rango)'}
{'id': 3, 'nombre': 'Fresa', 'categoria': 'Frutas', 'cantidad': 40, 'precio': 2.5, 'ph': 3.5, 'estado': 'Bajo (ácido)'}
{'id': 4, 'nombre': 'Pepino', 'categoria': 'Hortalizas', 'cantidad': 60, 'precio': 1.1, 'ph': 7.0, 'estado': 'Alto (alcalino)'}
```

## Referencias
- CENTRUM PUCP. (2017). IBM Perú y su Transformación Digital en la Era Cognitiva – XII Semana Internacional. YouTube.  
- DW Español. (2021). La ciudad que lo sabe todo sobre ti | Big Data: ciudades del futuro. YouTube.  

Autores:  
Estiven G.G
