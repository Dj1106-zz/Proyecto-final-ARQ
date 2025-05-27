from cache_directo import CacheMapeoDirecto

def benchmark_secuencial():
    cache = CacheMapeoDirecto(num_lineas=8, tamano_bloque=4)
    direcciones = [0, 4, 8, 0, 16, 20, 24, 8, 32, 0]

    for direccion in direcciones:
        print(f"\nAccediendo a dirección {direccion}")
        cache.acceder(direccion)

    print("\n=== Estadísticas de la Caché ===")
    cache.estadisticas()

def main():
    try:
        benchmark_secuencial()
    except Exception as e:
        print(f"Error durante el benchmark: {e}")

if __name__ == "__main__":
    main()