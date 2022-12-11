import re as re

# Trabajo realizado por Daniel Martínez Prior y Alfredo Marquina Meseguer

# Diccionarios requeridos son globales
diccEnzimas = {}
diccGenes = {}

# Creamos variables con nombres de los ficheros a consultar
fichero_enzimas = "link_bionet.txt"
fichero_cadenas_C = "All_C_genes_DNA.txt"


# Rellena el diccionario de genes con los datos presentes en el fichero All_C_genes_DNA.txt
def rellena_dicc_genes():
    print("Cargando All_C_genes_DNA.txt...")
    # Abre el fichero completo
    with open(fichero_cadenas_C) as fichero:
        # Cogemos todos los genes
        genes = re.findall(r"(?<=\n)>(C\.\w*).*\n([ATGC\s]+)(?=\n)", fichero.read())
    # Bucle que recorra todos los genes
    for gen in genes:
        # Reemplazar los espacios del grupo seis
        nucleotidos = re.sub(r"\s", "", gen[1])
        # Guardar en diccionario clave grupo 1 y contenido grupo seis reemplazado
        diccGenes[gen[0]] = nucleotidos


# Rellena el diccionario de enzimas con los datos presentes en el fichero link_bionet.txt
def rellena_dicc_enzimas():
    print("Cargando bionet...")
    # Abrir fichero
    with open(fichero_enzimas) as fichero:
        # Saltar diez primera lineas, contienen titulo
        for _ in range(10):
            next(fichero)
        # Expresion cada linea "([A-Z]\w*) (\(.+\))? +([A-Z^]+)"
        #   1 -> nombre enzima
        #   2 -> prototipo
        #   3 -> diana
        enzimas_separadas = re.findall(r'([A-Z][^ ]*) (\(.+\))? +([A-Z^]+)', fichero.read())
        # Bucle guardar en diccionario
        for actual in enzimas_separadas:
            #  nombre enzima -> clave diccionario
            clave = actual[0]
            #  diana -> contenido diccionario
            diana = actual[2]
            # Guardar posición ^ y suprimir
            posicion_corte = diana.find("^")
            if posicion_corte == -1:  # Si posicion corte es -1 es porque no está en la diana
                posicion_corte = 0  # Se supone que el corte está al principio
            else:  # Si "^" está, se suprime
                diana = re.sub(r"\^", "", diana)
            # Reformatear diana para expresión regular
            diana = reemplazar_enzimas(diana)
            # Añadir parentesis
            diana = "(" + diana + ")"
            # Estructura dicc {clave: ["(GGATCC)", [0]]}
            # Comprobación si existe ya entrada en el diccionario
            if clave in diccEnzimas:  # Si existe,
                # Comprobamos que esta combinación no se encuentra ya en el diccionario
                comprobar = re.sub(r'[\[\]()]', r"\\\g<0>", diana)
                # Comprobar que no se ha introducido el mismo patron en la entrada de diccionario
                if not re.search(comprobar, diccEnzimas[clave][0]):
                    # Si no se ha introducido ya el mismo patron añadir diana
                    diccEnzimas[clave][0] += "|" + diana  # Añadir diana con separador '|'
                    diccEnzimas[clave][1].append(posicion_corte)  # Añadir
            else:  # Sino existe crear estrucutra nueva entrada
                diccEnzimas[clave] = [diana, [posicion_corte]]


# Acción que consulta genes del diccionario por nombre hasta que se introduzca la cadena vacia
def consulta_genes():
    gen = input("--------------\nGen >> ")

    while gen != "":
        # Comprobar que existe en diccionario
        # Si no está
        if gen not in diccGenes:
            print("Nombre de gen incorreto")
        # Si está
        else:
            # Se imprime el numero de nucleotidos y la cadena del gen en el formato especificado
            print("-------------- " + str(len(diccGenes[gen])) + " nucleótidos\n" +
                  diccGenes[gen])
            # Llama a la funcion consulta enzimas
            consulta_enzimas(diccGenes[gen])

        gen = input("--------------\nGen >> ")


# Acción que consulta enzimas del diccionario con una expresión regular hasta que se introduzca la cadena vacia
def consulta_enzimas(cadena_gen: str):
    # Variable controla si alguna enzima coincide con la consulta
    enzima_tratado = False
    # Se le piden consultas al usuario hasta que consulte cadena vacia
    consulta = input("--------------\nEnzima >> ")
    while consulta:
        # Bucle comprobar nombre enzima
        # Comprobar todas la enzimas con la expresión regular
        for enzima in diccEnzimas.keys():
            # Comprobamos enzima a enzima
            if re.search(r"^" + consulta, enzima):
                # Si la consulta coincide con el enzima se trata
                tratar_enzima(cadena_gen, enzima)
                # Se informa de que se ha realizado al menos una coincidencia
                enzima_tratado = True
        # Si no hemos encontrado ninguna coincidencia se imprime un mensaje
        if not enzima_tratado:
            print("Nombre de enzima incorrecto")
        else:  # Sino, se resetea la variable de control
            enzima_tratado = False
        # Volvemos a pedir otra consulta
        consulta = input("--------------\nEnzima >> ")


# Recibe el nombre de un enzima y la cadena de ADN de un gen.
# Imprime los puntos de corte del enzima en el gen.
# Si no encuentra ninguna coincidencia no imprime nada
def tratar_enzima(cadena_gen: str, nombre_enzima: str):
    # Pasamos variables del diccionario a una forma más manejable
    expresion_enzima = diccEnzimas[nombre_enzima][0]
    gorritos_enzima = diccEnzimas[nombre_enzima][1]

    # Aquí guardaremos las coincidencias
    cortes = []

    # Indice con respecto a la cadena original
    indice_inicio = 0

    # Función search devuelve primer match hecho
    objeto_match = re.search(expresion_enzima, cadena_gen)

    # Estructura dicc {clave: [[0], ]}
    # Este bucle sigue buscando hasta que no se encuentren más coincidencias
    while objeto_match:
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


# Reemplaza subpatrones de la cadenas ezima por una expresión regular
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
    print("==============")
    rellena_dicc_enzimas()
    rellena_dicc_genes()
    consulta_genes()
    print("==============")


if __name__ == '__main__':
    main()
