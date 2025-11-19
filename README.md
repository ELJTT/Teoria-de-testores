# Teoría de Testores - Implementación de Algoritmos BT y YYC

## 📋 Descripción del Proyecto

Este proyecto implementa y evalúa dos algoritmos fundamentales en la teoría de testores para el análisis de matrices binarias: **BT (Búsqueda con Técnicas de Poda)** y **YYC (Yamada-Yokota-Cheng)**. Ambos métodos permiten identificar **testores típicos** - subconjuntos mínimos de características que preservan la capacidad discriminante de la matriz original.

## 🎯 Objetivos

- **Implementar algoritmos** BT y YYC para el cálculo de testores típicos
- **Analizar matrices binarias** básicas y generadas sintéticamente
- **Comparar el desempeño** computacional entre ambos algoritmos
- **Validar propiedades teóricas** de los testores típicos
- **Proveer herramientas** para investigación en reconocimiento de patrones

## 🧮 Algoritmos Implementados

### 🔍 Algoritmo BT (Búsqueda con Técnicas de Poda)
- Explora combinaciones booleanas de características mediante estrategias de poda
- Utiliza saltos inteligentes para evitar búsquedas redundantes
- Evalúa sistemáticamente n-uplos desde el más simple al más complejo
- Optimizado con reglas de irrelevancia para descartar combinaciones no válidas

### 🚀 Algoritmo YYC (Yamada-Yokota-Cheng)
- Construye testores de manera incremental fila por fila
- Verifica compatibilidad de submatrices en cada paso
- Emplea criterios de suma de columnas para validar testores
- Eficiente en matrices con estructura específica

## 📊 Características del Sistema

### Funcionalidades Principales
- **Generación de matrices** booleanas aleatorias con densidad controlada
- **Reducción a matriz básica** eliminando filas redundantes
- **Cálculo de testores típicos** con ambos algoritmos
- **Medición de tiempos** de ejecución por fila/iteración
- **Visualización de resultados** en formato binario y de características
- **Comparación automática** entre conjuntos de testores

### Operadores Implementados
- **θ(A,B)**: Concatenación de filas de A con filas de B
- **φ(A,B)**: Concatenación por columnas de matrices
- **γ(A,B)**: Construcción de matriz bloque-diagonal

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3.x
- **Librerías principales**: NumPy, time, math, random
- **Estructuras de datos** optimizadas para combinatoria
- **Algoritmos** de procesamiento de matrices booleanas

## 📁 Estructura del Código

### Clases Principales

#### `AlgoritmoYYC`
- `matriz_es_admisible()`: Valida matriz binaria
- `matriz_basica()`: Reduce matriz eliminando filas dominadas
- `submatriz_compatible()`: Verifica compatibilidad de submatrices
- `yyc()`: Algoritmo principal YYC

#### `AlgoritmoBT`
- `ultimo_indice_uno()`: Encuentra último índice con valor 1
- `bt()`: Algoritmo principal BT
- Cálculo de saltos optimizados

#### `GeneradorMatrices`
- `generar_matriz_aleatoria()`: Crea matrices con densidad mínima
- `ingresar_matriz_manual()`: Interfaz para entrada manual
- `mostrar_matriz()`: Visualización legible de matrices

## 📈 Métricas y Análisis

### Mediciones Implementadas
- **Tiempo de ejecución** por fila/iteración
- **Tiempo acumulado** total
- **Número de testores** por etapa
- **Evolución de candidatos** durante el proceso
- **Comparación de completitud** entre algoritmos

### Evaluación de Rendimiento
- **YYC vs BT** en diferentes configuraciones
- **Impacto del orden** de filas en el desempeño
- **Análisis de escalabilidad** con matrices grandes
- **Efecto de la densidad** en la complejidad computacional

## 🔬 Aplicaciones

### Académicas
- Enseñanza de teoría de testores
- Investigación en matemáticas discretas
- Análisis comparativo de algoritmos

### Prácticas
- Selección de características en machine learning
- Sistemas de diagnóstico basados en rasgos
- Reconocimiento de patrones y minería de datos
- Optimización de conjuntos discriminantes

## 📖 Referencias Teóricas

El proyecto se basa en la teoría formal de testores típicos, incluyendo:

- Conceptos de matriz básica y testores mínimos
- Propiedades de clausura de testores típicos
- Algoritmos clásicos YYC y BT
- Operadores matriciales θ, φ, γ

## 🚀 Uso del Sistema

El sistema ofrece interfaces interactivas para:

1. **Ingreso manual** de matrices
2. **Generación automática** con parámetros controlados
3. **Ejecución selectiva** de algoritmos
4. **Visualización detallada** de resultados
5. **Exportación** de conjuntos de testores

## 📊 Resultados Esperados

- Identificación completa de testores típicos
- Análisis comparativo de eficiencia algorítmica
- Validación de propiedades teóricas
- Herramienta educativa para teoría de testores

---

*Proyecto desarrollado en el marco de Matemáticas Discretas - Teoría de Testores*
