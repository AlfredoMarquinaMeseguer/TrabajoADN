# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re as re
import urllib.request

# url = 'https://aulavirtual.um.es/access/content/group/1896_G_2022_N_N/PRACTICAS/PRACTICA%202/All_C_genes_DNA.txt'

# Implementar la
dicc = {"clave": [[], []]}
diccEnzimas = {}

# dicc["clave"][0].append(2)
# dicc["clave"][1].append("Hola")

fichero_encimas = "link_bionet.txt"
fichero_cadenas_C = "All_C_genes_DNA.txt"


def rellenaDiccGenes():
    print("Cargando bionet...")
    # No Abrir fichero por lineas
    abrir_fichero("All_C_genes_DNA.txt")
    # Cogemos todos los genes

    # Bucle que recorra todos los genes
    # for i in :
    # Reemplazar los espacios del grupo seis
    #   guardar = re.sub("\s", "", grupo6)

    # Guardar en diccionario clave grupo 1 y contenido grupo seis reemplazado
    return 0


def rellenaDiccEnzimas():
    print("Cargando bionet.txt...")
    # Abrir

    # Separar por nombre de enzima

    with open("link_bionet.txt") as fichero_enzimas:
        # Saltar diez primera lineas, contienen titulo
        for _ in range(10):
            next(fichero_enzimas)
        # Expresion cada linea "([A-Z]\w*) (\(.+\))? +([A-Z^]+)"
        #   1 -> nombre enzima
        #   2 -> prototipo
        #   3 -> diana
        enzimas_separadas = re.findall(r"([A-Z][^ ]*) (\(.+\))? +([A-Z^]+)", fichero_enzimas.read())
        # Bucle guardar en diccionario
        print(enzimas_separadas)
        for actual in enzimas_separadas:
            #  nombre enzima -> clave diccionario
            clave = actual[0]
            #  diana -> contenido diccionario
            diana = actual[2]
            # Guardar posición ^ y suprimir
            posicion_corte = diana.find("^")
            copia = posicion_corte
            if posicion_corte == -1:  # Si posicion corte es -1 es porque no está en la diana
                posicion_corte = 0  # Se supone que el corte está al principio
            else:  # Si "^" está, se suprime
                diana = re.sub(r"\^", "", diana)
            # Reformatear diana para expresión regular
            diana = reemplazar_enzimas(diana)
            # Añadir parentesis
            diana = "(" + diana + ")"

            print(clave, copia, posicion_corte, diana)
            # Estructura dicc {clave: ["(GGATCC)", [0]]}
            # Comprobación si existe ya entrada en dicc
            if clave in diccEnzimas:  # Si existe, añadir diana al string con separador '|'
                # Comprobamos que esta combinación no se encuentra ya en el diccionario
                comprobar = re.sub(r"[\[\]()]", r"\\\g<0>", diana)
                if not re.search(comprobar, diccEnzimas[clave][0]):  # Si no hay coincidencia devuelve None
                    diccEnzimas[clave][0] += "|" + diana  # Añadir el separador
                    diccEnzimas[clave][1].append(posicion_corte)
            else:  # Sino existe crear estrucutra nueva entrada
                diccEnzimas[clave] = [diana, [posicion_corte]]


def consultaGenes():
    gen = input("Gen >> ")

    while (gen != ""):
        # Comprobar que existe en diccionario
        # Sino está
        # print("Nombre de gen incorreto")
        # Si está
        # print("-------------- "+dicc[clave].length()+" nucleótidos\n"+ \
        # dicc[gen]+ \
        # "\n--------------")
        # consultaEnzimas(dicc[gen])

        # volver a pedir otro gen
        gen = input("Gen >> ")

    # print("==============")
    # Salir


def consultaEnzimas(gen: str):
    # Listado de clave
    # dicc.keys()

    consulta = input("Enzima >> ")
    enzima_tratado = False

    # Bucle comprobar nombre enzima
    # Comprobar todas la enzimas con la expresión regular
    for enzima in diccEnzimas.keys():
        # Comprobamos enzima a enzima
        if re.search(consulta, enzima):  # Si la expresión hace algún
            tratarEnzima(gen, enzima)
            enzima_tratado = True

    if not enzima_tratado:
        print("Nombre de enzima incorrecto")


def tratarEnzima(cadena_gen: str, nombre_enzima: str):
    # Pasamos variables del dicc a una forma más manejable
    expresion_enzima = dicc[nombre_enzima][0]
    gorritos_enzima = dicc[nombre_enzima][1]

    # Aquí guardaremos las coincidencias
    cortes = []

    # Indice con respecto a la cadena original
    indice_inicio = 0

    # Función search devuelve primer match hecho
    objeto_match = re.search(expresion_enzima, cadena_gen)

    # Estructura dicc {clave: [[0], "(GGATCC)"]}
    # Este bucle sigue buscando hasta que no se encuentren más coincidencias
    while objeto_match:
        cortes.append(objeto_match.start())
        # Aprendemos que grupo ha hecho match
        i = 1
        while not objeto_match[i]:
            i += 1

        # Añadimos posicion de corte a la lista de cortes
        cortes.append(indice_inicio + objeto_match.start() + gorritos_enzima[i - 1])
        # Actualiar indice
        indice_inicio += objeto_match.end()

        # Actualizar string quitando la parte ya comprobada
        cadena_gen = cadena_gen[objeto_match.end():]

        # Se busca el siguiente punto de corte
        objeto_match = re.search(expresion_enzima, cadena_gen)

    # Se imprime mensaje si la lista de cortes no está vacia
    if len(cortes) != 0:
        print(nombre_enzima + " # " + cortes.__str__())


def abrir_fichero(fichero):
    try:
        fichero = open(fichero, "r")
        for linea in fichero:
            linea = linea.strip()
            print(linea)
    except IOError as e:
        print('link_bionet no disponible: ', e)


def reemplazar_enzimas(cadena):
    cadena = re.sub(r"R", "[AG]", cadena)
    cadena = re.sub(r"Y", "[CT]", cadena)
    cadena = re.sub(r"M", "[AC]", cadena)
    cadena = re.sub(r"K", "[GT]", cadena)
    cadena = re.sub(r"S", "[CG]", cadena)
    cadena = re.sub(r"W", "[AT]", cadena)
    cadena = re.sub(r"B", "[CGT]", cadena)
    cadena = re.sub(r"D", "[AGT]", cadena)
    cadena = re.sub(r"H", "[ACT]", cadena)
    cadena = re.sub(r"V", "[ACG]", cadena)
    cadena = re.sub(r"N", "[ACGT]", cadena)
    return cadena


def main():
    rellenaDiccEnzimas()
    print(diccEnzimas.items())


if __name__ == '__main__':
    main()
