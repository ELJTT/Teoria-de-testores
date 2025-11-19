import numpy as np
import time
import math
import random

def matrizEsAdmisible(matriz):
    """Verifica si una matriz es binaria y con filas del mismo tamaño."""
    n = len(matriz[0])
    for fila in matriz:
        if len(fila) != n:
            print("❌ Error: Las filas no tienen la misma longitud.")
            return False
        if any(x not in (0, 1) for x in fila):
            print("❌ Error: La matriz contiene valores distintos de 0 y 1.")
            return False

    print("✔ La matriz es admisible.")
    return True


def esSuperfila(f1, f2):
    """Retorna True si f1 es superfila de f2."""
    for a, b in zip(f1, f2):
        if a == 1 and b == 0:
            return False
    return True


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


def matrizCompatible(matriz):
    """Verifica compatibilidad (submatriz debe tener suficientes 1s)."""
    matriz = matriz[np.sum(matriz, axis=1) == 1]
    if matriz.shape[0] >= matriz.shape[1]:
        return np.all(np.sum(matriz, axis=0) >= 1)
    return False

def bt(matriz):
    testores = []

    if not matrizEsAdmisible(matriz):
        return []

    matriz = matrizBasica(matriz)
    matrizNp = np.array(matriz)
    numFeatures = matrizNp.shape[1]

    j = 0
    while j < 2 ** numFeatures:

        bits = [(j >> (numFeatures - 1 - k)) & 1 for k in range(numFeatures)]

        esTestor = True
        k = None

        for fila in matrizNp:
            cubre = False
            for ind in range(numFeatures):
                if bits[ind] == 1 and fila[ind] == 1:
                    cubre = True
                    break

            if not cubre:
                esTestor = False
                ultimo = ultimo_indice_uno(fila)
                if k is None or ultimo < k:
                    k = ultimo

        if esTestor:
            esTipico = True
            for t in testores:
                if esSuperfila(t, bits):
                    esTipico = False
                    break

            if esTipico:
                testores.append(bits)

            k = ultimo_indice_uno(bits)
            j += 2 ** (numFeatures - k)

        else:
            j += 1

    return caracteristicas_testores_tipicos(testores)


# ======================================================
# ====================== YYC OPTIMIZADO ================
# ======================================================

def yyc(matriz):
    print("\n=========== EJECUCIÓN DEL ALGORITMO YYC ===========")

    if not matrizEsAdmisible(matriz):
        return []

    # Reducir a matriz básica
    matriz = matrizBasica(matriz)
    matrizNp = np.array(matriz)

    print("\nMatriz en forma básica:")
    for fila in matrizNp:
        print(fila)

    # Inicializar testores con columnas de la fila 1
    testores = [[i] for i in range(len(matrizNp[0])) if matrizNp[0][i] == 1]

    print("\nTestores iniciales:", testores)

    # Tiempo acumulado
    tiempo_acumulado = 0.0

    print("\n============== INICIANDO PROCESO FILA POR FILA ==============\n")

    # Recorrer filas desde la segunda
    for fila_idx in range(1, len(matrizNp)):

        print(f"\n----- Fila {fila_idx + 1} -----")
        fila = matrizNp[fila_idx]

        inicio = time.time()

        t_idx = 0
        while t_idx < len(testores):

            testor = testores[t_idx]
            cubre = any(fila[col] == 1 for col in testor)

            if cubre:
                print(f"✔ Testor válido {testor}")
                t_idx += 1
                continue

            print(f"❌ Testor {testor} NO cubre esta fila. Intentando ampliaciones...")

            ampliaciones = []
            for col in range(len(fila)):
                if fila[col] == 1 and col not in testor:

                    # FIX: lista válida, NO numpy array raro
                    nuevo = sorted(testor + [col])

                    # Submatriz compatible
                    sub = matrizNp[:fila_idx+1, nuevo]

                    if matrizCompatible(sub):
                        print(f"   ➕ Ampliación válida → {nuevo}")
                        ampliaciones.append(nuevo)

            if ampliaciones:
                # Reemplazar por ampliaciones
                testores[t_idx:t_idx+1] = ampliaciones
                t_idx += len(ampliaciones)
            else:
                print(f"   ❌ Eliminando testor {testor}")
                del testores[t_idx]

        fin = time.time()
        tiempo_fila = fin - inicio
        tiempo_acumulado += tiempo_fila

        print(f"\n✔ Testores después de procesar fila {fila_idx + 1}: {testores}")
        print(f"⏱ Tiempo fila {fila_idx + 1}: {tiempo_fila:.6f} s")
        print(f"⏱ Tiempo acumulado hasta ahora: {tiempo_acumulado:.6f} s")

    print("\n====================================================")
    print("✔ Testores típicos finales:", testores)
    print(f"⏱ Tiempo total del algoritmo: {tiempo_acumulado:.6f} segundos")
    print("====================================================\n")

    return testores


def matriz_basica_densidad_mayor_mitad():
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
            print("❌ Error: Fila inválida. Intente otra vez.")
    return matriz


def thetaoperador(A, B):
    resultado = []
    for filaA in A:
        for filaB in B:
            resultado.append(filaA + filaB)
    return resultado


def phioperador(A, B):
    A = np.array(A)
    B = np.array(B)
    return np.concatenate((A, B), axis=1).tolist()


def gammaoperador(A, B):
    A = np.array(A)
    B = np.array(B)
    cerosA = np.zeros((len(A), len(B[0])), dtype=int)
    cerosB = np.zeros((len(B), len(A[0])), dtype=int)
    arriba = np.concatenate((A, cerosA), axis=1)
    abajo = np.concatenate((cerosB, B), axis=1)
    return np.concatenate((arriba, abajo), axis=0).tolist()


def ultimo_indice_uno(lista):
    for i in range(len(lista)-1, -1, -1):
        if lista[i] == 1:
            return i+1
    return 0


def caracteristicas_testores_tipicos(testores):
    res = []
    for fila in testores:
        indices = [i for i,x in enumerate(fila) if x == 1]
        res.append(indices)
    return res

# ======================================================
# ===================== MENÚ PRINCIPAL =================
# ======================================================

def mostrar_matriz(M):
    if M is None:
        print("\n❌ No hay matriz cargada aún.\n")
        return
    print("\n=== MATRIZ ACTUAL ===")
    for fila in M:
        print(fila)
    print("=====================\n")


def menu():
    matriz_actual = None

    while True:
        print("\n=========== MENÚ PRINCIPAL ===========")
        print("1. Ingresar matriz manualmente")
        print("2. Generar matriz booleana aleatoria (densidad ≥ 0.5)")
        print("3. Generar matriz con Θ (Theta)")
        print("4. Generar matriz con Φ (Phi)")
        print("5. Generar matriz con Γ (Gamma)")
        print("6. Ejecutar algoritmo YYC")
        print("7. Ejecutar algoritmo BT")
        print("8. Mostrar matriz actual")
        print("9. Salir")
        print("======================================")

        opcion = input("Seleccione una opción: ")

        # 1. Matriz manual
        if opcion == "1":
            matriz_actual = ingresar_matriz()
            print("\n✔ Matriz cargada correctamente.\n")

        # 2. Matriz aleatoria con densidad ≥ 0.5
        elif opcion == "2":
            matriz_actual = matriz_basica_densidad_mayor_mitad()
            print("\n✔ Matriz aleatoria generada y reducida.\n")

        # 3. Operador Theta
        elif opcion == "3":
            if matriz_actual is None:
                print("❌ Primero cargue una matriz base para aplicar Θ.")
            else:
                print("Ingrese la segunda matriz B para aplicar Θ:")
                B = ingresar_matriz()
                matriz_actual = thetaoperador(matriz_actual, B)
                print("\n✔ Nueva matriz generada con Θ.\n")

        # 4. Operador Phi
        elif opcion == "4":
            if matriz_actual is None:
                print("❌ Primero cargue una matriz base para aplicar Φ.")
            else:
                print("Ingrese la segunda matriz B para aplicar Φ:")
                B = ingresar_matriz()
                matriz_actual = phioperador(matriz_actual, B)
                print("\n✔ Nueva matriz generada con Φ.\n")

        # 5. Operador Gamma
        elif opcion == "5":
            if matriz_actual is None:
                print("❌ Primero cargue una matriz base para aplicar Γ.")
            else:
                print("Ingrese la segunda matriz B para aplicar Γ:")
                B = ingresar_matriz()
                matriz_actual = gammaoperador(matriz_actual, B)
                print("\n✔ Nueva matriz generada con Γ.\n")

        # 6. Ejecutar YYC
        elif opcion == "6":
            if matriz_actual is None:
                print("❌ No hay matriz cargada.")
            else:
                print("\n=== EJECUCIÓN DEL ALGORITMO YYC ===")
                yyc(matriz_actual)

        # 7. Ejecutar BT
        elif opcion == "7":
            if matriz_actual is None:
                print("❌ No hay matriz cargada.")
            else:
                print("\n=== EJECUCIÓN DEL ALGORITMO BT ===")
                resultado = bt(matriz_actual)
                print("\n✔ Testores BT:")
                for fila in resultado:
                    print(fila)

        # 8. Mostrar matriz actual
        elif opcion == "8":
            mostrar_matriz(matriz_actual)

        # 9. Salir
        elif opcion == "9":
            print("\n👋 Saliendo del programa...")
            break

        else:
            print("\n❌ Opción inválida. Intente nuevamente.\n")


# ===================== INICIO =========================

#menu()


# ============================================================
# ===  CÓDIGO REPARADO PARA EL EJERCICIO 5  ===================
# ============================================================

import copy
import time
import csv
import numpy as np
import random

# ---------- ENVOLTURAS SIN PRINTS PARA YYC / BT ----------

def yyc_sin_print(M):
    # copia ligera de yyc pero con stdout silenciado
    import sys, io
    backup_stdout = sys.stdout
    sys.stdout = io.StringIO()
    res = yyc(copy.deepcopy(M))
    sys.stdout = backup_stdout
    return res

def bt_sin_print(M):
    import sys, io
    backup_stdout = sys.stdout
    sys.stdout = io.StringIO()
    res = bt(copy.deepcopy(M))
    sys.stdout = backup_stdout
    return res

# ---------- OPERADORES USADOS EN EL EJERCICIO 5 ----------

def theta_from_AB(A, B):
    out = []
    for a in A:
        for b in B:
            out.append(a + b)
    return out

def phi_from_AB(A, B):
    A = np.array(A)
    B = np.array(B)
    return np.concatenate((A, B), axis=1).tolist()

def gamma_from_AB(A, B):
    A = np.array(A)
    B = np.array(B)
    cerosA = np.zeros((len(A), len(B[0])), dtype=int)
    cerosB = np.zeros((len(B), len(A[0])), dtype=int)
    up = np.concatenate((A, cerosA), axis=1)
    down = np.concatenate((cerosB, B), axis=1)
    return np.concatenate((up, down), axis=0).tolist()

# ---------- ORDENAR FILAS ----------
def sort_rows_by_ones(M):
    return sorted(M, key=lambda r: sum(r))

# ---------- MEDICIÓN DE TIEMPO ----------
def medir(func, M, veces=3):
    tiempos = []
    for _ in range(veces):
        t0 = time.time()
        func(copy.deepcopy(M))
        t1 = time.time()
        tiempos.append(t1 - t0)
    return sum(tiempos) / len(tiempos)

# ---------- EXPERIMENTO ----------
def experimento(nombre, M):
    filas = len(M)
    cols = len(M[0])
    dens = sum(sum(r) for r in M) / (filas * cols)

    # ANY ORDER
    yyc_any = medir(yyc_sin_print, M)
    bt_any  = medir(bt_sin_print,  M)

    # SORTED
    M_sorted = sort_rows_by_ones(M)
    yyc_sorted = medir(yyc_sin_print, M_sorted)
    bt_sorted  = medir(bt_sin_print,  M_sorted)

    return {
        "matriz": nombre,
        "filas": filas,
        "cols": cols,
        "densidad": dens,
        "yyc_any": yyc_any,
        "yyc_sorted": yyc_sorted,
        "bt_any": bt_any,
        "bt_sorted": bt_sorted,
    }

# ---------- MATRICES A y B DEL PROYECTO ----------
A = [
    [0,0,0,0,0,1],
    [1,0,0,1,0,0],
    [0,1,1,1,0,0],
    [1,0,0,0,1,0],
    [1,1,1,0,0,0],
    [0,1,0,1,1,0]
]

B = [
    [0,0,1,1,1,1],
    [0,1,0,1,1,1],
    [1,0,0,1,0,1],
    [1,0,1,0,1,1],
    [1,1,0,0,0,1],
    [1,1,1,0,1,0]
]

# ---------- GENERAR MATRICES DEL EJERCICIO ----------
Theta = theta_from_AB(A, B)
Phi   = phi_from_AB(A, B)
Gamma = gamma_from_AB(A, B)

print("Matriz Theta:")
for l in Theta:
    print(l)
print("\nMatriz Phi:")
for l in Phi:
    print(l)
print("\nMatriz Gamma:")
for l in Gamma:
    print(l)
# ---------- CORRER EXPERIMENTOS ----------
resultados = []
resultados.append(experimento("Theta", Theta))
resultados.append(experimento("Phi",   Phi))
resultados.append(experimento("Gamma", Gamma))

# ---------- EXPORTAR A CSV ----------
with open("resultados_ej5.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Matriz","Filas","Cols","Densidad",
                "YYC_any","YYC_sorted","BT_any","BT_sorted"])
    for r in resultados:
        w.writerow([r["matriz"], r["filas"], r["cols"], r["densidad"],
                    r["yyc_any"], r["yyc_sorted"], r["bt_any"], r["bt_sorted"]])

print(">>> Experimento completado. Archivo generado: resultados_ej5.csv")
print("Resultados:")
for r in resultados:
    print(r)
