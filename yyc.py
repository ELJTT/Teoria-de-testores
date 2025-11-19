import numpy as np
import time
import math
import random

class AlgoritmoYYC:
    """Implementación del algoritmo YYC con interfaz amigable"""
    
    def __init__(self):
        self.tiempo_acumulado = 0.0
        self.testores_por_fila = []
    
    def matriz_es_admisible(self, matriz):
        """Verifica si una matriz es binaria y con filas del mismo tamaño."""
        if not matriz:
            return False
            
        n_columnas = len(matriz[0])
        for i, fila in enumerate(matriz):
            if len(fila) != n_columnas:
                print(f" Error: Fila {i+1} tiene longitud diferente")
                return False
            if any(valor not in (0, 1) for valor in fila):
                print(f" Error: Fila {i+1} contiene valores no binarios")
                return False
        return True
    
    def es_superfila(self, fila1, fila2):
        """Retorna True si fila1 es superfila de fila2."""
        for a, b in zip(fila1, fila2):
            if a == 1 and b == 0:
                return False
        return True
    
    def matriz_basica(self, matriz):
        """Reduce la matriz eliminando filas dominadas."""
        filas_a_eliminar = []
        n_filas = len(matriz)
        
        for i in range(n_filas):
            if sum(matriz[i]) == 0:  # Fila de ceros
                filas_a_eliminar.append(i)
                continue
                
            for j in range(n_filas):
                if i != j and j not in filas_a_eliminar:
                    if self.es_superfila(matriz[i], matriz[j]):
                        filas_a_eliminar.append(j)
        
        matriz_basica = [fila for i, fila in enumerate(matriz) 
                        if i not in filas_a_eliminar]
        
        print(f" Matriz básica: {len(matriz_basica)} filas de {n_filas} originales")
        return matriz_basica
    
    def submatriz_compatible(self, submatriz):
        """Verifica si una submatriz es compatible."""
        if len(submatriz) == 0 or len(submatriz[0]) == 0:
            return False
            
        # Filtrar filas que tienen exactamente un 1
        filas_con_un_uno = [fila for fila in submatriz if sum(fila) == 1]
        
        if len(filas_con_un_uno) < len(submatriz[0]):
            return False
            
        # Verificar que cada columna tenga al menos un 1
        suma_columnas = [sum(col) for col in zip(*filas_con_un_uno)]
        return all(suma >= 1 for suma in suma_columnas)
    
    def crear_matriz_testores(self, testores, n_columnas):
        """Crea la matriz de testores en formato binario."""
        matriz_testores = []
        for testor in testores:
            fila = [0] * n_columnas
            for caracteristica in testor:
                fila[caracteristica] = 1
            matriz_testores.append(fila)
        return matriz_testores
    
    def yyc(self, matriz):
        """Algoritmo YYC con medición de tiempo por fila."""
        print("\n" + "="*60)
        print("ALGORITMO YYC - INICIANDO EJECUCIÓN")
        print("="*60)
        
        # Verificar admisibilidad
        if not self.matriz_es_admisible(matriz):
            print(" La matriz no es admisible")
            return []
        
        print(" Matriz admisible verificada")
        print(f" Dimensiones: {len(matriz)} filas × {len(matriz[0])} columnas")
        
        # Reducir a matriz básica
        matriz_basica = self.matriz_basica(matriz)
        matriz_np = np.array(matriz_basica)
        n_columnas_original = len(matriz[0])
        
        print("\n" + "-"*40)
        print("MATRIZ BÁSICA:")
        for i, fila in enumerate(matriz_basica):
            print(f"Fila {i+1}: {fila}")
        print("-"*40)
        
        # Reiniciar contadores
        self.tiempo_acumulado = 0.0
        self.testores_por_fila = []
        
        # Inicializar testores con características de la primera fila
        testores_actuales = []
        for col in range(len(matriz_np[0])):
            if matriz_np[0][col] == 1:
                testores_actuales.append([col])
        
        self.testores_por_fila.append(testores_actuales.copy())
        
        print(f"\n TESTORES INICIALES (después de fila 1):")
        for i, testor in enumerate(testores_actuales):
            print(f"  Testor {i+1}: {testor}")
        print(f"⏱ Tiempo acumulado: 0.000000 s")
        
        # Procesar filas restantes
        for fila_idx in range(1, len(matriz_np)):
            inicio_tiempo = time.time()
            
            fila_actual = matriz_np[fila_idx]
            print(f"\n{'='*50}")
            print(f"PROCESANDO FILA {fila_idx + 1}: {fila_actual}")
            print(f"{'='*50}")
            
            idx_testor = 0
            while idx_testor < len(testores_actuales):
                testor = testores_actuales[idx_testor]
                
                # Verificar si el testor actual cubre la fila
                cubre_fila = any(fila_actual[caracteristica] == 1 
                               for caracteristica in testor)
                
                if cubre_fila:
                    print(f"   Testor {testor} cubre la fila")
                    idx_testor += 1
                    continue
                
                print(f"   Testor {testor} NO cubre la fila. Buscando ampliaciones...")
                
                # Buscar ampliaciones válidas
                nuevas_ampliaciones = []
                for nueva_caracteristica in range(len(fila_actual)):
                    if (fila_actual[nueva_caracteristica] == 1 and 
                        nueva_caracteristica not in testor):
                        
                        nuevo_testor = sorted(testor + [nueva_caracteristica])
                        
                        # Verificar compatibilidad de la submatriz
                        submatriz = matriz_np[:fila_idx+1, nuevo_testor]
                        if self.submatriz_compatible(submatriz):
                            print(f"     Ampliación válida: {testor} → {nuevo_testor}")
                            nuevas_ampliaciones.append(nuevo_testor)
                
                # Actualizar testores
                if nuevas_ampliaciones:
                    testores_actuales[idx_testor:idx_testor+1] = nuevas_ampliaciones
                    idx_testor += len(nuevas_ampliaciones)
                else:
                    print(f"    🗑 Eliminando testor {testor} (sin ampliaciones válidas)")
                    del testores_actuales[idx_testor]
            
            # Calcular tiempo de esta fila
            tiempo_fila = time.time() - inicio_tiempo
            self.tiempo_acumulado += tiempo_fila
            self.testores_por_fila.append(testores_actuales.copy())
            
            # Mostrar resultados de esta fila
            print(f"\n RESULTADOS FILA {fila_idx + 1}:")
            print(f"  Testores actuales: {len(testores_actuales)}")
            for i, testor in enumerate(testores_actuales):
                print(f"    Testor {i+1}: {testor}")
            print(f"⏱ Tiempo esta fila: {tiempo_fila:.6f} s")
            print(f"⏱ Tiempo acumulado: {self.tiempo_acumulado:.6f} s")
        
        # Resultados finales
        print("\n" + "="*60)
        print(" EJECUCIÓN COMPLETADA - TESTORES TÍPICOS FINALES")
        print("="*60)
        
        # Mostrar matriz de testores
        matriz_testores = self.crear_matriz_testores(testores_actuales, n_columnas_original)
        self.mostrar_matriz_testores(matriz_testores)
        
        # Mostrar resumen
        self.mostrar_resumen_ejecucion()
        
        return testores_actuales
    
    def mostrar_matriz_testores(self, matriz_testores):
        """Muestra la matriz de testores en formato binario."""
        print(f"\n{'='*60}")
        print(" MATRIZ DE TESTORES TÍPICOS (Formato Binario)")
        print(f"{'='*60}")
        print("NOTA: Los testores típicos son los de la ÚLTIMA fila del proceso")
        print("      (después de procesar todas las filas de la matriz original)")
        print(f"{'-'*60}")
        
        if not matriz_testores:
            print("No se encontraron testores típicos")
            return
            
        n_columnas = len(matriz_testores[0])
        
        # Encabezado de columnas
        encabezado = "     " + " ".join(f"x{i}" for i in range(n_columnas))
        print(encabezado)
        
        # Filas de la matriz de testores
        for i, fila in enumerate(matriz_testores):
            fila_str = " ".join(f" {valor} " for valor in fila)
            print(f"T{i+1}:  [{fila_str}]")
        
        print(f"{'-'*60}")
        print(f"Total: {len(matriz_testores)} testores típicos encontrados")
        print(f"{'='*60}")
    
    def mostrar_resumen_ejecucion(self):
        """Muestra el resumen completo de la ejecución."""
        print(f"\n RESUMEN DETALLADO DE EJECUCIÓN:")
        print(f"{'='*50}")
        print(f"⏱ Tiempo total: {self.tiempo_acumulado:.6f} segundos")
        print(f" Evolución de testores por fila procesada:")
        print(f"{'-'*50}")
        
        for i, testores in enumerate(self.testores_por_fila):
            print(f"\n📍 Después de fila {i+1}: {len(testores)} testores")
            for j, testor in enumerate(testores):
                print(f"    Testor {j+1}: {testor}")
        
        print(f"\n{'='*50}")
        print(" IMPORTANTE: Los TESTORES TÍPICOS FINALES son")
        print(f"   los de la ÚLTIMA fila (fila {len(self.testores_por_fila)})")
        print(f"{'='*50}")
        
        testores_finales = self.testores_por_fila[-1]
        print(f"\n TESTORES TÍPICOS FINALES ({len(testores_finales)}):")
        for i, testor in enumerate(testores_finales):
            print(f"  {i+1}. Características: {testor}")
            # Mostrar en formato binario
            binario = ["1" if j in testor else "0" for j in range(max(testor) + 1 if testor else 0)]
            print(f"     Formato binario: [{', '.join(binario)}]")


class GeneradorMatrices:
    """Generador de matrices booleanas para testing"""
    
    @staticmethod
    def generar_matriz_aleatoria(filas, columnas, densidad_minima=0.5):
        """Genera una matriz booleana aleatoria con densidad mínima."""
        if columnas < 6:
            raise ValueError("Se requieren al menos 6 columnas")
        
        total_elementos = filas * columnas
        unos_necesarios = math.ceil(total_elementos * densidad_minima)
        ceros_necesarios = total_elementos - unos_necesarios
        
        elementos = [1] * unos_necesarios + [0] * ceros_necesarios
        random.shuffle(elementos)
        
        matriz = np.array(elementos).reshape(filas, columnas).tolist()
        
        print(f" Matriz generada: {filas}×{columnas}")
        print(f" Densidad: {unos_necesarios/total_elementos:.2f}")
        
        return matriz
    
    @staticmethod
    def ingresar_matriz_manual():
        """Permite al usuario ingresar una matriz manualmente."""
        print("\n INGRESO MANUAL DE MATRIZ")
        filas = int(input("Número de filas: "))
        columnas = int(input("Número de columnas: "))
        
        matriz = []
        print("Ingrese cada fila (valores separados por espacios, solo 0 y 1):")
        
        for i in range(filas):
            while True:
                try:
                    entrada = input(f"Fila {i+1}: ")
                    valores = list(map(int, entrada.split()))
                    
                    if len(valores) != columnas:
                        print(f" Error: debe ingresar exactamente {columnas} valores")
                        continue
                    
                    if any(valor not in (0, 1) for valor in valores):
                        print("Error: solo se permiten 0 y 1")
                        continue
                    
                    matriz.append(valores)
                    break
                    
                except ValueError:
                    print(" Error: ingrese solo números enteros")
        
        return matriz
    
    @staticmethod
    def mostrar_matriz(matriz, titulo="MATRIZ"):
        """Muestra una matriz de forma legible."""
        print(f"\n{titulo}:")
        if not matriz:
            print("  (vacía)")
            return
            
        # Mostrar encabezado de columnas
        if matriz:
            n_columnas = len(matriz[0])
            encabezado = "     " + " ".join(f"x{i}" for i in range(n_columnas))
            print(encabezado)
            print("     " + "-" * (n_columnas * 3 - 1))
            
        for i, fila in enumerate(matriz):
            fila_str = " ".join(f" {valor} " for valor in fila)
            print(f"F{i+1}:  [{fila_str}]")


def menu_principal():
    """Menú principal interactivo."""
    yyc = AlgoritmoYYC()
    generador = GeneradorMatrices()
    matriz_actual = None
    
    while True:
        print("\n" + "="*50)
        print("        ALGORITMO YYC - MENÚ PRINCIPAL")
        print("="*50)
        print("1.  Ingresar matriz manualmente")
        print("2.  Generar matriz aleatoria (densidad ≥ 0.5)")
        print("3.  Ejecutar algoritmo YYC")
        print("4.  Mostrar matriz actual")
        print("5.  Salir")
        print("-"*50)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            matriz_actual = generador.ingresar_matriz_manual()
            generador.mostrar_matriz(matriz_actual, "MATRIZ INGRESADA")
            
        elif opcion == "2":
            try:
                filas = int(input("Número de filas: "))
                columnas = int(input("Número de columnas (mínimo 6): "))
                matriz_actual = generador.generar_matriz_aleatoria(filas, columnas)
                generador.mostrar_matriz(matriz_actual, "MATRIZ ALEATORIA GENERADA")
            except Exception as e:
                print(f" Error: {e}")
                
        elif opcion == "3":
            if matriz_actual is None:
                print(" Primero cargue una matriz")
            else:
                generador.mostrar_matriz(matriz_actual, "MATRIZ A PROCESAR")
                input("\nPresione Enter para ejecutar YYC...")
                testores = yyc.yyc(matriz_actual)
                
        elif opcion == "4":
            if matriz_actual is not None:
                generador.mostrar_matriz(matriz_actual, "MATRIZ ACTUAL")
            else:
                print(" No hay matriz cargada")
            
        elif opcion == "5":
            print(" ¡CIAO!")
            break
            
        else:
            print(" Opción inválida. Intente nuevamente.")
#matenme :,(

# Ejecución principal
if __name__ == "__main__":
    print(" IMPLEMENTACIÓN DEL ALGORITMO YYC")
    print("   Con medición de tiempo acumulado por fila")
    print("   y visualización de matriz de testores")
    menu_principal()
