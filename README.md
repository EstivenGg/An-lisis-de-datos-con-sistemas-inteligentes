# Análisis de datos con sistemas inteligentes

Este proyecto corresponde a la Actividad 6 – Sistemas Cognitivos basados en Big Data.  
Implementa un servidor MCP (Multi-Command Protocol) en Python con operaciones CRUD sobre una base de datos SQLite para gestionar un inventario agrícola.  

Se agregó la variable pH como parámetro clave en los productos del invernadero y se generaron reportes bilingües (español/inglés) que clasifican el estado de cada producto según su nivel de pH.  

## Características
- CRUD completo sobre productos (crear, consultar, actualizar, eliminar).  
- Base de datos SQLite (inventory.db).  
- Variable pH integrada para control del invernadero.  
- Reportes bilingües (ES/EN) sobre el estado de los productos.  
- Scripts de prueba incluidos.  

## Estructura del proyecto
```
mcp_crud_inventory/
├── database.py         # Inicialización de la base de datos
├── server.py           # Servidor MCP con CRUD y reporte cognitivo
├── test_carga.py       # Script para cargar productos de ejemplo
├── test_operaciones.py # Pruebas de consulta, actualización y eliminación
├── test_reporte.py     # Generación de reportes en español e inglés
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
   venv\Scripts\activate     # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install fastmcp uvicorn
   ```

## Ejecución de pruebas
1. Cargar productos de ejemplo:
   ```bash
   python test_carga.py
   ```
2. Probar operaciones CRUD:
   ```bash
   python test_operaciones.py
   ```
3. Generar reporte bilingüe:
   ```bash
   python test_reporte.py
   ```

## Ejemplo de reporte

Reporte en español (ES):
```json
{
  "resumen": {"total_productos": 4, "rango_ideal": [5.5, 6.5]},
  "productos": [
    {"id": 1, "nombre": "Tomate", "estado": "Óptimo (dentro del rango)", "ph": 6.2}
  ]
}
```

Reporte en inglés (EN):
```json
{
  "summary": {"total_products": 4, "ideal_range": [5.5, 6.5]},
  "products": [
    {"id": 1, "name": "Tomato", "state": "Optimal (within range)", "ph": 6.2}
  ]
}
```

## Referencias
- CENTRUM PUCP. (2017). IBM Perú y su Transformación Digital en la Era Cognitiva – XII Semana Internacional. YouTube.  
- DW Español. (2021). La ciudad que lo sabe todo sobre ti | Big Data: ciudades del futuro. YouTube.  

Autores:  
Estiven G.G