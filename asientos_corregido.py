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


def buscar_vacios(asientos, valor_buscado):
    for i, fila in enumerate(asientos[1:], start=1):  # Comienza en 1 para omitir los encabezados
        for j, valor in enumerate(fila[1:], start=1):  # Comienza en 1 para omitir el número de la fila
            if (valor == valor_buscado) and ((j + personas) < 8):
                asientos_vacios.append((i,j))


def logica_asiento(personas):
    for fila in asientos[1:]:
        for inicio in range(1, len(fila) - personas + 1):
            if all((fila[inicio + i] == 2 or (fila[inicio + i] == 0 and personas > 1)) for i in range(personas)):
                if inicio > 1 and fila[inicio - 1] != 0:
                    continue

                for i in range(personas):
                    fila[inicio + i] = 1
                if inicio + personas < len(fila) and fila[inicio + personas] == 2:
                    fila[inicio + personas] = 0
                if inicio + personas + 1 < len(fila) and fila[inicio + personas + 1] == 0:
                    fila[inicio + personas + 1] = 2
                return True
    print("No hay suficiente espacio disponible.")
    return False


def verificar_rojo():
    for fila in asientos[1:]:
        for i in range(1, len(fila)):
            if fila[i] == 1:
                if i + 1 < len(fila) and fila[i + 1] == 2:
                    fila[i + 1] = 0  # Cambio a rojo si el siguiente es blanco


while True:
    imprimir_mapa()
    try:
        personas = int(input("¿Cuántos boletos desea comprar? "))
        if personas > 5 or personas <= 0:
            print("No se pueden comprar esa cantidad de boletos.")
            continue

        if not logica_asiento(personas):
            continue

        verificar_rojo()  # Verificar y actualizar asientos rojos si es necesario
    except ValueError:
        print("Por favor, ingrese un número válido de boletos.")
