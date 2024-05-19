asientos = [
    [" ", "A", "  B", "  C", "", "  D", "  E", "  F"],
    ["1", 2, 0, 2, 2, 0, 2],
    ["2", 2, 0, 2, 2, 0, 2],
    ["3", 2, 0, 2, 2, 0, 2],
    ["4", 2, 0, 2, 2, 0, 2],
    ["5", 2, 0, 2, 2, 0, 2],
    ["6", 2, 0, 2, 2, 0, 2],
]

rojos = []
asientos_vacios = []

def imprimir_mapa():
    # Encabezados de columna
    print("  ", end="")
    for header in asientos[0]:
        if header != " ":
            print(f" {header} ", end="")
        else:
            print("   ", end="")

    print()  # Salto de línea después de los encabezados

    # Imprimir los asientos
    for fila in asientos[1:]:
        print(" ")
        if fila[0].isdigit():  # Comprobar si la fila contiene números de asiento
            print(f" {fila[0]:2} ", end="")  # Número de fila con ajuste de formato
            for i, valor in enumerate(fila[1:]):
                if i == 3:  # Espacio entre las alas
                    print("  ", end="")  # Espacio para la columna central vacía
                if valor == 0:
                    print(" \033[91m███\033[0m ", end="")  # Rojo
                elif valor == 1:
                    print(" \033[92m███\033[0m ", end="")  # Verde
                elif valor == 2:
                    print(" \033[97m███\033[0m ", end="")  # Blanco
                elif valor == 3:
                    print(" \033[90m███\033[0m ", end="")  # Gris
            print()  # Nueva línea al final de cada fila
        else:
            print(fila[0])  # Imprimir la línea de separación

def buscar_asiento(asientos, valor_buscado):
    for i, fila in enumerate(asientos[1:], start=1):  # Comienza en 1 para omitir los encabezados
        for j, valor in enumerate(fila[1:], start=1):  # Comienza en 1 para omitir el número de la fila
            if valor == valor_buscado:
                return (i, j)  # Retornar índices como (número de fila, columna)
    return None  # Retorna None si no encuentra el valor

def buscar_vacios(asientos, valor_buscado, personas):
    for i, fila in enumerate(asientos[1:], start=1):  # Comienza en 1 para omitir los encabezados
        for j, valor in enumerate(fila[1:], start=1):  # Comienza en 1 para omitir el número de la fila
            if (valor == valor_buscado) and ((j + personas) < 8):
                asientos_vacios.append((i, j))

def logica_asiento(personas, indice_asiento):
    x, y = indice_asiento[0], indice_asiento[1]
    for iterador in range(personas):
        asientos[x][y] = 1
        y += 1
        if iterador == personas - 1:
            if y < len(asientos[x]):  # Verificar límites antes de acceder a asientos[x][y]
                if asientos[x][y] in {0, 1, 2}:
                    asientos[x][y] = 0
            else:
                print("papas fritas")

def encontrar_rojo():
    for i, fila in enumerate(asientos[1:], start=1):
        for j, valor in enumerate(fila[1:], start=1):
            if valor == 0:  # valor 0 representa un asiento rojo
                rojos.append((i, j))  # Guardamos la fila y la columna

def verificar_rojo():
    encontrar_rojo()
    for x_r, y_r in rojos:
        y_r += 1  # Verificamos el siguiente asiento en la misma fila
        if y_r < len(asientos[x_r]):  # Aseguramos que no salimos de rango
            if asientos[x_r][y_r] == 0:
                asientos[x_r][y_r] = 2  # Cambiamos a blanco
        else:
            print("papas")

def asiento():
    try:
        while True:
            imprimir_mapa()
            personas = int(input("¿Cuántos boletos desea comprar? "))
            if personas > 5 or personas <= 0:
                print("No se pueden comprar esa cantidad de boletos.")
                break
            else:
                buscar_vacios(asientos, 2, personas)
                if asientos_vacios:
                    indice_asiento = asientos_vacios[0]
                    print(asientos_vacios)
                    print(indice_asiento)
                    asientos_vacios.clear()

                    if indice_asiento:
                        print(f"El primer asiento disponible se encuentra en la fila {indice_asiento[0]}, columna {indice_asiento[1]}")
                    else:
                        print("No se encontró un asiento disponible.")
                    asiento_disponible = buscar_asiento(asientos, 2)  # Busca asientos disponibles (valor 2)
                    if asiento_disponible:
                        print(f"Asiento disponible en fila {asiento_disponible[0]}, columna {asiento_disponible[1]}.")
                        logica_asiento(personas, indice_asiento)
                        verificar_rojo()
                        rojos.clear()
                    else:
                        print("No hay asientos disponibles.")
                    verificar_rojo()
                    rojos.clear()
                else:
                    print("No hay suficientes asientos disponibles.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Llamar a la función asiento para ejecutar la lógica
asiento()
