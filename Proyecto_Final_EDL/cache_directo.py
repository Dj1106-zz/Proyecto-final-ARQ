class CacheMapeoDirecto:
    def __init__(self, num_lineas=8, tamano_bloque=4):
        self.num_lineas = num_lineas
        self.tamano_bloque = tamano_bloque
        self.cache = [{"etiqueta": None, "valido": False} for _ in range(num_lineas)]
        self.aciertos = 0
        self.fallos = 0
        self.registro_accesos = []

    def acceder(self, direccion, escritura=False, mostrar=True):
        if direccion < 0:
            raise ValueError("La dirección no puede ser negativa.")

        numero_bloque = direccion // self.tamano_bloque
        indice_linea = numero_bloque % self.num_lineas
        etiqueta = numero_bloque
        operacion = "ESCRITURA" if escritura else "LECTURA"

        if self.cache[indice_linea]["valido"] and self.cache[indice_linea]["etiqueta"] == etiqueta:
            self.aciertos += 1
            mensaje = f"[{operacion}] ACIERTO en línea {indice_linea}"
            self.registro_accesos.append(f"{operacion}: ACIERTO en línea {indice_linea}")
        else:
            self.fallos += 1
            mensaje = f"[{operacion}] FALLO en línea {indice_linea}. Cargando bloque {etiqueta}..."
            self.registro_accesos.append(f"{operacion}: FALLO en línea {indice_linea} -> Cargar bloque {etiqueta}")
            self.cache[indice_linea]["etiqueta"] = etiqueta
            self.cache[indice_linea]["valido"] = True

        if mostrar:
            print(mensaje)

    def estadisticas(self):
        total = self.aciertos + self.fallos
        tasa_acierto = self.aciertos / total if total > 0 else 0

        print("\n=== Estadísticas de Caché ===")
        print(f"Accesos totales: {total}")
        print(f"Aciertos: {self.aciertos}")
        print(f"Fallos: {self.fallos}")
        print(f"Tasa de acierto: {tasa_acierto:.2%}")

    def exportar_estadisticas(self, nombre_archivo='cache_directo_estadisticas.txt'):
        total = self.aciertos + self.fallos
        tasa_acierto = self.aciertos / total if total > 0 else 0

        with open(nombre_archivo, 'w') as archivo:
            archivo.write("=== Estadísticas de Caché ===\n")
            archivo.write(f"Accesos totales: {total}\n")
            archivo.write(f"Aciertos: {self.aciertos}\n")
            archivo.write(f"Fallos: {self.fallos}\n")
            archivo.write(f"Tasa de acierto: {tasa_acierto:.2%}\n")
            archivo.write("\n--- Registro de accesos ---\n")
            for linea in self.registro_accesos:
                archivo.write(linea + '\n')

        print(f"\n📄 Estadísticas exportadas a '{nombre_archivo}'")