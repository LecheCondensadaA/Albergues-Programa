import tkinter as tk
import tkinter.messagebox as msgbox
from logica import*
from tkinter.font import* 

def proyeccion_paquetes():
    try:
        Albergues_leido = leer_archivo("albergues.csv")
    except FileNotFoundError:
        Albergues_leido = []

    como_se_ve_en_la_listbox = []

    for i in range(len(Albergues_leido)):
        ordenado = f"{Albergues_leido[i][0]} ({Albergues_leido[i][1]}, {Albergues_leido[i][2]}) Creación: {Albergues_leido[i][3]}. Personas: {Albergues_leido[i][5]}/{Albergues_leido[i][4]}. Medicamentos: {Albergues_leido[i][7]}/{Albergues_leido[i][6]}."
        como_se_ve_en_la_listbox.append(ordenado)

    if not Albergues_leido:
        msgbox.showwarning(title="Advertencia", message="Ingrese al menos un albergue.")
    else:
        root = tk.Toplevel()
        root.attributes('-topmost', True)
        root.title("Proyección de suministros")
        root.minsize(550, 310)

        tk.Label(root, text="ALBERGUES:", font=Font(size=15)).pack()

        frame = tk.Frame(root)
        frame.pack(pady=10, fill=tk.BOTH, expand=False)

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        lista = tk.Listbox(frame, width=50, height=10, yscrollcommand=scrollbar.set)

        scrollbar.config(command=lista.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for albergue in como_se_ve_en_la_listbox:
            lista.insert(tk.END, albergue)
        lista.pack()

        tk.Label(root, text="PROYECCIÓN:", font=Font(size=15)).pack()

        cuadrito_de_proyeccion = tk.Frame(root,height=60)
        cuadrito_de_proyeccion.pack()

        frame_boton_ingresar = tk.Frame(root)
        frame_boton_ingresar.pack(fill=tk.BOTH, pady=10)
        boton_ingresar = tk.Button(frame_boton_ingresar, text="Proyectar", command=lambda: al_pinchar(lista, cuadrito_de_proyeccion, Albergues_leido))
        boton_ingresar.pack(side=tk.RIGHT, anchor="se", padx=10)

        root.mainloop()

def interfaz_ingresar_albergues():

    root = tk.Toplevel()
    root.attributes('-topmost',True)
    root.title('Ingresar albergues')
    centrar_ventana(root, 0)

    tk.Label(root, text = 'Nombre del albergue:').pack()
    nombre_del_albergue = tk.Entry(root, width = 30)
    nombre_del_albergue.pack()

    tk.Label(root, text = 'Latitud del albergue:').pack()
    latitud_albergue = tk.Entry(root, width = 30)
    latitud_albergue.pack()

    tk.Label(root, text = 'Longitud del albergue:').pack()
    longitud_albergue = tk.Entry(root, width = 30)
    longitud_albergue.pack()

    tk.Label(root, text = 'Capacidad de personas:').pack()
    cap_personas = tk.Entry(root, width = 30)
    cap_personas.pack()

    tk.Label(root, text = 'Cantidad de personas:').pack()
    cantidad_personas = tk.Entry(root, width = 30)
    cantidad_personas.pack()

    tk.Label(root, text = 'Capacidad de medicamentos:').pack()
    cap_medicamentos = tk.Entry(root, width = 30)
    cap_medicamentos.pack()
    
    tk.Label(root, text = 'Cantidad de medicamentos:').pack()
    cantidad_medicamentos = tk.Entry(root, width = 30)
    cantidad_medicamentos.pack()

    boton_ingresar= tk.Button(root, text = "Ingresar", command= lambda: ingresar_albergues(nombre_del_albergue.get(), [latitud_albergue.get(), longitud_albergue.get()], cap_personas.get(), cantidad_personas.get(), cap_medicamentos.get(), cantidad_medicamentos.get()))
    boton_ingresar.pack()
    

    root.mainloop()

def interfaz_ingresar_envios():

    try:
        Albergues_leido = leer_archivo("albergues.csv")
    except FileNotFoundError:
        Albergues_leido = []
    
    if len(Albergues_leido) >0:
        root = tk.Toplevel()
        root.attributes('-topmost',True)
        root.title('Ingresar envíos')
        centrar_ventana(root, 0)

        tk.Label(root, text = 'Nombre del albergue:').pack()
        nombre_del_albergue = tk.Entry(root, width = 30)
        nombre_del_albergue.pack()

        tk.Label(root, text = 'Paquetes a enviar (cant. entera):').pack()
        paquetes__enviados = tk.Entry(root, width = 30)
        paquetes__enviados.pack()

        boton_ingresar= tk.Button(root, text = "Ingresar", command= lambda: ingresar_envios(nombre_del_albergue.get(), paquetes__enviados.get()))
        boton_ingresar.pack()
        root.mainloop()
    else:
        generar_popup("Advertencia", "Ingrese al menos un albergue.")

def interfaz_editar_personas_albergue():

    try:
        Albergues_leido = leer_archivo("albergues.csv")
    except FileNotFoundError:
        Albergues_leido = []

    if len(Albergues_leido) >0:
        root = tk.Toplevel()
        root.attributes('-topmost',True)
        root.title('Editar albergues')
        centrar_ventana(root, 0)
        tk.Label(root, text = 'Nombre del albergue:').pack()
        nombre_del_albergue = tk.Entry(root, width = 30)
        nombre_del_albergue.pack()

        tk.Label(root, text = 'Nueva cantidad de personas:').pack()
        nueva_cant_personas = tk.Entry(root, width = 30)
        nueva_cant_personas.pack()

        boton_ingresar= tk.Button(root, text = "Ingresar", command= lambda: editar_personas_albergue(nombre_del_albergue.get(), nueva_cant_personas.get()))
        boton_ingresar.pack()
        
        root.mainloop()
    else:
        generar_popup("Advertencia", "Ingrese al menos un albergue.")

def cerrar_dia():
    respuesta = msgbox.askyesno("Cerrar día", "¿Quieres cerrar el día?")
    if respuesta == True:
        nueva_ventana("Cerrar día", ["Día actual: " + str(dia(1)+1) + "."], 7, 40, 0)
        act_paq_alm()
        return True
    else:
        return False 

def main():
    root = tk.Tk()
    root.attributes('-topmost',True)
    ancho = 800
    alto = 300
    root.minsize(ancho,alto)
    x = (root.winfo_screenwidth()//2)-(ancho//2)
    y = (root.winfo_screenheight()//2)-(alto//2)
    root.geometry("{}x{}+{}+{}".format(ancho, alto, x, y))
    root.title('Menú')

    root.grid_rowconfigure([0, 1, 2, 3, 4, 5, 6], weight=1, uniform="fila")
    root.grid_columnconfigure([0, 1, 2, 3, 4], weight=1, uniform="columna")

    bot_ingresar = tk.Button(root, text="Ingresar albergues", command= interfaz_ingresar_albergues)
    bot_ingresar.grid(row=1, column=1, sticky="nsew")

    bot_suministros = tk.Button(root, text="Enviar suministros", command= interfaz_ingresar_envios)
    bot_suministros.grid(row=1, column=3, sticky="nsew")

    bot_editar = tk.Button(root, text="Editar albergue", command= interfaz_editar_personas_albergue)
    bot_editar.grid(row=3, column=1, sticky="nsew")

    bot_proyeccion = tk.Button(root, text="Proyección de suministros", command=proyeccion_paquetes)
    bot_proyeccion.grid(row=3, column=3, sticky="nsew")

    bot_cerrar = tk.Button(root, text="Cerrar día", command= cerrar_dia)
    bot_cerrar.grid(row=5, column=2, sticky="nsew")

    root.mainloop()

if __name__ == "__main__":
    main()
