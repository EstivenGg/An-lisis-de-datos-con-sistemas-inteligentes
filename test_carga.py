# test_carga.py
from server import crear_producto, listar_productos

def main():
    # Productos de ejemplo con pH
    ejemplos = [
        {"nombre": "Tomate", "categoria": "Hortalizas", "cantidad": 50, "precio": 1.2, "ph": 6.2},
        {"nombre": "Lechuga", "categoria": "Hortalizas", "cantidad": 80, "precio": 0.9, "ph": 5.6},
        {"nombre": "Fresa", "categoria": "Frutas", "cantidad": 40, "precio": 2.5, "ph": 3.5},
        {"nombre": "Pepino", "categoria": "Hortalizas", "cantidad": 60, "precio": 1.1, "ph": 7.0},
        {"nombre": "Arándano", "categoria": "Frutas", "cantidad": 30, "precio": 3.2, "ph": 5.9},
    ]

    print("=== Creación de productos ===")
    for it in ejemplos:
        res = crear_producto(**it)
        print(res["producto"])

    lista = listar_productos()
    print("\n=== Listado total ===")
    for item in lista["productos"]:
        print(item)

if __name__ == "__main__":
    main()
