def escribir_archivo(archivo:str, dato:str):
    a_escribir = open(archivo, "a")
    a_escribir= a_escribir.write(dato)

def crear_linea(L_valores:list, nombre_archivo:str):
    try:
        string = open(nombre_archivo, "r")
    except FileNotFoundError:
        string = open(nombre_archivo, "w")
        string.close()
    string = open(nombre_archivo, "r")
    string = string.readlines()
    L_valores = ",".join(L_valores) + "\n"
    string2 = open(nombre_archivo, "a")
    string2 = string2.writelines(L_valores)

def act_linea(archivo:str , L_parametros:list, indice:int):
    arch = open(archivo, "r")
    arch = arch.readlines()
    with open (archivo, "w"):
        for i in range(len(arch)):
            if i == indice:
                crear_linea(L_parametros, archivo)
            else:
                aux = [arch[i].strip("\n")]
                crear_linea(aux, archivo)
                
def leer_archivo(archivo:str):
    a_leido = open(archivo, "r")
    a_leido = a_leido.readlines()
    archivo_separado = []
    for x in range(1, len(a_leido)):
        i = a_leido[x].strip("\n")
        i = i.split(",")
        lista_separada = i
        archivo_separado.append(lista_separada)
    return archivo_separado
