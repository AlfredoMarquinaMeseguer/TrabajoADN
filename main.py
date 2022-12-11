import re as re

# url = 'https://aulavirtual.um.es/access/content/group/1896_G_2022_N_N/PRACTICAS/PRACTICA%202/All_C_genes_DNA.txt'

dicc = {"clave": [[], []]}
diccGenes = {}

# dicc["clave"][0].append(2)
# dicc["clave"][1].append("Hola")

fichero_encimas = "link_bionet.txt"
fichero_cadenas_C = "All_C_genes_DNA.txt"


def rellenaDiccGenes():
    print("Cargando bionet...")
    # Abre el fichero completo
    with open(fichero_cadenas_C) as fichero:
        # Cogemos todos los genes
        genes = re.findall(r"(?<=\n)>(C\.\w*).*\n([ATGC\s]+)(?=\n)", fichero.read())
    # Bucle que recorra todos los genes
    # print(genes)
    # print(len(genes))
    for gen in genes:
        # separado = re.search(r">(C\.(\w*)) *((\d+) nt)\n([ATGC\s]+)", gen)
        # Reemplazar los espacios del grupo seis
        nucleotidos = re.sub(r"\s", "", gen[1])
        # Guardar en diccionario clave grupo 1 y contenido grupo seis reemplazado
        diccGenes[gen[0]] = nucleotidos


def rellenaDiccEnzimas():
    print("Cargando All_C_genes_DNA.txt...")
    # Abrir

    # Separar por nombre de enzima

    # Bucle guardar en diccionario
    # Saltar diez primera lineas
    # Expresion cada linea "([A-Z]\w*) (\(.+\))? +([A-Z^]+)"
    #  1 -> Clave
    #  3 -> contenido

    # Sustitución grupo 3 -> diana
    # Guardar posición ^ y suprimir
    # llamar reeemplazar por enzimas
    # Añadir parentesis

    # Estructura dicc {clave: [[0], "(GGATCC)"]}
    # Comprobación si existe ya entrada en dicc
    # if dicc[clave] :
    # Si Existe añadir grupo3 al string con separador '|'
    # str.append("|"+diana)
    # listadeCortes.append(posCorte)
    # Sino existe crear estrucutra nueva entrada
    # dicc[clave] = [[posCorte],diana]
    # Fin Bucle


def consultaGenes():
    gen = input("Gen >> ")

    while gen != "":
        # Comprobar que existe en diccionario
        # Si no está
        if gen not in diccGenes:
            print("Nombre de gen incorreto")
        # Si está
        else:
            # Se imprime el numero de nucleotidos y la cadena del gen en el formato especificado
            print("-------------- " + diccGenes[gen].length() + " nucleótidos\n" +
                  diccGenes[gen] +
                  "\n--------------")
        # Llama a la funcion consulta enzimas
            consultaEnzimas(diccGenes[gen])

        gen = input("Gen >> ")

    print("==============")


def consultaEnzimas(gen: str):
    # Listado de clave
    # dicc.keys()

    enzima = input("Enzima >> ")
    enzimaTratado = False

    # Bucle comprobar nombre enzima
    # Comporbar todas la enzimas con la expresión regular
    # Si la expresión hace algún tipo de match
    # tratarEnzima(gen, enzima)
    # enzimaTratado = True

    if not enzimaTratado:
        print("Nombre de enzima incorrecto")


def tratarEnzima(gen: str, nombre_enzima: str):
    # Pasamos variables del dicc a una forma más manejable
    expresion_enzima = dicc[nombre_enzima][1]
    gorritos_enzima = dicc[nombre_enzima][0]

    # Aquí guardaremos las coincidencias
    cortes = []

    # Indice con respecto a la cadena original
    indice_inicio = 0

    # Función search devuelve primer match hecho
    objeto_match = re.search(expresion_enzima, gen)

    # Estructura dicc {clave: [[0], "(GGATCC)"]}
    # Este bucle sigue buscando hasta que no se encuentren más coincidencias
    while objeto_match:
        cortes.append(objeto_match.start())
        # Aprendemos que grupo ha hecho match
        i = 1
        while (objeto_match[i] == None):
            i += 1

        # Añadimos posicion de corte a la lista de cortes
        cortes.append(indice_inicio + objeto_match.start() + gorritos_enzima[i - 1])
        # Actualiar indice
        indice_inicio += objeto_match.end()

        # Actualizar string quitando la parte ya comprobada
        gen = gen[objeto_match.end():]

        # Se busca el siguiente punto de corte
        objeto_match = re.search(expresion_enzima, gen)

    # Se imprime mensaje si la lista de cortes no está vacia
    if len(cortes) != 0:
        print(nombre_enzima + " # " + cortes.__str__())


def reemplazar_enzimas(cadena):
    cadena = re.sub("R", "[AG]", cadena)
    cadena = re.sub("Y", "[CT]", cadena)
    cadena = re.sub("M", "[AC]", cadena)
    cadena = re.sub("K", "[GT]", cadena)
    cadena = re.sub("S", "[CG]", cadena)
    cadena = re.sub("W", "[AT]", cadena)
    cadena = re.sub("B", "[CGT]", cadena)
    cadena = re.sub("D", "[AGT]", cadena)
    cadena = re.sub("H", "[ACT]", cadena)
    cadena = re.sub("V", "[ACG]", cadena)
    cadena = re.sub("N", "[ACGT]", cadena)
    return cadena


def main():
    rellenaDiccGenes()
    print(diccGenes.keys())
    print(diccGenes.items())
    consultaGenes()


if __name__ == '__main__':
    main()
