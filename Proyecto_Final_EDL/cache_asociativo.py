class CacheAsociativa2Vias:
    def __init__(self, num_conjuntos=4, tamano_bloque=4):
        self.num_conjuntos = num_conjuntos
        self.tamano_bloque = tamano_bloque
        self.cache = [[{"etiqueta": None, "valido": False}, {"etiqueta": None, "valido": False}] for _ in range(num_conjuntos)]
        self.lru = [0] * num_conjuntos  # 0: vía 0 es más reciente, 1: vía 1 lo es
        self.aciertos = 0
        self.fallos = 0
        self.registro_accesos = []

    def acceder(self, direccion, escritura=False, mostrar=True):
        if direccion < 0:
            raise ValueError("La dirección no puede ser negativa.")

        numero_bloque = direccion // self.tamano_bloque
        indice_conjunto = numero_bloque % self.num_conjuntos
        etiqueta = numero_bloque

        via0, via1 = self.cache[indice_conjunto]
        operacion = "ESCRITURA" if escritura else "LECTURA"

        if (via0["valido"] and via0["etiqueta"] == etiqueta) or (via1["valido"] and via1["etiqueta"] == etiqueta):
            self.aciertos += 1
            via_acierto = 0 if (via0["valido"] and via0["etiqueta"] == etiqueta) else 1
            self.lru[indice_conjunto] = via_acierto
            mensaje = f"[{operacion}] ACIERTO en conjunto {indice_conjunto}, vía {via_acierto}"
            self.registro_accesos.append(f"{operacion}: ACIERTO en conjunto {indice_conjunto}, vía {via_acierto}")
        else:
            self.fallos += 1
            victima = self.lru[indice_conjunto]
            self.cache[indice_conjunto][victima]["etiqueta"] = etiqueta
            self.cache[indice_conjunto][victima]["valido"] = True
            self.lru[indice_conjunto] = 1 - victima
            mensaje = f"[{operacion}] FALLO en conjunto {indice_conjunto}. Reemplazando en vía {victima}"
            self.registro_accesos.append(f"{operacion}: FALLO en conjunto {indice_conjunto} -> Reemplazo en vía {victima}, nueva etiqueta {etiqueta}")

        if mostrar:
            print(mensaje)

    def estadisticas(self):
        total = self.aciertos + self.fallos
        tasa_acierto = self.aciertos / total if total > 0 else 0

        print("\n=== Estadísticas de Caché 2-Vías ===")
        print(f"Accesos totales: {total}")
        print(f"Aciertos: {self.aciertos}")
        print(f"Fallos: {self.fallos}")
        print(f"Tasa de acierto: {tasa_acierto:.2%}")

    def exportar_estadisticas(self, nombre_archivo='cache_asociativa_estadisticas.txt'):
        total = self.aciertos + self.fallos
        tasa_acierto = self.aciertos / total if total > 0 else 0

        with open(nombre_archivo, 'w') as archivo:
            archivo.write("=== Estadísticas de Caché 2-Vías ===\n")
            archivo.write(f"Accesos totales: {total}\n")
            archivo.write(f"Aciertos: {self.aciertos}\n")
            archivo.write(f"Fallos: {self.fallos}\n")
            archivo.write(f"Tasa de acierto: {tasa_acierto:.2%}\n")
            archivo.write("\n--- Registro de accesos ---\n")
            for linea in self.registro_accesos:
                archivo.write(linea + '\n')

        print(f"\n📄 Estadísticas exportadas a '{nombre_archivo}'")