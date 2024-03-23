from collections import deque
from rich.table import Table
from rich.console import Console


grafo = {
    "A": [("B", 2, 10), ("D", 5, 4), ("E", 3, 7)],
    "B": [("C", 16, 0)],
    "C": [],
    "D": [("C", 4, 0)],
    "E": [("F", 2, 8)],
    "F": [],
}

grafo2 = {
    "n1": [("n2", 200, 50), ("n3", 30, 50), ("n4", 40, 50), ("n5", 200, 50), ("n6", 325, 0), ("n7", 250, 45)],
    "n2": [("n3", 25, 50), ("n7", 100, 45)],
    "n3": [],
    "n4": [("n3", 35, 50), ("n5", 150, 50)],
    "n5": [("n6", 100, 0)],
    "n6": [],
    "n7": [("n6", 25, 0)],
}


def obtener_camino(nodo_final, estructura_datos):
    camino = [nodo_final]
    nodo_actual = nodo_final
    costo = estructura_datos[nodo_actual]["coste_al_anterior"]

    while estructura_datos[nodo_actual]["anterior"] is not None:
        nodo_actual = estructura_datos[nodo_actual]["anterior"]
        costo += estructura_datos[nodo_actual]["coste_al_anterior"]
        camino.append(nodo_actual)

    camino.reverse()
    return camino, costo


def coste_uniforme(graph, start, target, direction="I"):
    ABIERTA = []
    ABIERTA.append(start)
    TABLA_A = {}
    counter = 0
    console = Console()
    tabla = Table(title=f"Búsqueda de coste uniforme.")
    columnas = [
        "Nodo",
        "ABIERTA",
        "TABLA_A",
        "Camino",
        "Costo total",
        "Es nodo objetivo",
    ]
    for columna in columnas:
        tabla.add_column(columna)
    while ABIERTA:
        vertice = ABIERTA.pop(0)
        if vertice not in TABLA_A:
            TABLA_A[vertice] = {
                "clave": vertice,
                "anterior": None,
                "sucesores": [],
                "coste_al_anterior": 0,
            }
        for hijo in graph[vertice] if direction == "I" else graph[vertice][::-1]:
            if hijo[0] not in TABLA_A:
                TABLA_A[vertice]["sucesores"].append(hijo[0])
                TABLA_A[hijo[0]] = {
                    "clave": hijo[0],
                    "anterior": vertice,
                    "sucesores": [],
                    "coste_al_anterior": hijo[1],
                }
            if hijo[0] not in ABIERTA:
                ABIERTA.append(hijo[0])
        new_abierta = []
        for v in ABIERTA:
            _, costo_total = obtener_camino(v, TABLA_A)
            new_abierta.append((v, costo_total))
        ABIERTA = [x[0] for x in sorted(new_abierta, key=lambda x: x[1])]
        camino, costo_total = obtener_camino(vertice, TABLA_A)
        tabla.add_row(
            *[
                str(counter),
                str(list(ABIERTA)),
                str(TABLA_A[vertice]),
                str(camino),
                str(costo_total),
                "Si" if vertice == target else "No",
            ],
            style="bright_green",
        )
        counter += 1
        if vertice == target:
            console.print(tabla)
            return True
    console.print(tabla)
    return False


def busqueda_en_anchura(grafo, inicio, objetivo, direccion="I", max_anchura=1000):
    ABIERTA = deque()
    ABIERTA.append(inicio)
    TABLA_A = set()
    NODE_INFO = {}
    TABLA_A.add(inicio)
    counter = 0
    console = Console()
    tabla = Table(
        title=f"Búsqueda en anchura {'de izquierda a derecha' if direccion == 'I' else 'de derecha a izquierda'}."
    )
    columnas = [
        "Nodo",
        "ABIERTA",
        "TABLA_A",
        "Camino",
        "Costo total",
        "Es nodo objetivo",
    ]
    for columna in columnas:
        tabla.add_column(columna)

    while ABIERTA:
        vertice = ABIERTA.popleft()
        if not vertice in NODE_INFO:
            NODE_INFO[vertice] = {
                "clave": vertice,
                "anterior": None,
                "sucesores": [],
                "coste_al_anterior": 0,
            }
        if vertice != inicio:
            for vecino in grafo:
                if vertice in [x[0] for x in grafo[vecino]]:
                    NODE_INFO[vertice]["anterior"] = vecino
                    for x in grafo[vecino]:
                        if vertice == x[0]:
                            NODE_INFO[vertice]["coste_al_anterior"] = x[1]
        for vecino in (
            grafo[vertice][:max_anchura]
            if direccion == "I"
            else grafo[vertice][::-1][:max_anchura]
        ):
            if vecino not in TABLA_A:
                TABLA_A.add(vecino[0])
                ABIERTA.append(vecino[0])
                NODE_INFO[vertice]["sucesores"].append(vecino[0])
        info = None
        info = NODE_INFO[vertice]
        camino, costo_total = obtener_camino(vertice, NODE_INFO)
        tabla.add_row(
            *[
                str(counter),
                str(list(ABIERTA)),
                str(info),
                str(camino),
                str(costo_total),
                "Si" if vertice == objetivo else "No",
            ],
            style="bright_green",
        )
        counter += 1
        if vertice == objetivo:
            console.print(tabla)
            return True
    console.print(tabla)
    return False


def dfs(graph, start, target, direction="I", max_profundidad=1000):
    ABIERTA = deque()
    ABIERTA.append(start)
    TABLA_A = {}
    counter = 0
    console = Console()
    tabla = Table(
        title=f"Búsqueda en profundidad {'de izquierda a derecha' if direction == 'I' else 'de derecha a izquierda'}."
    )
    columnas = [
        "Nodo",
        "ABIERTA",
        "TABLA_A",
        "Camino",
        "Costo total",
        "Es nodo objetivo",
    ]
    for columna in columnas:
        tabla.add_column(columna)
    while ABIERTA:
        vertice = ABIERTA.popleft()
        if vertice not in TABLA_A:
            TABLA_A[vertice] = {
                "clave": vertice,
                "anterior": None,
                "sucesores": [],
                "coste_al_anterior": 0,
            }

        for hijo in graph[vertice][::-1] if direction == "I" else graph[vertice]:
            if hijo[0] not in TABLA_A:
                TABLA_A[vertice]["sucesores"].append(hijo[0])
                TABLA_A[hijo[0]] = {
                    "clave": hijo[0],
                    "anterior": vertice,
                    "sucesores": [],
                    "coste_al_anterior": hijo[1],
                }
            if hijo[0] not in ABIERTA and counter < max_profundidad:
                ABIERTA.appendleft(hijo[0])
        camino, costo_total = obtener_camino(vertice, TABLA_A)
        tabla.add_row(
            *[
                str(counter),
                str(list(ABIERTA)),
                str(TABLA_A[vertice]),
                str(camino),
                str(costo_total),
                "Si" if vertice == target else "No",
            ],
            style="bright_green",
        )
        counter += 1
        if vertice == target:
            console.print(tabla)
            return True
    console.print(tabla)
    return False


def busqueda_en_anchura_iterativa(max_anchura, grafo, inicio, objetivo, direccion="I"):
    print(
        "##################### INICIO BUSQUEDA EN ANCHURA ITERATIVA #####################"
    )
    for x in range(0, max_anchura):
        busqueda_en_anchura(grafo, inicio, objetivo, direccion, x)
    print(
        "##################### FIN BUSQUEDA EN ANCHURA ITERATIVA #####################"
    )


def busqueda_en_profundidad_iterativa(
    max_profundidad, grafo, inicio, objetivo, direccion="I"
):
    print(
        "##################### INICIO BUSQUEDA EN PROFUNDIAD ITERATIVA #####################"
    )
    for x in range(0, max_profundidad):
        dfs(grafo, inicio, objetivo, direccion, x)
    print(
        "##################### FIN BUSQUEDA EN PROFUNDIDAD ITERATIVA #####################"
    )


def a_estrella(graph, start, goal):
    ABIERTA = []
    TABLA_A = {}
    ABIERTA.append(start)
    counter = 0
    console = Console()
    tabla = Table(
        title=f"Búsqueda A*."
    )
    columnas = [
        "Nodo",
        "ABIERTA",
        "TABLA_A",
        "Camino",
        "Costo total",
        "h",
        "Es nodo objetivo",
    ]
    for columna in columnas:
        tabla.add_column(columna)

    def g(n):
        return obtener_camino(n, TABLA_A)[1]

    def h(n):
        return TABLA_A[n]["estimado_a_meta"] + TABLA_A[n]["g"]

    def rectificar(n, p, costepn):
        if g(p) + costepn < g(n):
            TABLA_A[n]["anterior"] = p
            TABLA_A[n]["coste_al_anterior"] = costepn
            TABLA_A[n]["g"] = g(p) + costepn

    def ordenar_abierta():
        ABIERTA.sort(key=lambda x: TABLA_A[x]["h"] + TABLA_A[x]["g"])

    while ABIERTA:
        n = ABIERTA.pop(0)
        if n not in TABLA_A:
            TABLA_A[n] = {
                "clave": n,
                "anterior": None,
                "coste_al_anterior": 0,
                "estimado_a_meta": 100,
                "g": 0,
                "h": 100,
            }
        camino, costo = obtener_camino(n, TABLA_A)
        tabla.add_row(
            *[
                str(counter),
                str(list(ABIERTA)),
                str(TABLA_A[n]),
                str(camino),
                str(costo),
                str(TABLA_A[n]["h"]),
                "Si" if n == goal else "No",
            ],
            style="bright_green",
        )
        counter += 1
        if n == goal:
            console.print(tabla)
            return True
        for q in graph[n]:
            if q[0] in TABLA_A:
                rectificar(q[0], n, q[1])
                ordenar_abierta()
            else:
                TABLA_A[q[0]] = {
                    "clave": q[0],
                    "anterior": n,
                    "coste_al_anterior": q[1],
                    "estimado_a_meta": q[2],
                }
                TABLA_A[q[0]]["g"] = g(n) + q[1]
                TABLA_A[q[0]]["h"] = h(q[0])
                ABIERTA.append(q[0])
                ordenar_abierta()
    console.print(tabla)
    return False


# busqueda_en_profundidad_iterativa(4, grafo, "A", "C", "I")
a_estrella(grafo2, "n1", "n6")
