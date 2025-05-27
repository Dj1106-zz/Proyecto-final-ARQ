# Clase CPU incluida directamente en main.py
class CPU:
    def __init__(self):
        self.etapas = ["IF", "ID", "EX", "MEM", "WB"]
        self.contador_programa = 0
        self.instrucciones = []
        self.ciclo = 0
        self.estado_pipeline = [None] * len(self.etapas)  # Pipeline state
        self.pipeline_indices = [None] * len(self.etapas)  # Track instruction indices

    def cargar_programa(self, instrucciones):
        self.instrucciones = instrucciones
        self.instruccion_indices = {instr: idx + 1 for idx, instr in enumerate(instrucciones)}

    def ejecutar(self):
        print("=== Simulación de Pipeline ===")
        # Ciclos necesarios considerando posibles riesgos que puedan causar stalls
        ciclos_totales = len(self.instrucciones) + len(self.etapas) - 1
        for i in range(1, len(self.instrucciones)):
            # Detectar riesgos simples (e.g., dependencias entre instrucciones consecutivas)
            if self.instrucciones[i - 1] == self.instrucciones[i]:  # Ejemplo de riesgo
                ciclos_totales += 1  # Añadir un ciclo de stall

        for ciclo in range(ciclos_totales):
            self.ciclo = ciclo
            print(f"\nCiclo {self.ciclo + 1}:")

            # Avanzar el pipeline
            for i in range(len(self.etapas) - 1, 0, -1):
                self.estado_pipeline[i] = self.estado_pipeline[i - 1]
                self.pipeline_indices[i] = self.pipeline_indices[i - 1]

            # IF: buscar nueva instrucción si es posible
            if self.contador_programa < len(self.instrucciones):
                self.estado_pipeline[0] = self.instrucciones[self.contador_programa]
                self.pipeline_indices[0] = self.contador_programa
                self.contador_programa += 1
            else:
                self.estado_pipeline[0] = None
                self.pipeline_indices[0] = None

            # Mostrar solo las etapas ocupadas del pipeline
            hay_instrucciones = False
            for idx, etapa in enumerate(self.etapas):
                instruccion = self.estado_pipeline[idx]
                if instruccion is not None:
                    print(f"  Etapa {etapa}: Instrucción {self.instrucciones.index(instruccion) + 1} ({instruccion})")
                    hay_instrucciones = True
            if not hay_instrucciones:
                print("  (Pipeline vacío)")

# Resto del código de main.py
from cache_directo import CacheMapeoDirecto
from cache_asociativo import CacheAsociativa2Vias
from io_device import DispositivoIO

def main():
    # Instrucciones de ejemplo para la CPU
    instrucciones = ["LOAD A", "ADD B", "STORE C"]

    # Prueba del CPU con pipeline
    print("--- Prueba del CPU con Pipeline ---")
    cpu = CPU()
    cpu.cargar_programa(instrucciones)
    cpu.ejecutar()

    # Prueba de la caché con mapeo directo
    print("\n--- Prueba de Caché con Mapeo Directo ---")
    cache1 = CacheMapeoDirecto()
    for direccion in [0, 4, 8, 0, 16, 20, 24, 8, 32, 0]:
        cache1.acceder(direccion)
    cache1.estadisticas()

    # Prueba de la caché asociativa 2-vías
    print("\n--- Prueba de Caché Asociativa 2-Vías ---")
    cache2 = CacheAsociativa2Vias()
    for direccion in [0, 4, 8, 12, 16, 20, 24, 28, 0, 4]:
        cache2.acceder(direccion)
    cache2.estadisticas()

    # Prueba del dispositivo de E/S
    print("\n--- Prueba del Dispositivo de E/S ---")
    dispositivo = DispositivoIO()
    datos = dispositivo.leer_datos()
    print(f"Datos recibidos del dispositivo: {datos}")
    if dispositivo.tiene_interrupcion():
        print("Interrupción recibida: manejando evento...")
        dispositivo.limpiar_interrupcion()

if __name__ == "__main__":
    main()