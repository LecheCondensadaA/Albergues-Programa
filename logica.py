from archivo import*
import tkinter.messagebox as msgbox
import tkinter as tk
from math import*
from tkinter.font import* 

def centrar_ventana(root:tk.Toplevel, modo:int):
    ancho = root.winfo_screenwidth()
    alto = root.winfo_screenheight()
    x = (ancho - root.winfo_reqwidth()) // 2
    y = (alto - root.winfo_reqheight()) // 2
    if modo == 1:
        x=0
    else:
        if modo == 2:
            y=0
    root.geometry(f"+{x}+{y}")

def generar_popup(tipo:str, mensaje:str):
    root = tk.Tk()
    root.wm_attributes("-topmost", 1)
    root.withdraw()
    if tipo == "Advertencia":
        msgbox.showwarning(tipo, mensaje, parent=root)
    else:
        if tipo == "Error":
            msgbox.showerror(tipo, mensaje, parent=root)
        else:
            msgbox.showinfo(tipo, mensaje, parent=root)
    root.destroy()
        
def al_pinchar(lista:tk.Toplevel, cuadrito_de_proyeccion:tk.Listbox, Albergues_leido:list):
    for widget in cuadrito_de_proyeccion.winfo_children():
        widget.destroy()
    
    seleccion = lista.curselection()
    if seleccion:
        indice = seleccion[0]
        albergue = Albergues_leido[indice]

        nombre = albergue[0]
        cant_pers = int(albergue[5])
        cant_med = round(float(albergue[7]), 1)
        dias = 7

        proyeccion = calcular_proyeccion_diaria(cant_med, cant_pers, dias)

        tk.Label(cuadrito_de_proyeccion, text="Día", font=Font(size=15)).grid(row=0, column=0, padx=10)
        for i in range(1, dias + 1):
            tk.Label(cuadrito_de_proyeccion, text=str(i), font=Font(size=15)).grid(row=0, column=i, padx=10)

        tk.Label(cuadrito_de_proyeccion, text=nombre, font=Font(size=15)).grid(row=1, column=0, padx=10, sticky="w")
        for i, cantidad in enumerate(proyeccion):
            tk.Label(cuadrito_de_proyeccion, text=str(cantidad), font=Font(size=15)).grid(row=1, column=i + 1, padx=10)
    
def act_paq_alm():
    try:
        Albergues_leido = leer_archivo("albergues.csv")
        ind = 1
        for i in Albergues_leido:
            i[7] =  str(round((float(i[7]) - int(i[5])/10), 2))
            act_linea("albergues.csv", i, ind)
            ind = ind+1
    except FileNotFoundError:
        pass

def dia(dias_añadidos:int):
    n_dia = 1
    try:
        with open("días.csv", "r") as dias:
            n_dia = dias.readlines()
            if dias_añadidos == 1:
                n_dia = str(len(n_dia) + dias_añadidos) + "\n"
                escribir_archivo("días.csv", n_dia)
            else:
                n_dia = len(n_dia)
    except FileNotFoundError:
        with open("días.csv", "w") as dias:
            dias.write(str(n_dia) + "\n")
    return int(n_dia)

def nueva_ventana(titulo:str, texto:list, alto:int, ancho:int, modo:int):
    ventana = tk.Toplevel()
    ventana.attributes('-topmost',True)
    ventana.title(titulo)
    centrar_ventana(ventana, modo)
    for i in range(len(texto)):
        tk.Label(ventana, text=texto[i], height=alto, width=ancho).pack()
    
def calcular_proyeccion_diaria(cant_med:float, cant_pers:int, dias:int):
    medicamentos_restantes = []
    for i in range(dias): 
        medicamentos_restantes.append(cant_med)
        cant_med -= round((cant_pers/10), 1)
        cant_med = round(cant_med, 1)
        if cant_med < 0:
            cant_med = round(0, 1)
    return medicamentos_restantes

def ingresar_albergues(Nombre_del_albergue:str, Ubicacion:list, Capacidad_maxima_personas:str, Cantidad_personas:str, Capacidad_maxima_paquetes:str, Paquetes_almacenados:str):
    try:
        archivo_albergue = open("albergues.csv", "r")
        archivo_albergue.close()
    except FileNotFoundError:
        escribir_archivo("albergues.csv", "# Nombre, lat, long, dia_creacion, cap_pers, cant_pers, cap_med, cant_med\n")
    if Nombre_del_albergue == "" and Ubicacion[0] == "" and Ubicacion[1] == "" and Capacidad_maxima_personas == "" and Cantidad_personas == "" and Capacidad_maxima_paquetes ==""  and Paquetes_almacenados == "":
        pass
    else:
        Nombre_del_albergue = nombre_albergue(Nombre_del_albergue)
        if Nombre_del_albergue !="":
            Ubicacion = ubicacion(Ubicacion[0], Ubicacion[1])
            if Ubicacion != ["", ""]:
                Capacidad_maxima_personas = cap_max_personas(Capacidad_maxima_personas)
                if Capacidad_maxima_personas!="":
                    Cantidad_personas = personas_albergue(Cantidad_personas, Capacidad_maxima_personas)
                    if Cantidad_personas!="":
                        Capacidad_maxima_paquetes = cap_max_paquetes(Capacidad_maxima_paquetes)
                        if Capacidad_maxima_paquetes!="":
                            Paquetes_almacenados = paquetes_albergue(Paquetes_almacenados, Capacidad_maxima_paquetes)
                            if Paquetes_almacenados!="":
                                escribir_archivo("albergues.csv", Nombre_del_albergue + ",")
                                escribir_archivo("albergues.csv", Ubicacion[0] + ",")
                                escribir_archivo("albergues.csv", Ubicacion[1] + ",")
                                escribir_archivo("albergues.csv", str(dia(0)) + ",")
                                escribir_archivo("albergues.csv", Capacidad_maxima_personas + ",")
                                escribir_archivo("albergues.csv", Cantidad_personas + ",")
                                escribir_archivo("albergues.csv", Capacidad_maxima_paquetes + ",")
                                escribir_archivo("albergues.csv", Paquetes_almacenados + "\n")
                                generar_popup("Ingresar albergues", "¡Albergue ingresado exitosamente!")

def nombre_albergue(nombre:str):
    archivo_albergue = open("albergues.csv", "r")
    archivo_albergue.close()
    Albergues_leido = leer_archivo("albergues.csv")
    existe = False
    for i in range(len(Albergues_leido)):
        if nombre == Albergues_leido[i][0]:
            existe = True
            break
    nombre = nombre.strip("")
    nombre = nombre.strip(" ")
    
    if len(nombre) >0 and existe == False:
        return nombre
    else:
        if len(nombre) <=0:
            generar_popup("Error", "Ingrese el nombre del albergue.")
            return ""
    if existe == True:
        generar_popup("Error", "Este albergue ya ha sido ingresado.")
        return ""

def ubicacion(latitud:float, longitud:float):
    try:
        latitud = round(float(latitud),1)
        longitud = round(float(longitud),1)
        if latitud <=-17.5 and latitud >= float(-56) and longitud <= float(-66) and longitud >= float(-75):
            return [str(latitud), str(longitud)]
        else:
            if latitud >-17.5 or latitud < float(-56):
                generar_popup("Error", "La latitud debe estar comprendida entre -17.5° por el norte y -56° por el sur.")
            else:
                if longitud > float(-66) or longitud < float(-75):
                    generar_popup("Error", "La longitud debe estar comprendida entre -75° por el oeste y -66° por el este.")
            return ["", ""]
    except ValueError:
        generar_popup("Error", "La latitud debe estar comprendida entre -17.5° por el norte y -56° por el sur,"
                        + " y la longitud debe estar comprendida entre -75° por el oeste y -66° por el este.")
        return ["", ""]
    
def personas_albergue(cantidad_personas:str, capacidad_max_personas:str):
    try:
        cant_personas = int(cantidad_personas)
        capacidad_max_personas = int(capacidad_max_personas)
        if cant_personas >=0 and cant_personas <=capacidad_max_personas:
            return str(cant_personas)
        else:
            if cant_personas<0:
                generar_popup("Error", "La cantidad de personas debe ser un número entero mayor a 0.")
            if cant_personas>capacidad_max_personas:
                generar_popup("Error", "La cantidad de personas debe ser menor a la capacidad máxima.")
            return ""
    except ValueError:
        generar_popup("Error", "La cantidad de personas debe ser un número entero mayor a 0.")
        return ""
    
def cap_max_personas(capacidad_personas:int):
    try:
        capacidad_maxima_personas = int(capacidad_personas)
        if capacidad_maxima_personas > 0:
            return str(capacidad_maxima_personas)
        else:
            generar_popup("Error", "La capacidad máxima de personas debe ser un número entero mayor a 0.")
            return ""
    except ValueError:
        generar_popup("Error", "La capacidad máxima de personas debe ser un número entero mayor a 0.")
        return ""

def paquetes_albergue(cantidad_paquetes:float, capacidad_max_paquetes:float):
    try:
        capacidad_max_paquetes = round(float(capacidad_max_paquetes),1)
        cant_paquetes = round(float(cantidad_paquetes),1)
        if cant_paquetes >=0 and cant_paquetes <=capacidad_max_paquetes:
            return str(cant_paquetes)
        else:
            if cant_paquetes<0:
                generar_popup("Error", "La cantidad de paquetes debe ser un número mayor a 0.")
            if cant_paquetes>capacidad_max_paquetes:
                generar_popup("Error", "La cantidad de paquetes debe ser menor a la capacidad máxima.")
            return ""
    except ValueError:
        generar_popup("Error", "La cantidad de paquetes debe ser un número mayor a 0.")
        return ""

def cap_max_paquetes(capacidad_paquetes:float):
    try:
        capacidad_maxima_paquetes = round(float(capacidad_paquetes),1)
        if capacidad_maxima_paquetes > 0:
            return str(capacidad_maxima_paquetes)
        else:
            generar_popup("Error", "La capacidad máxima de paquetes debe ser un número mayor a 0.")
            return ""
    except ValueError:
        generar_popup("Error", "La capacidad máxima de paquetes debe ser un número mayor a 0.")
        return ""

def ingresar_envios(nombre_albergue:str, cant_paquetes_medicos:str):
    try:
        Albergues_leido = leer_archivo("albergues.csv")
    except FileNotFoundError:
        Albergues_leido = []
    albergues_recorridos = []
    if len(Albergues_leido) <=0:
        generar_popup("Advertencia", "Ingrese al menos un albergue.")
    if len(Albergues_leido) > 0:
        try:
            with open('envios.csv','r') as archivo:
                envios = archivo.readlines()
                num_vuelo = len(envios)
        except FileNotFoundError:
            crear_linea(["num_vuelo", "destino", "carga", "dia"], "envios.csv")
            num_vuelo = 1
        nombre_albergue = nombre_albergue.strip("")
        nombre_albergue = nombre_albergue.strip(" ")
        if nombre_albergue == "" and cant_paquetes_medicos == "":
            pass
        else:
            existe = False
            for i in range(len(Albergues_leido)):
                if nombre_albergue == Albergues_leido[i][0]:
                    existe = True
                    break
                else:
                    pass
            if nombre_albergue == "":
                generar_popup("Error", "Ingrese el nombre del albergue.")
            else:
                if existe == False:
                    generar_popup("Error", "El albergue ingresado no existe.")
                else:
                    try:
                        cant_paquetes_medicos = int(cant_paquetes_medicos)
                        if cant_paquetes_medicos<=0:
                            generar_popup("Error", "La cantidad de paquetes a enviar debe ser un número entero mayor a 0.")
                    except ValueError:
                        cant_paquetes_medicos = int(0)
                        generar_popup("Error", "La cantidad de paquetes a enviar debe ser un número entero mayor a 0.")

                    if nombre_albergue != "" and cant_paquetes_medicos>0:
                        escribir_archivo("envios.csv", str(num_vuelo) + ",")
                        escribir_archivo("envios.csv", nombre_albergue + ",")
                        escribir_archivo("envios.csv", str(cant_paquetes_medicos) + ",")
                        escribir_archivo("envios.csv", str(dia(0)) + "\n")
                        texto = ["Núm vuelo: " + str(num_vuelo) + ". Albergue: " + nombre_albergue + ".\n",
                            " Paquetes enviados: " + str(cant_paquetes_medicos) + ". Día: " + str(dia(0)) + ".\n"]
                        
                        for i in range(len(Albergues_leido)):
                            for y in range(len(Albergues_leido)):
                                if Albergues_leido[y][0] == nombre_albergue:
                                    listaDelAlbergue = Albergues_leido[y]
                            
                            p_anteriores = listaDelAlbergue[7]
                            
                            cant_paquetes_medicos = añadir_paquete(nombre_albergue, cant_paquetes_medicos)
                            albergues_recorridos.append(nombre_albergue)
                            Albergues_leido = leer_archivo("albergues.csv")
                            texto.append(nombre_albergue + " pasa de " + str(p_anteriores) +"/" + str(listaDelAlbergue[6]) + " a " + Albergues_leido[i][7] + "/" + str(listaDelAlbergue[6]) + "\n")
                            
                            if cant_paquetes_medicos > 0:
                                d_de_albergues = distancia_albergue(nombre_albergue)
                                for x in range(len(d_de_albergues)):
                                    for y in range(len(Albergues_leido)):
                                        if Albergues_leido[y][0] == d_de_albergues[x][0]:
                                            listaDelAlbergue = Albergues_leido[y]
                                            if round(float((listaDelAlbergue[6])), 1) >= round(float((listaDelAlbergue[7])), 1) and listaDelAlbergue[0] not in albergues_recorridos:
                                                nombre_albergue = d_de_albergues[x][0]
                                                break
                                    if nombre_albergue == d_de_albergues[x][0]:
                                        break
                            else:
                                break
                            if len(albergues_recorridos) == len(Albergues_leido):
                                texto.append(paquetes_perdidos(cant_paquetes_medicos, texto))
                            
                        nueva_ventana("Envío completado", texto, 0,0, 2)

def ordenar_distancia(distancia:list):
    lista_ordenada = []
    n_distancia = []
    for i in range(len(distancia)):
        n_distancia.append(distancia[i][1])
    n_distancia = sorted(n_distancia)
    for j in range(len(n_distancia)):
        for k in range(len(distancia)):
            if distancia[k][1] == n_distancia[j]:
                lista_ordenada.append(distancia[k])
    return lista_ordenada
            
def calcular_distancia(y1:float, x1:float, y2:float, x2:float):
    x1= float(x1)
    x2=float(x2)
    y1=float(y1)
    y2=float(y2)
    distancia = sqrt(((x2-x1)**2) + ((y2-y1)**2))
    return distancia

def distancia_albergue(albergue:str):
    Albergues_leido = leer_archivo("albergues.csv")
    distancias_albergues = []
    for i in range(len(Albergues_leido)):
        if albergue == Albergues_leido[i][0]:
            lista_con_albergue = Albergues_leido[i]
            break
    for j in range(len(Albergues_leido)):
        d_albergue = []
        if Albergues_leido[j] == lista_con_albergue:
            pass
        else:
            d_albergue = [Albergues_leido[j][0], 
                          calcular_distancia(Albergues_leido[j][1],
                          Albergues_leido[j][2],
                          lista_con_albergue[1], 
                          lista_con_albergue[2])]
            
            distancias_albergues.append(d_albergue)
    return ordenar_distancia(distancias_albergues)

def añadir_paquete(n_albergue:str, n_paquetes:int):
    Albergues_leido = leer_archivo("albergues.csv")
    for i in range(len(Albergues_leido)):
        if n_albergue == Albergues_leido[i][0]:
            lista_n_albergue = Albergues_leido[i]
            indice = i+1
            break
    r_resta = float(lista_n_albergue[6]) - float(lista_n_albergue[7])
    r_resta = round(r_resta, 1)
    if r_resta <= n_paquetes:
        lista_n_albergue[7] = str(round(float(lista_n_albergue[7]) + r_resta, 1))
        act_linea("albergues.csv", lista_n_albergue, indice)
        p_restantes = round(float(n_paquetes) - r_resta, 1)
    else:
        lista_n_albergue[7] = str(round(float((lista_n_albergue[7])), 1) + n_paquetes)
        act_linea("albergues.csv", lista_n_albergue, indice)
        p_restantes = int(0)
    return p_restantes

def paquetes_perdidos(p_perdidos:int, texto:list):
    if p_perdidos == 0:
        texto.append("No se perdieron paquetes médicos." + "\n")
    else:
        texto.append("Se perdieron " + str(p_perdidos) + " paquetes médicos." + "\n")

def editar_personas_albergue(nombre_albergue:str, nueva_cant_personas:str):
    
    try:
        Albergues_leido = leer_archivo("albergues.csv")
    except FileNotFoundError:
        Albergues_leido = []

    if len(Albergues_leido) <=0:
        generar_popup("Advertencia", "Ingrese al menos un albergue.")
    else:
        nombre_albergue = nombre_albergue.strip("")
        nombre_albergue = nombre_albergue.strip(" ")
        if nombre_albergue == "" and nueva_cant_personas == "":
            pass
        else:
            if nombre_albergue == "":
                generar_popup("Error", "Ingrese el nombre del albergue.")
            else:
                existe = False
                for y in range(len(Albergues_leido)):
                    if Albergues_leido[y][0] == nombre_albergue:
                        existe = True
                        listaDelAlbergue = Albergues_leido[y]
                        indice_albergue = y+1
                        break
                if existe == False:
                    generar_popup("Error", "El albergue ingresado no existe.")
                else:
                    if nueva_cant_personas == "":
                        generar_popup("Error", "La nueva cantidad de personas debe ser un número entero positivo mayor o igual a 0.")
                    else:
                        try:
                            if int(nueva_cant_personas) <= int(listaDelAlbergue[4]) and int(nueva_cant_personas) >=0:
                                cant_personas = str(nueva_cant_personas)
                                listaDelAlbergue[5] = cant_personas
                                act_linea("albergues.csv", listaDelAlbergue, indice_albergue)
                                generar_popup("Albergue actualizado exitosamente", "La cantidad de personas ha sido actualizada exitosamente.")
                            else:
                                if int(nueva_cant_personas) > int(listaDelAlbergue[4]):
                                    generar_popup("Error", "La nueva cantidad de personas no puede exceder la capacidad máxima del albergue.")
                                if int(nueva_cant_personas) <0:
                                    generar_popup("Error", "La nueva cantidad de personas debe ser un número entero positivo mayor o igual a 0.")
                        except ValueError:
                            generar_popup("Error", "La nueva cantidad de personas debe ser un número entero positivo mayor o igual a 0.")
