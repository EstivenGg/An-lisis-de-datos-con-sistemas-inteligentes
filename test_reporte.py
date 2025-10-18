# test_reporte.py
from server import reporte_estado

def main():
    # Reporte en español
    print("=== Reporte del invernadero (ES) ===")
    rep_es = reporte_estado(idioma="es")
    print(rep_es["resumen"])
    for it in rep_es["productos"]:
        print(it)
        
if __name__ == "__main__":
    main()
