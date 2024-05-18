import json
from datetime import datetime, timedelta


def cargar_usuarios():
    with open('usuarios.json', 'r') as file:
        return json.load(file)

def guardar_usuarios(usuarios_datos):
    with open('usuarios.json', 'w') as file:
        json.dump(usuarios_datos, file, indent=4)

def registro_usuarios():
    usuarios_datos = cargar_usuarios()

    while True:
        numero_cedula = str(input("\nDigite su número de cédula: ")).strip()
        if numero_cedula.isdigit() and len(numero_cedula) == 9:
            if numero_cedula in usuarios_datos['usuarios']:
                print("La cédula ya está registrada. Por favor, ingrese una nueva cédula.")
                continue  # Volver al inicio del bucle
            else:
                nombre = input("Digite el nombre del usuario: ")
                while True:
                    try:
                        edad = int(input(f"{nombre} digite su edad del usuario: "))
                        if edad < 0:
                            print("La edad no puede ser negativa.")
                            continue
                        elif edad < 18:
                            print("El usuario debe ser mayor de 18 años.")
                            continue
                        break
                    except ValueError:
                        print("Ingrese un número entero para la edad.")

                clave = input("Digite la clave del usuario: ")
                usuarios_datos['usuarios'][numero_cedula] = {"nombre": nombre, "edad": edad, "clave": clave}
                guardar_usuarios(usuarios_datos)
                print("Persona registrada exitosamente.")
                break
        else:
            print("\n¡Error!")
            print("El número de cédula debe tener nueve dígitos y debe ser de carácter numérico")

def inicio_sesion():
    usuarios_datos = cargar_usuarios()
    numero_cedula = input("\nDigite su número de cédula: ").strip()
    clave = input("Digite su clave: ")

    if numero_cedula in usuarios_datos['usuarios']:
        if usuarios_datos['usuarios'][numero_cedula]['clave'] == clave:
            print("Inicio de sesión exitoso.")
            print("¡Bienvenido Usuario! Meter resto de funcionalidades acá para el usuarios")
        else:
            print("La clave es incorrecta.")
    elif numero_cedula == usuarios_datos['admin'].get('cedula'):
        if clave == usuarios_datos['admin'].get('clave'):
            print("Inicio de sesión exitoso.")
            print("¡Bienvenido Administrador! Meter el resto de funcionalidades de admi acá")
        else:
            print("La clave de administrador es incorrecta.")
    else:
        print("El número de cédula no está registrado.")


# Acá se almacena una lista de al menos 10 aerolíneas con la siguiente información
aerolineas = {
    "AAL": "American Airlines",
    "DAL": "Delta Air Lines",
    "UAL": "United Airlines",
    "SWA": "Southwest Airlines",
    "JAL": "Japan Airlines",
    "ANA": "All Nippon Airways",
    "BAW": "British Airways",
    "LUF": "Lufthansa",
    "AFR": "Air France",
    "QTR": "Qatar Airways"
}


#  Debe estar almacenada una lista de al menos 10 aeropuertos de países diferentes con la siguiente información:
aeropuertos = {
    "SJO": {"id_aeropuerto": "SJO", "nombre": "Aeropuerto Internacional Juan Santamaría", "pais": "Costa Rica"},
    "LHR": {"id_aeropuerto": "LHR", "nombre": "Heathrow Airport", "pais": "Reino Unido"},
    "CDG": {"id_aeropuerto": "CDG", "nombre": "Charles de Gaulle Airport", "pais": "Francia"},
    "HND": {"id_aeropuerto": "HND", "nombre": "Haneda Airport", "pais": "Japón"},
    "SYD": {"id_aeropuerto": "SYD", "nombre": "Sydney Airport", "pais": "Australia"},
    "DXB": {"id_aeropuerto": "DXB", "nombre": "Dubai International Airport", "pais": "Emiratos Árabes Unidos"},
    "SIN": {"id_aeropuerto": "SIN", "nombre": "Singapore Changi Airport", "pais": "Singapur"},
    "CAN": {"id_aeropuerto": "CAN", "nombre": "Guangzhou Baiyun International Airport", "pais": "China"},
    "MEX": {"id_aeropuerto": "MEX", "nombre": "Mexico City International Airport", "pais": "México"},
    "ICN": {"id_aeropuerto": "ICN", "nombre": "Incheon International Airport", "pais": "Corea del Sur"}
}


def cargar_vuelos():
    try:
        with open('vuelos.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Si no existe devuelve un diccionario vacío
        return {}
    except json.decoder.JSONDecodeError:
        # Si está vacio devuelve un diccionario vacío
        return {}
vuelos = cargar_vuelos()


def actualizar_disponibilidad():
    ahora = datetime.now()
    cambios = False
    try:
        with open('vuelos.json', 'r') as file:
            vuelos = json.load(file).get('vuelos', [])
        with open('aviones.json', 'r') as file:
            aviones = json.load(file)
        with open('tripulaciones.json', 'r') as file:
            tripulaciones = json.load(file)
    except FileNotFoundError:
        print("Uno o más archivos no se encontraron.")
        return
    except json.decoder.JSONDecodeError:
        print("Error al decodificar el JSON.")
        return

    # Actualizar estados
    for vuelo in vuelos:
        fecha_hora_salida = datetime.strptime(vuelo['Fecha_y_hora_salida'], "%d-%m-%Y %H:%M:%S")
        if ahora >= fecha_hora_salida + timedelta(hours=24):
            id_aerolinea = vuelo['Id_de_la_aerolinea']
            id_avion = vuelo['Id_del_avion']
            print(f"Actualizando disponibilidad para el vuelo {vuelo['Id_del_vuelo']} de la aerolínea {id_aerolinea}")

            # Marcar avión como disponible
            for avion in aviones.get(id_aerolinea, []):
                if avion['id_avion'] == id_avion and avion['estado'] == 'No disponible':
                    avion['estado'] = 'Disponible'
                    cambios = True
                    print(f"Avión {id_avion} de la aerolínea {id_aerolinea} marcado como disponible.")

            # Marcar tripulación como disponible
            for rol, id in vuelo['Id_de_tripulacion'].items():
                for tripulante in tripulaciones.get(id_aerolinea, []):
                    if tripulante['cedula'] == id and tripulante['estado'] == 'No disponible':
                        tripulante['estado'] = 'Disponible'
                        cambios = True
                        print(f"Tripulante {id} ({rol}) de la aerolínea {id_aerolinea} marcado como disponible.")

    # Guardar cambios solo de ser es necesario
    if cambios:
        with open('aviones.json', 'w') as file:
            json.dump(aviones, file, indent=4)
        with open('tripulaciones.json', 'w') as file:
            json.dump(tripulaciones, file, indent=4)
        print("Disponibilidad actualizada.")
    else:
        print("No se necesitaron actualizaciones.")

def creacion_vuelos():
    actualizar_disponibilidad()
    # Cargar info de vuelos si hay
    try:
        with open('vuelos.json', 'r') as file:
            data = json.load(file)
            vuelos = data.get("vuelos", [])
    except (FileNotFoundError, json.JSONDecodeError):
        vuelos = []

    # Cargar info de tripulaciones desde el archivo JSON
    try:
        with open('tripulaciones.json', 'r') as file:
            tripulaciones = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: No se pudo cargar el archivo tripulaciones.json")
        return

    # Cargar info de aviones desde el archivo JSON
    try:
        with open('aviones.json', 'r') as file:
            aviones = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: No se pudo cargar el archivo aviones.json")
        return

    # Mostrar menú para elegir aerolínea
    print("Seleccione la aerolínea:")
    aerolineas_lista = list(aerolineas.items())
    for i, (codigo, nombre) in enumerate(aerolineas_lista, start=1):
        print(f"{i}. {codigo} : {nombre} ")
    while True:
        try:
            opcion_aerolinea = int(input("Seleccione el número de la aerolínea: "))
            if 1 <= opcion_aerolinea <= len(aerolineas_lista):
                aerolinea = aerolineas_lista[opcion_aerolinea - 1][0]
                break
            else:
                print("Opción no válida, intente de nuevo.")
        except ValueError:
            print("Entrada no válida, por favor ingrese un número.")

    while True:
        try:
            precio = float(input("Ingrese el precio del vuelo: "))
            if precio < 0:
                print("El precio no puede ser negativo")
                continue
            elif precio >= 40:
                break
            else:
                print("El precio debe ser de al menos 40. Intente de nuevo.")
        except ValueError:
            print("Entrada no válida, por favor ingrese un valor numérico válido.")

    # Mostrar menú para elegir aeropuerto de salida
    print("\nSeleccione el aeropuerto de salida:")
    aeropuertos_lista = list(aeropuertos.items())
    for i, (codigo, aeropuerto) in enumerate(aeropuertos_lista, start=1):
        print(f"{i}. {codigo} : {aeropuerto['nombre']} - {aeropuerto['pais']}")
    while True:
        try:
            opcion_aeropuerto_salida = int(input("Seleccione el número del aeropuerto de salida: "))
            if 1 <= opcion_aeropuerto_salida <= len(aeropuertos_lista):
                aeropuerto_salida = aeropuertos_lista[opcion_aeropuerto_salida - 1][0]
                break
            else:
                print("Opción no válida, intente de nuevo.")
        except ValueError:
            print("Entrada no válida, por favor ingrese un número.")

    # Mostrar menú para elegir aeropuerto de llegada
    print("\nSeleccione el aeropuerto de llegada:")
    for i, (codigo, aeropuerto) in enumerate(aeropuertos_lista, start=1):
        print(f"{i}. {codigo} : {aeropuerto['nombre']} - {aeropuerto['pais']}")

    while True:
        try:
            opcion_aeropuerto_llegada = int(input("Seleccione el número del aeropuerto de llegada: "))
            aeropuerto_llegada = aeropuertos_lista[opcion_aeropuerto_llegada - 1][0]
            if aeropuerto_llegada == aeropuerto_salida:
                print(
                    "El aeropuerto de llegada y salida no puede ser el mismo. Por favor, seleccione un aeropuerto de llegada diferente.")
                continue
            break
        except ValueError:
            print("Entrada no válida, por favor ingrese un número.")
        except IndexError:
            print("Opción no válida, intente de nuevo.")

    fecha_salida = input("Ingrese la fecha y hora de salida (formato DD-MM-YYYY HH:MM): ").strip()
    fecha_llegada = input("Ingrese la fecha y hora de llegada (formato DD-MM-YYYY HH:MM): ").strip()

    try:
        fecha_salida = datetime.strptime(fecha_salida, "%d-%m-%Y %H:%M")
        fecha_llegada = datetime.strptime(fecha_llegada, "%d-%m-%Y %H:%M")
    except ValueError:
        print("Formato de fecha y hora incorrecto. Use DD-MM-YYYY HH:MM.")
        return

    if fecha_llegada <= fecha_salida:
        print("La fecha de llegada debe ser posterior a la fecha de salida.")
        return

    duracion = str(fecha_llegada - fecha_salida)  # Duracion como string

    avion_disponible = None
    for avion in aviones.get(aerolinea, []):
        if avion['estado'] == 'Disponible':
            avion_disponible = avion
            break

    tripulacion_disponible = []
    for tripulante in tripulaciones.get(aerolinea, []):
        if tripulante['estado'] == 'Disponible':
            tripulacion_disponible.append(tripulante)
            if len(tripulacion_disponible) >= 2:
                break

    if not avion_disponible and len(tripulacion_disponible) < 2:
        print("No hay aviones ni suficiente tripulación disponibles para esta aerolínea.")
        return
    elif not avion_disponible:
        print("No hay aviones disponibles para esta aerolínea.")
        return
    elif len(tripulacion_disponible) < 2:
        print("No hay suficiente tripulación disponible para esta aerolínea.")
        return

    avion_disponible['estado'] = 'No disponible'
    for tripulante in tripulacion_disponible:
        tripulante['estado'] = 'No disponible'

    # Guardar el cambio de estado de las tripulaciones en el archivo tripulaciones.json
    with open('tripulaciones.json', 'w') as file:
        json.dump(tripulaciones, file, indent=4)

    # Guardar el cambio de estado de los aviones en el archivo aviones.json
    with open('aviones.json', 'w') as file:
        json.dump(aviones, file, indent=4)

    id_vuelo = f"V{len(vuelos) + 1:04d}"
    id_piloto = tripulacion_disponible[0]['cedula']
    id_servicio_al_cliente = tripulacion_disponible[1]['cedula']

    # Guardar la info con esa estructura en vuelos.json
    vuelo = {
        "Id_del_vuelo": id_vuelo,
        "Id_de_la_aerolinea": aerolinea,
        "Precio": precio,
        "Fecha_y_hora_salida": fecha_salida.strftime("%d-%m-%Y %H:%M:%S"),
        "Id_del_aeropuerto_de_salida": aeropuerto_salida,
        "Fecha_y_hora_llegada": fecha_llegada.strftime("%d-%m-%Y %H:%M:%S"),
        "Id_del_aeropuerto_de_llegada": aeropuerto_llegada,
        "Duracion": duracion,
        "Id_del_avion": avion_disponible['id_avion'],
        "Id_de_tripulacion": {
            "Id_piloto": id_piloto,
            "Id_servicio_al_cliente": id_servicio_al_cliente
        }
    }

    vuelos.append(vuelo)

    # Guardar la información actualizada de los vuelos en el archivo
    with open('vuelos.json', 'w') as file:
        json.dump({"vuelos": vuelos}, file, indent=4)

    print("Vuelo creado exitosamente.")


def cargar_vuelos():
    try:
        with open('vuelos.json', 'r') as file:
            data = json.load(file)
            return data['vuelos']
    except FileNotFoundError:
        print("El archivo de vuelos no se encuentra.")
        return []
    except json.JSONDecodeError:
        print("Error en la decodificación del JSON.")
        return []

def buscar_vuelos():
    vuelos = cargar_vuelos()
    if not vuelos:
        print("No hay vuelos creados")
        return

    # Mostrar menú para seleccionar aeropuerto de origen
    while True:
        print("\nSeleccione el aeropuerto de origen:")
        for i, (codigo, aeropuerto) in enumerate(aeropuertos.items(), start=1):
            print(f"{i}. {codigo} - {aeropuerto['nombre']} ({aeropuerto['pais']})")
        try:
            origen = int(input("Elija una opción: "))
            aeropuerto_origen = list(aeropuertos.keys())[origen - 1]
            break
        except (ValueError, IndexError):
            print("Entrada inválida. Por favor, elija una opción correcta del menú.")

    # Mostrar menú para seleccionar aeropuerto de destino
    while True:
        print("\nSeleccione el aeropuerto de destino:")
        for i, (codigo, aeropuerto) in enumerate(aeropuertos.items(), start=1):
            print(f"{i}. {codigo} - {aeropuerto['nombre']} ({aeropuerto['pais']})")
        try:
            destino = int(input("Elija una opción: "))
            aeropuerto_destino = list(aeropuertos.keys())[destino - 1]
            if aeropuerto_origen == aeropuerto_destino:
                print(
                    "El aeropuerto de origen y destino no pueden ser el mismo. Por favor, elija un destino diferente.")
                continue
            break
        except (ValueError, IndexError):
            print("Entrada inválida. Por favor, elija una opción correcta del menú.")

    # Solicitar la fecha de salida
    while True:
        fecha_salida_1 = input("Ingrese la fecha de salida (formato DD-MM-YYYY): ").replace(" ", "")
        partes = fecha_salida_1.split('-')

        # Comprobar si la entrada es correcta y llenar con ceros de ser necesario
        if len(partes) == 3:
            year, mes, dia = partes
            mes = mes.zfill(2)
            dia = dia.zfill(2)
            fecha_salida_1 = f"{year}-{mes}-{dia}"

        try:
            fecha_salida = datetime.strptime(fecha_salida_1, "%d-%m-%Y")
            break  # Salir del bucle si la fecha es válida
        except ValueError:
            print("Fecha inválida. Asegúrese de ingresar la fecha en el formato correcto YYYY-MM-DD.")

    # Buscar vuelos directos
    vuelos_directos = [v for v in vuelos if v['Id_del_aeropuerto_de_salida'] == aeropuerto_origen
                       and v['Id_del_aeropuerto_de_llegada'] == aeropuerto_destino
                       and datetime.strptime(v['Fecha_y_hora_salida'], "%d-%m-%Y %H:%M:%S").date() == fecha_salida.date()]

    # Buscar vuelos
    vuelos_escala = []
    for vuelo1 in vuelos:
        if vuelo1['Id_del_aeropuerto_de_salida'] == aeropuerto_origen and datetime.strptime(
                vuelo1['Fecha_y_hora_salida'], "%d-%m-%Y %H:%M:%S").date() == fecha_salida.date():
            for vuelo2 in vuelos:
                if (vuelo1['Id_del_aeropuerto_de_llegada'] == vuelo2['Id_del_aeropuerto_de_salida'] and
                        vuelo1['Id_del_aeropuerto_de_llegada'] != aeropuerto_destino and
                        vuelo2['Id_del_aeropuerto_de_llegada'] == aeropuerto_destino):
                    fecha_llegada_vuelo1 = datetime.strptime(vuelo1['Fecha_y_hora_llegada'], "%d-%m-%Y %H:%M:%S")
                    fecha_salida_vuelo2 = datetime.strptime(vuelo2['Fecha_y_hora_salida'], "%d-%m-%Y %H:%M:%S")
                    # Cambiar tiempo para tomar un vuelo a otro hours = 2, en este caso 15 minutos para tomar otro avión
                    if fecha_llegada_vuelo1 + timedelta(minutes=15) <= fecha_salida_vuelo2:
                        vuelos_escala.append((vuelo1, vuelo2))

    # Calcular costo y tiempo total de vuelos
    resultados_vuelos = []
    for vuelo in vuelos_directos:
        nombre_aerolinea = aerolineas.get(vuelo['Id_de_la_aerolinea'], "Nombre no disponible")
        origen = f"{vuelo['Id_del_aeropuerto_de_salida']}: {aeropuertos[vuelo['Id_del_aeropuerto_de_salida']]['nombre']} ({aeropuertos[vuelo['Id_del_aeropuerto_de_salida']]['pais']})"
        destino = f"{vuelo['Id_del_aeropuerto_de_llegada']}: {aeropuertos[vuelo['Id_del_aeropuerto_de_llegada']]['nombre']} ({aeropuertos[vuelo['Id_del_aeropuerto_de_llegada']]['pais']})"
        resultados_vuelos.append((nombre_aerolinea, origen, destino, vuelo['Fecha_y_hora_salida'],
                                  vuelo['Fecha_y_hora_llegada'], vuelo['Duracion'], vuelo['Precio']))

    for v1, v2 in vuelos_escala:
        precio_total = v1['Precio'] + v2['Precio']
        duracion_total = (datetime.strptime(v2['Fecha_y_hora_llegada'], "%d-%m-%Y %H:%M:%S") - datetime.strptime(
            v1['Fecha_y_hora_salida'], "%d-%m-%Y %H:%M:%S"))
        nombre_aerolinea = aerolineas.get(v1['Id_de_la_aerolinea'], "Nombre no disponible")
        origen = f"{v1['Id_del_aeropuerto_de_salida']}: {aeropuertos[v1['Id_del_aeropuerto_de_salida']]['nombre']} ({aeropuertos[v1['Id_del_aeropuerto_de_salida']]['pais']})"
        destino = f"{v2['Id_del_aeropuerto_de_llegada']}: {aeropuertos[v2['Id_del_aeropuerto_de_llegada']]['nombre']} ({aeropuertos[v2['Id_del_aeropuerto_de_llegada']]['pais']})"
        resultados_vuelos.append((nombre_aerolinea, origen, destino, v1['Fecha_y_hora_salida'],
                                  v2['Fecha_y_hora_llegada'], str(duracion_total), precio_total))

    # Mostrar resultados
    if not resultados_vuelos:
        print("No hay vuelos disponibles para las fechas y destinos seleccionados.")
    else:
        print("\nVuelos disponibles:")
        for i, vuelo in enumerate(resultados_vuelos, start=1):
            print(
                f"{i}. Aerolínea: {vuelo[0]}, Origen: {vuelo[1]}, Destino: {vuelo[2]}, Salida: {vuelo[3]}, Llegada: {vuelo[4]}, Duración: {vuelo[5]}, Precio: ${vuelo[6]:.2f}")

        eleccion = int(input("Seleccione un vuelo para más detalles: "))
        vuelo_elegido = resultados_vuelos[eleccion - 1]
        print(
            f"Ha seleccionado el vuelo de {vuelo_elegido[0]} desde {vuelo_elegido[1]} a {vuelo_elegido[2]}, salida {vuelo_elegido[3]} y llegada {vuelo_elegido[4]} con una duración de {vuelo_elegido[5]} y un costo de ${vuelo_elegido[6]:.2f}.")



def menu_principal():
    while True:
        print("\n╔══════════════════════ Menú principal ══════════════════════╗")
        print("║                                                            ║")
        print("║                    Menú de Opciones                        ║")
        print("║                                                            ║")
        print("║ 1. Inicio de sesión                                        ║")
        print("║ 2. Registrar usuario                                       ║")
        print("║ 3. Creacion de vuelos                                      ║")
        print("║ 4. Buscar vuelos                                           ║")
        print("║ 0. Salir                                                   ║")
        print("║                                                            ║")
        print("╚════════════════════════════════════════════════════════════╝")

        try:
            opcion = int(input("Digite una opcion: "))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue

        match opcion:
            case 1:
                inicio_sesion()
            case 2:
                registro_usuarios()
            case 3:
                creacion_vuelos()
            case 4:
                buscar_vuelos()
            case 0:
                quit("Saliendo del programa...")
            case _:
                print("Opción no válida. Inténtelo de nuevo")


menu_principal()



# Formato de fecha ejemplo
# 15-06-2024 15:30
# 15-06-2024 18:45
# 15-06-2024 19:11
# 15-06-2024 19:50
