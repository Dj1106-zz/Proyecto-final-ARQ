import random
import time

class DispositivoIO:
    def __init__(self):
        self.interrupcion = False
        self.estado = "INACTIVO"  # Estados posibles: INACTIVO, OCUPADO, ERROR

    def leer_datos(self):
        # Simula lectura de un dispositivo ficticio con latencia
        self.estado = "OCUPADO"
        time.sleep(0.1)  # Retraso de 100ms para simular latencia
        try:
            datos = random.randint(0, 255)
            self.interrupcion = True
            self.estado = "INACTIVO"
            return datos
        except Exception as e:
            self.estado = "ERROR"
            self.interrupcion = True
            raise RuntimeError(f"Error al leer datos: {e}")

    def limpiar_interrupcion(self):
        self.interrupcion = False

    def tiene_interrupcion(self):
        return self.interrupcion

    def obtener_estado(self):
        return self.estado