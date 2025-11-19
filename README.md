# Teoria-de-testores
Este proyecto implementa y ejecuta dos algoritmos fundamentales en el análisis de matrices binarias dentro del marco de los testores típicos: el algoritmo BT y el algoritmo YYC. Ambos métodos permiten identificar subconjuntos mínimos de características que preservan la capacidad discriminante de la matriz original.

El sistema permite:

Algoritmo BT

Implementa el método descrito en la sección 3.2, explorando las combinaciones de características mediante una estrategia de poda basada en relevancia e irrelevancia. El objetivo es obtener todos los testores típicos minimizando el espacio de búsqueda.

Algoritmo YYC

Ejecuta el análisis fila por fila considerando sumas parciales de columnas y restricciones de agregación, permitiendo verificar si cada candidato puede seguir ampliándose o debe descartarse. Esto asegura una construcción eficiente de testores válidos.
Objetivo del Proyecto:

Proveer una herramienta académica y experimental que permita:

Analizar matrices binarias básicas o generadas sintéticamente.

Comparar el desempeño y resultados entre BT y YYC.

Generar, validar y visualizar conjuntos de testores típicos.

Apoyar investigaciones relacionadas con Algoritmos de Testores, Reconocimiento de Patrones, y Sistemas Basados en Rasgos Discriminantes.

Tecnologías y Lenguaje

Lenguaje: Python

Estructuras de datos optimizadas para combinatoria

Salidas en consola y/o tablas según la matriz procesada
