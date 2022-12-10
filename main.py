# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re as re
import urllib.request

#url = 'https://aulavirtual.um.es/access/content/group/1896_G_2022_N_N/PRACTICAS/PRACTICA%202/All_C_genes_DNA.txt'

# Implementar la
dicc = {"clave":[[],[]]}

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


def consultaGenes() :
    gen = input("Gen >> ")

    while(gen != "") :
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


def consultaEnzimas(gen : str) :
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


def tratarEnzima(gen:str, nombre_enzima:str):
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
        print(nombre_enzima+" # "+cortes)


def abrir_fichero(fichero):
    try:
        fichero = open(fichero, "r")
        for linea in fichero:
            linea = linea.strip()
            print(linea)
    except IOError as e:
        print('link_bionet no disponible: ', e)

def reemplazar_enzimas(cadena):
    cadena = re.sub("R", "[AG]",cadena)
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
    cadena_prueba = "UcoMSI (SacI)                     GAGCTCNNNNN^"
    #Coge y Separa una linea de
    d = re.search("(\w+) (\(.+\))? +([ATCGRYMKSWBDHVN^]+)",cadena_prueba)




    print(d.group(1),d.group(2),d.group(3))
    reemplazado = reemplazar_enzimas(d.group(3))
    print(reemplazado)


if __name__ == '__main__':
    main()

