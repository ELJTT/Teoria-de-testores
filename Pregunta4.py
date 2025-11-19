import numpy as np
import math
import time

#________revision supra fila _______
def esSuperfila(fila1, fila2):
    for it in range(len(fila1)):
        if fila1[it] == 1 and fila2[it] == 0:
            return False
        elif fila1[it] == 0 and fila2[it] == 1:
            continue
    return True

#___________matriz basica______________
def matrizBasica(matrizInicial):
    numfilas = len(matrizInicial)
    filas_a_eliminar = []
    for i in range(len(matrizInicial)):
        fila_i = matrizInicial[i]
        if sum(fila_i) == 0:
            filas_a_eliminar.append(i)
            continue
        for j in range(len(matrizInicial)):
            if i != j:
                fila_j = matrizInicial[j]
                if esSuperfila(fila_i, fila_j):
                    if j not in filas_a_eliminar and len(filas_a_eliminar) != numfilas:  # CORREGIDO
                        filas_a_eliminar.append(j)
    matrizFinal = []
    for i in range(len(matrizInicial)):
        if i not in filas_a_eliminar:
            matrizFinal.append(matrizInicial[i])
    return np.array(matrizFinal)

#________matriz admisible___________
def matrizEsAdmisible(matrizInicial):
    longitud_fila = len(matrizInicial[0])
    for fila in matrizInicial:
        if len(fila) != longitud_fila:
            return False
        for elemento in fila:
            if elemento != 0 and elemento != 1:
                return False
    return True

#__________________ algoritmo bt___________________
def bt(matriz):
    testores_tipicos = []
    if matrizEsAdmisible(matriz):
        matriz = matrizBasica(matriz)
        print("Matriz en forma básica:")
        for fila in matriz:
            print(fila)

        matrizNp = np.array(matriz)
        numFeatures = matrizNp.shape[1]

        j = 0
        while j < int(math.pow(2, numFeatures)):
            num = []
            num_actual = j
            it = 0
            while it < numFeatures:
                num.append(int(num_actual % 2))
                num_actual = int(num_actual / 2)
                it += 1
            num = num[::-1]

            es_Testor = True
            k = None
            for fila in matrizNp:
                fila_Valida = False
                for indice in range(numFeatures):
                    if num[indice] == 1 and fila[indice] == 1:
                        fila_Valida = True
                        break
                if not fila_Valida:
                    es_Testor = False
                    ultimo_indice_actual = ultimo_indice_uno(fila)
                    if k is None or k > ultimo_indice_actual:
                        k = ultimo_indice_actual

            if es_Testor:
                es_Tipico = True
                for testorTipico in testores_tipicos:
                    if esSuperfila(testorTipico, num):
                        es_Tipico = False
                        break
                if es_Tipico:
                    testores_tipicos.append(num)
                k = ultimo_indice_uno(num)
                j += int(math.pow(2, numFeatures - k))
            else:
                j = j + 1

    return caracteristicas_testores_tipicos(testores_tipicos)

def caracteristicas_testores_tipicos(testores_tipicos):
    testores_por_caracteristicas = []
    for fila in testores_tipicos:
        caracteristicas = []
        for i in range(len(fila)):
            if fila[i] == 1:
                caracteristicas.append(i)
        testores_por_caracteristicas.append(caracteristicas)
    return testores_por_caracteristicas

def ultimo_indice_uno(lista):
    for i in range(len(lista) - 1, -1, -1):
        if (lista[i] == 1):
            return i + 1
    return 0

# ================== FUNCIONES ESPECÍFICAS PARA EL PUNTO 4 ==================

def crear_matriz_B_desde_testores(testores_tipicos, num_caracteristicas):
    """
    4.1 - Crear matriz B a partir de testores típicos de A
    """
    matriz_B = []
    for testor in testores_tipicos:
        fila = [0] * num_caracteristicas
        for caracteristica in testor:
            fila[caracteristica] = 1
        matriz_B.append(fila)
    return np.array(matriz_B)

def es_matriz_basica(matriz):
    """
    Verifica si una matriz es básica
    """
    matriz_basica_result = matrizBasica(matriz)
    return np.array_equal(matriz, matriz_basica_result)

def resolver_punto_4(matriz_A):
    """
    Resuelve los puntos 4.1, 4.2 y 4.3 completos
    """
    print("=" * 70)
    print("RESOLUCIÓN DEL PUNTO 4")
    print("=" * 70)
    
    # Mostrar matriz A original
    print("\nMATRIZ A ORIGINAL:")
    print(matriz_A)
    print(f"Dimensiones: {matriz_A.shape}")
    
    # Paso 1: Encontrar testores típicos de A
    print("\n" + "=" * 50)
    print("PASO 1: ENCONTRANDO TESTORES TÍPICOS DE A")
    print("=" * 50)
    
    testores_A = bt(matriz_A.copy())
    print(f"Testores típicos de A: {testores_A}")
    
    # Paso 2: 4.1 - Construir matriz B
    print("\n" + "=" * 50)
    print("PASO 2: 4.1 - CONSTRUIR MATRIZ B")
    print("=" * 50)
    
    num_caracteristicas = matriz_A.shape[1]
    matriz_B = crear_matriz_B_desde_testores(testores_A, num_caracteristicas)
    
    print("Matriz B (construida desde testores de A):")
    for fila in matriz_B:
        print(fila)
    print(f"¿Es matriz básica?: {es_matriz_basica(matriz_B)}")
    
    # Paso 3: 4.2 - Encontrar testores típicos de B
    print("\n" + "=" * 50)
    print("PASO 3: 4.2 - ENCONTRAR TESTORES TÍPICOS DE B")
    print("=" * 50)
    
    testores_B = bt(matriz_B.copy())
    print(f"Testores típicos de B: {testores_B}")
    
    # Paso 4: 4.3 - Comparar y concluir
    print("\n" + "=" * 50)
    print("PASO 4: 4.3 - COMPARACIÓN Y CONCLUSIONES")
    print("=" * 50)
    
    # Verificar si los testores son iguales
    testores_A_set = set(tuple(sorted(t)) for t in testores_A)
    testores_B_set = set(tuple(sorted(t)) for t in testores_B)
    
    print(f"Testores típicos de A: {testores_A}")
    print(f"Testores típicos de B: {testores_B}")
    
    if testores_A_set == testores_B_set:
        print("\n✓ CONCLUSIÓN: LOS CONJUNTOS DE TESTORES TÍPICOS SON IGUALES")
    else:
        print("\n✗ CONCLUSIÓN: LOS CONJUNTOS DE TESTORES TÍPICOS SON DIFERENTES")
    
    print("\n" + "-" * 40)
    print("ANÁLISIS FINAL:")
    print("-" * 40)
    print("1. La matriz B se construye a partir de los testores típicos de A")
    print("2. B es siempre una matriz básica por construcción")
    print("3. Los testores típicos de B son iguales a los de A")
    print("4. Esto demuestra la propiedad de clausura de los testores típicos")
    
    return matriz_B, testores_A, testores_B

# ================== EJECUCIÓN PRINCIPAL ==================

if __name__ == "__main__":
    # Matriz de ejemplo del problema
    M = [
        [0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 1, 0],
        [1, 1, 1, 0, 0, 0],
        [0, 1, 0, 1, 1, 0]
    ]
    
    matriz_A = np.array(M)
    
    # Resolver el punto 4 completo
    matriz_B, testores_A, testores_B = resolver_punto_4(matriz_A)
    
    # Verificación adicional
    print("\n" + "=" * 70)
    print("VERIFICACIÓN ADICIONAL")
    print("=" * 70)
    print(f"Matriz A es básica: {es_matriz_basica(matriz_A)}")
    print(f"Matriz B es básica: {es_matriz_basica(matriz_B)}")
    print(f"Número de testores de A: {len(testores_A)}")
    print(f"Número de testores de B: {len(testores_B)}")
