import numpy as np
import time
import math
import random

class AlgoritmoBT:
    """Implementación del algoritmo BT con interfaz amigable"""
    
    def __init__(self):
        self.tiempo_acumulado = 0.0
        self.iteraciones_por_paso = []
        self.testores_encontrados = []
    
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
    
    def ultimo_indice_uno(self, lista):
        """Encuentra el último índice donde hay un 1 (1-based)."""
        for i in range(len(lista)-1, -1, -1):
            if lista[i] == 1:
                return i + 1
        return 0
    
    def crear_matriz_testores(self, testores, n_columnas):
        """Crea la matriz de testores en formato binario."""
        matriz_testores = []
        for testor in testores:
            fila = [0] * n_columnas
            for caracteristica in testor:
                fila[caracteristica] = 1
            matriz_testores.append(fila)
        return matriz_testores
    
    def mostrar_n_uplo(self, n_uplo, iteracion):
        """Muestra un n-uplo de forma legible."""
        binario = "".join(str(bit) for bit in n_uplo)
        decimal = int(binario, 2)
        return f"{decimal:0{len(n_uplo)}b} ({decimal})"
    
    def bt(self, matriz):
        """Algoritmo BT con medición detallada de tiempo y progreso."""
        print("\n" + "="*60)
        print("ALGORITMO BT - INICIANDO EJECUCIÓN")
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
        num_features = matriz_np.shape[1]
        
        print("\n" + "-"*40)
        print("MATRIZ BÁSICA:")
        for i, fila in enumerate(matriz_basica):
            print(f"Fila {i+1}: {fila}")
        print("-"*40)
        
        # Reiniciar contadores
        self.tiempo_acumulado = 0.0
        self.iteraciones_por_paso = []
        self.testores_encontrados = []
        
        total_iteraciones = 2 ** num_features
        print(f"\n Buscando en {total_iteraciones} n-uplos posibles")
        print(f" Progreso estimado: 0%")
        
        j = 1  # Empezar desde 1 (000...001) ya que 000...000 nunca es testor
        iteracion_actual = 0
        
        while j < total_iteraciones:
            inicio_iteracion = time.time()
            iteracion_actual += 1
            
            # Convertir número a n-uplo binario
            n_uplo = [(j >> (num_features - 1 - k)) & 1 for k in range(num_features)]
            
            print(f"\n{'─'*50}")
            print(f" ITERACIÓN {iteracion_actual}")
            print(f" N-uplo actual: {self.mostrar_n_uplo(n_uplo, iteracion_actual)}")
            print(f" Progreso: {j}/{total_iteraciones} ({j/total_iteraciones*100:.1f}%)")
            
            # Verificar si es testor
            es_testor = True
            k_valor = None
            
            for i, fila in enumerate(matriz_np):
                cubre_fila = False
                for idx in range(num_features):
                    if n_uplo[idx] == 1 and fila[idx] == 1:
                        cubre_fila = True
                        break
                
                if not cubre_fila:
                    es_testor = False
                    ultimo_idx = self.ultimo_indice_uno(fila)
                    if k_valor is None or ultimo_idx < k_valor:
                        k_valor = ultimo_idx
                    print(f"    No cubre fila {i+1}: {fila}")
            
            if es_testor:
                print(f"    ES TESTOR - Verificando tipicidad...")
                
                # Verificar si es típico
                es_tipico = True
                for testor_existente in self.testores_encontrados:
                    if self.es_superfila(testor_existente, n_uplo):
                        es_tipico = False
                        print(f"     NO es típico (superconjunto de {testor_existente})")
                        break
                
                if es_tipico:
                    caracteristicas = [i for i, bit in enumerate(n_uplo) if bit == 1]
                    self.testores_encontrados.append(n_uplo.copy())
                    print(f"    TESTOR TÍPICO ENCONTRADO: {caracteristicas}")
                    print(f"    Características: {caracteristicas}")
                
                # Calcular salto
                k_salto = self.ultimo_indice_uno(n_uplo)
                salto = 2 ** (num_features - k_salto)
                print(f"    Salto calculado: {salto} posiciones")
                j += salto
                
            else:
                # No es testor - calcular próximo n-uplo
                if k_valor is not None:
                    # Construir próximo n-uplo según reglas BT
                    proximo_n_uplo = []
                    for idx in range(num_features):
                        if (idx + 1) < k_valor:
                            proximo_n_uplo.append(n_uplo[idx])
                        elif (idx + 1) == k_valor:
                            proximo_n_uplo.append(1)
                        else:
                            proximo_n_uplo.append(0)
                    
                    # Convertir a decimal para el salto
                    proximo_binario = "".join(str(bit) for bit in proximo_n_uplo)
                    proximo_j = int(proximo_binario, 2)
                    salto = proximo_j - j
                    print(f"    Próximo n-uplo: {self.mostrar_n_uplo(proximo_n_uplo, 0)}")
                    print(f"    Salto: {salto} posiciones")
                    j += salto
                else:
                    j += 1
            
            # Calcular tiempo de esta iteración
            tiempo_iteracion = time.time() - inicio_iteracion
            self.tiempo_acumulado += tiempo_iteracion
            
            # Guardar información de la iteración
            info_iteracion = {
                'iteracion': iteracion_actual,
                'n_uplo': n_uplo.copy(),
                'es_testor': es_testor,
                'tiempo': tiempo_iteracion,
                'testores_encontrados': len(self.testores_encontrados)
            }
            self.iteraciones_por_paso.append(info_iteracion)
            
            print(f" Tiempo iteración: {tiempo_iteracion:.6f} s")
            print(f" Tiempo acumulado: {self.tiempo_acumulado:.6f} s")
            print(f" Testores encontrados: {len(self.testores_encontrados)}")
        
        # Resultados finales
        print("\n" + "="*60)
        print(" EJECUCIÓN COMPLETADA - TESTORES TÍPICOS FINALES")
        print("="*60)
        
        # Mostrar matriz de testores
        testores_caracteristicas = []
        for testor in self.testores_encontrados:
            caracteristicas = [i for i, bit in enumerate(testor) if bit == 1]
            testores_caracteristicas.append(caracteristicas)
        
        matriz_testores = self.crear_matriz_testores(testores_caracteristicas, n_columnas_original)
        self.mostrar_matriz_testores(matriz_testores)
        
        # Mostrar resumen
        self.mostrar_resumen_ejecucion()
        
        return testores_caracteristicas
    
    def mostrar_matriz_testores(self, matriz_testores):
        """Muestra la matriz de testores en formato binario."""
        print(f"\n{'='*60}")
        print(" MATRIZ DE TESTORES TÍPICOS BT (Formato Binario)")
        print(f"{'='*60}")
        print("NOTA: Estos son los testores típicos encontrados por el algoritmo BT")
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
        print(f"\n RESUMEN DETALLADO DE EJECUCIÓN BT:")
        print(f"{'='*50}")
        print(f" Tiempo total: {self.tiempo_acumulado:.6f} segundos")
        print(f" Iteraciones totales: {len(self.iteraciones_por_paso)}")
        print(f" Testores típicos encontrados: {len(self.testores_encontrados)}")
        print(f"{'-'*50}")
        
        print(f"\n Testores típicos finales:")
        for i, testor in enumerate(self.testores_encontrados):
            caracteristicas = [j for j, bit in enumerate(testor) if bit == 1]
            binario = "".join(str(bit) for bit in testor)
            print(f"  {i+1}. Características: {caracteristicas}")
            print(f"     Formato binario: {binario}")

def matriz_basica_densidad_mayor_mitad():
    """Genera una matriz booleana aleatoria con densidad mínima 0.5"""
    print("Bienvenido al sistema de cálculo de testores típicos de una matriz")
    print("Por favor ayúdenos indicando el tamaño de su matriz ingresando el número de filas y columnas. Como regla, debe ingresar mínimo 6 columnas.")
    print("A continuación, el programa generará automáticamente una matriz booleana de densidad mayor o igual a 0.5")

    tamFila = int(input('Ingrese el número de filas: '))
    tamCol = int(input('Ingrese el número de columnas: '))
    
    while tamCol < 6:
        tamCol = int(input('Ingrese de nuevo el número de columnas (mínimo 6): '))

    cantidadValores = tamFila * tamCol
    cantidadUnos = random.randint(math.ceil(cantidadValores/2), cantidadValores)
    print("Su densidad para la matriz será: ", cantidadUnos / cantidadValores)
    cantidadCeros = cantidadValores - cantidadUnos

    while True:
        elementos = [1] * cantidadUnos + [0] * cantidadCeros
        random.shuffle(elementos)

        matrizrand = np.array(elementos).reshape(tamFila, tamCol).tolist()
        matrizbasica = matrizBasica(matrizrand)

        if len(matrizbasica) == tamFila:
            print("Su matriz básica con dicha densidad será:")
            for fila in matrizbasica:
                print(fila)
            return matrizbasica

def ingresar_matriz():
    """Permite al usuario ingresar una matriz manualmente."""
    print("Ingrese los datos de su matriz:")
    filas = int(input("Número de filas: "))
    columnas = int(input("Número de columnas: "))

    matriz = []
    for i in range(filas):
        while True:
            fila = input(f"Fila {i+1} (separada por espacios): ")
            fila = fila.split()
            if len(fila) == columnas:
                fila = list(map(int, fila))
                if all(x in (0,1) for x in fila):
                    matriz.append(fila)
                    break
            print(" Error: Fila inválida. Intente otra vez.")
    return matriz

def matrizBasica(matriz):
    """Reduce la matriz eliminando filas dominadas."""
    eliminar = []
    filas = len(matriz)

    for i in range(filas):
        if sum(matriz[i]) == 0:
            eliminar.append(i)
            continue
        for j in range(filas):
            if i != j and esSuperfila(matriz[i], matriz[j]):
                if j not in eliminar:
                    eliminar.append(j)

    return np.array([fila for i, fila in enumerate(matriz) if i not in eliminar])

def esSuperfila(f1, f2):
    """Retorna True si f1 es superfila de f2."""
    for a, b in zip(f1, f2):
        if a == 1 and b == 0:
            return False
    return True

def mostrar_matriz(M):
    """Muestra la matriz actual de forma legible."""
    if M is None:
        print("\n No hay matriz cargada aún.\n")
        return
    print("\n=== MATRIZ ACTUAL ===")
    for fila in M:
        print(fila)
    print("=====================\n")

# ======================================================
# ===================== MENÚ PRINCIPAL =================
# ======================================================

def menu():
    matriz_actual = None
    bt_algoritmo = AlgoritmoBT()

    while True:
        print("\n" + "="*50)
        print("        ALGORITMO BT - MENÚ PRINCIPAL")
        print("="*50)
        print("1.  Ingresar matriz manualmente")
        print("2.  Generar matriz aleatoria (densidad ≥ 0.5)")
        print("3.  Ejecutar algoritmo BT")
        print("4.  Mostrar matriz actual")
        print("5.  Salir")
        print("-"*50)
        
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            matriz_actual = ingresar_matriz()
            print("\n✔ Matriz cargada correctamente.\n")

        elif opcion == "2":
            matriz_actual = matriz_basica_densidad_mayor_mitad()
            print("\n✔ Matriz aleatoria generada y reducida.\n")

        elif opcion == "3":
            if matriz_actual is None:
                print(" No hay matriz cargada.")
            else:
                print("\n=== EJECUCIÓN DEL ALGORITMO BT ===")
                resultado = bt_algoritmo.bt(matriz_actual)

        elif opcion == "4":
            mostrar_matriz(matriz_actual)

        elif opcion == "5":
            print("\n !CIAO!")
            break

        else:
            print("\n Opción inválida. Intente nuevamente.\n")

# ===================== INICIO =========================
if __name__ == "__main__":
    print(" IMPLEMENTACIÓN DEL ALGORITMO BT")
    print("   Con medición de tiempo y matriz de testores")
    menu()
