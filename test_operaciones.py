# test_operaciones.py
from server import consultar_producto, actualizar_producto, eliminar_producto, listar_productos

def main():
    lista = listar_productos()
    if not lista["productos"]:
        print("No hay productos. Ejecuta primero test_carga.py")
        return

    primer_id = lista["productos"][0]["id"]

    # Consultar
    print("=== Consultar producto ===")
    print(consultar_producto(primer_id))

    # Actualizar
    print("\n=== Actualizar producto ===")
    print(actualizar_producto(primer_id, cantidad=100, ph=6.0))

    # Eliminar último producto
    ultimo_id = lista["productos"][-1]["id"]
    print("\n=== Eliminar producto ===")
    print(eliminar_producto(ultimo_id))

    # Listar final
    print("\n=== Listado final ===")
    print(listar_productos())

if __name__ == "__main__":
    main()
