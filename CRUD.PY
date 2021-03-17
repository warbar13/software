from tkinter import *
from tkinter import messagebox
import sqlite3

def conexionBBDD():  #funcion base de  datos
    
    miConexion=sqlite3.connect("Usuarios") #  se  crea  variable y nombre BD

    miCursor=miConexion.cursor()

    try:

        miCursor.execute('''
            CREATE TABLE DATOSUSUARIOS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE_USUARIO VARCHAR(50),
            PASSWORD VARCHAR(50),
            APELLIDO VARCHAR(10),
            DIRECCION VARCHAR(50),
            COMENTARIOS VARCHAR(100))
            
        ''')
            
        messagebox.showinfo("BBDD", "BBDD  Creada con exito")

    except:

        messagebox.showwarning("¡Atencion!", "La  base  ya esta creada")


def salirAplicacion():

    valor=messagebox.askquestion("Salir", "¿Quieres Salir de la Aplicación?")

    if valor=="yes":
        root.destroy()

def limpiarCampos():

    miNombre.set("")
    miId.set("")
    miApellido.set("")
    miDireccion.set("")
    textoComentario.delete(1.0, END)
    miPass.set("")

def crear():
    miConexion=sqlite3.connect("Usuarios")

    miCursor=miConexion.cursor()
#Vamos realizar consultas parametrizadas con una  variable y evitar anidaciones   
     
    datos=miNombre.get(),miPass.get(),miApellido.get(),miDireccion.get(),textoComentario.get("1.0", END)

    #miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES(NULL, '" + miNombre.get() +
    #    "','" + miPass.get() +
    #    "','" + miApellido.get() +
    #    "','" + miDireccion.get() +
    #    "','" + textoComentario.get("1.0", END) + "')")

    miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES(NULL,?,?,?,?,?)",(datos))

    miConexion.commit()

    messagebox.showinfo("BBDD", "Registro Insertado Correctamente")

def leer():

    miConexion=sqlite3.connect("Usuarios")

    miCursor=miConexion.cursor()

    miCursor.execute("SELECT * FROM DATOSUSUARIOS WHERE ID=" + miId.get())

    elUsuario=miCursor.fetchall()  # fetchall  funcion devuelve un array con las coincidencias de la consulta
    
    for usuario in elUsuario:

        miId.set(usuario[0])
        miNombre.set(usuario[1])
        miPass.set(usuario[2])
        miApellido.set(usuario[3])
        miDireccion.set(usuario[4])
        textoComentario.insert(1.0, usuario[5])

    miConexion.commit()

def actualizar():
    miConexion=sqlite3.connect("Usuarios")

    miCursor=miConexion.cursor()
    #SET es para establecer
    #Vamos realizar consultas parametrizadas con una  variable y evitar anidaciones 
    datos=miNombre.get(),miPass.get(),miApellido.get(),miDireccion.get(),textoComentario.get("1.0", END)
    """miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO='" + miNombre.get() +
       "', PASSWORD='" + miPass.get() +
       "', APELLIDO='" + miApellido.get() +
       "', DIRECCION='" + miDireccion.get() +
       "', COMENTARIOS='" + textoComentario.get("1.0", END) +
       "' WHERE ID=" + miId.get())"""
    
    miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO=?,PASSWORD=?,APELLIDO=?,DIRECCION=?,COMENTARIOS=? " +
       "WHERE ID=" + miId.get(),(datos))


    miConexion.commit()

    messagebox.showinfo("BBDD", "Registro Actualizado Correctamente OK.")

def eliminar():

    miConexion=sqlite3.connect("Usuarios")

    miCursor=miConexion.cursor()

    miCursor.execute("DELETE FROM DATOSUSUARIOS WHERE ID=" + miId.get())

    miConexion.commit()

    messagebox.showinfo("BBDD", "Su registro Eliminado")


root=Tk()

barraMenu=Menu(root)
root.config(menu=barraMenu, width=300, height=300)


bbddmenu=Menu(barraMenu, tearoff=0)
bbddmenu.add_command(label="Conectar", command=conexionBBDD)
bbddmenu.add_command(label="Salir", command=salirAplicacion)

borrarmenu=Menu(barraMenu, tearoff=0)
borrarmenu.add_command(label="Borrar  Campos", command=limpiarCampos)

crudmenu=Menu(barraMenu, tearoff=0)
crudmenu.add_command(label="Crear", command=crear)
crudmenu.add_command(label="Leer", command=leer)
crudmenu.add_command(label="Actualizar", command=actualizar)
crudmenu.add_command(label="Borrar", command=eliminar)

ayudamenu=Menu(barraMenu, tearoff=0)
ayudamenu.add_command(label="Licencia")
ayudamenu.add_command(label="Acerca De....")

barraMenu.add_cascade(label="BBDD", menu=bbddmenu)  #esto crea lista de opciones en la barra superior
barraMenu.add_cascade(label="Borrar", menu=borrarmenu)
barraMenu.add_cascade(label="CRUD", menu=crudmenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudamenu)

#------Comienza Campos parte inferior--------

miFrame=Frame(root)
miFrame.pack()

miId=StringVar()  #se  debe utilizar Stringvar para procesos del Entry
miNombre=StringVar()
miApellido=StringVar()
miPass=StringVar()
miDireccion=StringVar()

cuadroID=Entry(miFrame, textvariable=miId)
cuadroID.grid(row=0, column=1, padx=10, pady=10)

cuadroNombre=Entry(miFrame, textvariable=miNombre)
cuadroNombre.grid(row=1, column=1, padx=10, pady=10)
cuadroNombre.config(fg="red", justify="right")
#cuadroNombre.config(fg="red", justify="right")

cuadroPass=Entry(miFrame, textvariable=miPass)
cuadroPass.grid(row=2, column=1, padx=10, pady=10)
cuadroPass.config(show="#")

cuadroApellido=Entry(miFrame, textvariable=miApellido)
cuadroApellido.grid(row=3, column=1, padx=10, pady=10)

cuadroDireccion=Entry(miFrame, textvariable=miDireccion)
cuadroDireccion.grid(row=4, column=1, padx=10, pady=10)

textoComentario=Text(miFrame, width=16, height=5)
textoComentario.grid(row=5, column=1, padx=10, pady=10)
scrollVert=Scrollbar(miFrame, command=textoComentario.yview)
scrollVert.grid(row=5, column=2, sticky="nsew")

textoComentario.config(yscrollcommand=scrollVert.set)
#---- creacion de  label Izquierdo-----------

idlabel=Label(miFrame, text="Id: ")
idlabel.grid(row=0, column=0, sticky="e", padx=10, pady=10)

nombrelabel=Label(miFrame, text="Nombre: ")
nombrelabel.grid(row=1, column=0, sticky="e", padx=10, pady=10)

passlabel=Label(miFrame, text="Password: ")
passlabel.grid(row=2, column=0, sticky="e", padx=10, pady=10)

apellidolabel=Label(miFrame, text="Apellido: ")
apellidolabel.grid(row=3, column=0, sticky="e", padx=10, pady=10)

direccionlabel=Label(miFrame, text="Direccion: ")
direccionlabel.grid(row=4, column=0, sticky="e", padx=10, pady=10)

Comentarioslabel=Label(miFrame, text="Comentarios: ")
Comentarioslabel.grid(row=5, column=0, sticky="e", padx=10, pady=10)

#------------Aqui  van los  Botones-------------



miFrame2=Frame(root)
miFrame2.pack()

botonCrear=Button(miFrame2, text="Crear", command=crear)
botonCrear.grid(row=1, column=0, sticky="e", padx=10, pady=10)

botonLeer=Button(miFrame2, text="Leer", command=leer)
botonLeer.grid(row=1, column=1, sticky="e", padx=10, pady=10)

botonActualizar=Button(miFrame2, text="Actualizar", command=actualizar)
botonActualizar.grid(row=1, column=2, sticky="e", padx=10, pady=10)

botonBorrar=Button(miFrame2, text="Eliminar", command=eliminar)
botonBorrar.grid(row=1, column=3, sticky="e", padx=10, pady=10)

root.mainloop()