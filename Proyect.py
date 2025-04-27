
from tkinter import  StringVar,END
import customtkinter as ctk
from PIL import Image
import os
from MysqlConector import *
import hashlib
from tkcalendar import DateEntry
from babel import numbers
import pyperclip


class Login(ctk.CTk):
    width = 320
    height = 450
    credenciales = Comunication()
    credenciales.conectar()
    con = credenciales.conectar()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        usuario = StringVar()
        password = StringVar()
       
        self.customap = ctk.set_appearance_mode("light")
        self.setcolor = ctk.set_default_color_theme("dark-blue")
        self.title("Operaciones Campo/Login Principal")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        self.state('zoomed')
    
        
        self.center_frame = ctk.CTkFrame(master=self)
        self.center_frame.pack(expand=True, fill="both")

        self.login_frame = ctk.CTkFrame(master=self.center_frame)
        self.login_frame.pack(expand=True, padx=50, pady=50)
        
        image_path = os.path.join(os.path.dirname(__file__), "imat.png") 
        self.only_image =ctk.CTkImage(Image.open(os.path.join(image_path)), size=(200, 200))

        self.navigation_label = ctk.CTkLabel(self.login_frame, text='', image=self.only_image, compound="center")
        self.navigation_label.grid(row=0, column=0, padx=5, pady=(5, 0))

        self.login_label = ctk.CTkLabel(self.login_frame, text="Inicio de sesión", font=ctk.CTkFont(size=25, weight="bold"))
        self.login_label.grid(row=1, column=0, padx=30, pady=(30, 15), sticky="n")

        self.username_entry = ctk.CTkEntry(self.login_frame , width=200, placeholder_text="Usuario")
        self.username_entry.grid(row=2, column=0, padx=30, pady=(30, 0))
        self.username_entry.bind("<Return>", self.bind_enter)




        self.password_entry = ctk.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="Contraseña")
        self.password_entry.grid(row=3, column=0, padx=30, pady=(0, 30))
        self.password_entry.bind("<Return>", self.bind_enter)


        self.lblmensaje = ctk.CTkLabel(self.login_frame, text="")
        self.lblmensaje.grid(row=5, column=0, padx=30, pady=(0, 15))

    def bind_enter(self, event):
        # Llama a la función loggin cuando se presiona Enter
        self.loggin()

    def loggin(self):
        usuario = self.username_entry.get()
        password = self.password_entry.get()

        if self.validar_login(usuario, password):
            self.lblmensaje.configure(text="Bienvenido")                  
            self.destroy()
            main_window = Main()
            main_window.mainloop()
            
            
            
        else:
            self.lblmensaje.configure(text="Usuario o contraseña incorrectos")

  

    def validar_login(self, usuario, password):
        conexion = self.credenciales.conectar()
        cursor = conexion.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            # Primero intenta buscar en la tabla "operaciones"
            sql = "SELECT * FROM operaciones WHERE USUARIO = %s AND CLAVE = %s"
            cursor.execute(sql, (usuario, hashed_password))
            validacion = cursor.fetchall()
            cursor.close()

            if validacion:
                return True

            else:
                # Si no se encuentra en "operaciones", intenta buscar en "Usuarios_Red"
                cursor = conexion.cursor()
                sql = "SELECT * FROM Usuarios_Red WHERE USUARIO = %s AND CLAVE = %s"
                
                cursor.execute(sql, (usuario, hashed_password))
                validacion = cursor.fetchall()
                cursor.close()

                if validacion:

                    self.lblmensaje.configure(text="Bienvenido", text_color="green",font=ctk.CTkFont(size=20, weight="bold"))
                    return True

                else:

                    self.lblmensaje.configure(text="Usuario o contraseña incorrectos", text_color="red",font=ctk.CTkFont(size=20, weight="bold"))
                    return False

        except Exception as e:

            print("Error:", e)
            self.lblmensaje.configure(text="Error al iniciar sesión. Intente nuevamente.", text_color="red",font=ctk.CTkFont(size=20, weight="bold"))
            return False

    def loggin(self):
        usuario = self.username_entry.get()
        password = self.password_entry.get()

        if self.validar_login(usuario, password):
            self.lblmensaje.configure(text="Bienvenido")                  
            self.destroy()
            if self.usuario_en_usuarios_red(usuario):
                main_window = Main()
            else:
                main_window = MainUsers()
            main_window.mainloop()
            
        else:
            self.lblmensaje.configure(text="Usuario o contraseña incorrectos")

    def usuario_en_usuarios_red(self, usuario):
        conexion = self.credenciales.conectar()
        cursor = conexion.cursor()
        try:


            sql = "SELECT * FROM Usuarios_Red WHERE USUARIO = %s"
            cursor.execute(sql, (usuario,))
            validacion = cursor.fetchall()
            cursor.close()
            return bool(validacion)
        except Exception as e:
            # Manejo de errores
            print("Error:", e)
            return False

              
if __name__ == "__main__":
    
    con = Comunication()
    app = Login()
    app.mainloop()
    
    
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, StringVar,END
import customtkinter as ctk
from PIL import Image
from MysqlConector import Comunication
import os
from tkcalendar import DateEntry
from babel import numbers
import subprocess
from tkcalendar import DateEntry
import pandas as pd

class Main(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.winempleados_ing = None
        self.customap_main = ctk.set_appearance_mode("light")
        self.setcolor_main = ctk.set_default_color_theme("dark-blue")
        self.title("Main Movistar")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.var_s()
        self.Interface_User()
    def var_s(self) :   
        self.windoempleadosC = None
        self.Empleados_X_In = None
        self.Empleados_X_Con = None
        self.Empleados_X_Re = None
        self.AccesoXCon = None
        self.AccesoXCre = None                
        self.PXAgregar= None
        self.PXConsultar= None
        self.AdminXUserN= None
        self.AdminXLA= None
        
        
    def Interface_User(self):
        image_path = os.path.join(os.path.dirname(__file__), "imt2.png") 
        self.only_image = ctk.CTkImage(Image.open(os.path.join(image_path)), size=(300, 90))

        self.content_frame = ctk.CTkFrame(self.winempleados_ing)
        # Modifica estos valores para ajustar el tamaño del frame 
        self.content_frame.grid(row=0, column=0,  sticky="ns")
        self.content_frame.columnconfigure(0, weight=1)

        # Ajustar la configuración de la cuadrícula principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)



        self.navigation_label = ctk.CTkLabel(master=self.content_frame, text='', image=self.only_image, compound="center",font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_label.grid(row=1, column=1, padx=20, pady=(5, 5), columnspan=4,rowspan=1)
        
        self.login_label = ctk.CTkLabel(master=self.content_frame, text="Gestor de Personas", font=ctk.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=2, column=1, padx=40, pady=(5, 5), columnspan=4,rowspan=1)

        self.login_label = ctk.CTkLabel(master=self.content_frame, text="Gestor de Nodos", font=ctk.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=4, column=1, padx=40, pady=(5, 5), columnspan=4,rowspan=1)

        self.login_label = ctk.CTkLabel(master=self.content_frame, text="Gestor de Permisos", font=ctk.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=6, column=1, padx=40, pady=(5, 5), columnspan=4,rowspan=1)

        self.administratoroptiosn = ctk.CTkLabel(master=self.content_frame, text="Opciones de Administrador", font=ctk.CTkFont(size=20, weight="bold"))
        self.administratoroptiosn.grid(row=8, column=1, padx=40, pady=(5, 5), columnspan=4,rowspan=1)
        
        
        self.lblempty = ctk.CTkLabel(master=self.content_frame,text="")
        self.lblempty.grid(row=0, column=1, padx=40, pady=100, columnspan=5, sticky="nsew")



        ctk.CTkButton(master=self.content_frame, text="Registro", hover_color='#006e44', command=self.EmpleadosXIngreso, font=ctk.CTkFont(size=12, weight="bold")).grid(row=3  , column=0, padx=(0, 200), pady=(15, 5), columnspan=4,rowspan=1)
        ctk.CTkButton(master=self.content_frame, text="Consulta", hover_color='#006e44', command=self.EmpleadosXConsultas, font=ctk.CTkFont(size=12, weight="bold")).grid(row=3  , column=1, padx=(200, 200), pady=(15, 5), columnspan=4,rowspan=1)
        ctk.CTkButton(master=self.content_frame, text="Actualización", hover_color='#006e44', command=self.EmpleadosXRemover, font=ctk.CTkFont(size=12, weight="bold")).grid(row=3  , column=2, padx=(200, 0), pady=(15, 5), columnspan=4,rowspan=1)
        
        ctk.CTkButton(master=self.content_frame, text="Registro", hover_color='#006e44', command=self.AccesoXCrear, font=ctk.CTkFont(size=12, weight="bold")).grid(row=7  , column=0, padx=(0, 200), pady=(15, 5), columnspan=4,rowspan=1)
        ctk.CTkButton(master=self.content_frame, text="Consulta", hover_color='#006e44', command=self.AccesoXConsultar, font=ctk.CTkFont(size=12, weight="bold")).grid(row=7  , column=1, padx=(200, 200), pady=(15, 5), columnspan=4,rowspan=1)
        ctk.CTkButton(master=self.content_frame, text="Solicitud", hover_color='#006e44', font=ctk.CTkFont(size=12, weight="bold")).grid(row=7  , column=2, padx=(200, 0), pady=(15, 5), columnspan=4,rowspan=1)

        
        ctk.CTkButton(master=self.content_frame, text="Registro", hover_color='#006e44', command=self.PtransXAgregar, font=ctk.CTkFont(size=12, weight="bold")).grid(row=5  , column=0, padx=(0, 200), pady=(15, 5), columnspan=4,rowspan=1)
        ctk.CTkButton(master=self.content_frame, text="Consulta", hover_color='#006e44', command=self.PtransXConsultar, font=ctk.CTkFont(size=12, weight="bold")).grid(row=5  , column=1, padx=(200, 200), pady=(15, 5), columnspan=4,rowspan=1)
        ctk.CTkButton(master=self.content_frame, text="Actualización", hover_color='#006e44',command=self.PtransXUpdate, font=ctk.CTkFont(size=12, weight="bold")).grid(row=5  , column=2, padx=(200, 0), pady=(15, 5), columnspan=4,rowspan=1)

        
        ctk.CTkButton(master=self.content_frame, text="Usuario Nuevo", hover_color='#006e44', command=self.AdminXAgregarNUser, font=ctk.CTkFont(size=12, weight="bold")).grid(row=9  , column=0, padx=(0, 200), pady=(15, 5), columnspan=4,rowspan=1)
        ctk.CTkButton(master=self.content_frame, text="Carga Masiva", hover_color='#006e44', command=self.AdminXDataMassive, font=ctk.CTkFont(size=12, weight="bold")).grid(row=9  , column=1, padx=(200, 200), pady=(15, 5), columnspan=4,rowspan=1)
        ctk.CTkButton(master=self.content_frame, text="Remover Usuario", hover_color='#006e44', font=ctk.CTkFont(size=12, weight="bold")).grid(row=9  , column=2, padx=(200, 0), pady=(15, 5), columnspan=4,rowspan=1)
    def EmpleadosXIngreso(self):
        
                self.Empleados_X_In = Login()
                self.Empleados_X_In.title("Formulario Empleados")  # Set title for FormularioP window
                self.Empleados_X_In.mainloop()

    def EmpleadosXConsultas(self):
       
                self.Empleados_X_Con = Login()
                self.Empleados_X_Con.title("Consultado Empleados")  # Set title for FormularioP window
                self.Empleados_X_Con.mainloop()
    def EmpleadosXRemover(self):
        
            ruta =  os.path.join(os.path.dirname(__file__), "_SoftEACCPT", "SoftEmRemoved.exe")
            try :
                subprocess.Popen([ruta])
            except FileNotFoundError:
                messagebox.showerror(title="Archivo Not Found")
    def AccesoXConsultar(self):
        
                self.AccesoXCon = Login()
                self.AccesoXCon.title("Formulario Permisos")  # Set title for FormularioP window
                self.AccesoXCon.mainloop()

    def AccesoXCrear(self):
                self.AccesoXCre = Login()
                self.AccesoXCre.title("Sitios Mensuales")  # Set title for FormularioP window
                self.AccesoXCre.mainloop() 
     
    def PtransXAgregar(self):
            ruta =  os.path.join(os.path.dirname(__file__), "_SoftEACCPT", "PTaddSoft.exe")
            try :
                subprocess.Popen([ruta])
            except FileNotFoundError:
                messagebox.showerror(title="Archivo Not Found")

    def PtransXConsultar(self):
            ruta =  os.path.join(os.path.dirname(__file__), "_SoftEACCPT", "PTCheckSoft.exe")
            try :
                subprocess.Popen([ruta])
            except FileNotFoundError:
                messagebox.showerror(title="Archivo Not Found")
                
    def PtransXUpdate(self):
            ruta =  os.path.join(os.path.dirname(__file__), "_SoftEACCPT", "PTUpdateSoft.exe")
            try :
                subprocess.Popen([ruta])
            except FileNotFoundError:
                messagebox.showerror(title="Archivo Not Found")
    
    
    def AdminXAgregarNUser(self):
                self.AdminXUserN = Login()
                self.AdminXUserN.title("Formulario Permisos")  # Set title for FormularioP window
                self.AdminXUserN.mainloop()

    def AdminXDataMassive(self):
                self.AdminXLA = Login()
                self.AdminXLA.title("Formato de DB Massive")  # Set title for FormularioP window
                self.AdminXLA.mainloop() 

if __name__ == "__main__":
    app = Main()
    app.mainloop()

from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
from MysqlConector import Comunication
import os, subprocess





class MainUsers(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.winempleados_ing = None
        self.customap_main = ctk.set_appearance_mode("light")
        self.setcolor_main = ctk.set_default_color_theme("dark-blue")
        self.title("Main Movistar")
        self.windoempleadosC = None
        # Initialize attributes for FormularioP, ConsultasR, and EliminarR windows

        self.Empleados_X_Con = None

        self.AccesoXCon = None
   
        self.PXConsultar= None
     
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.geometry(f"{screen_width}x{screen_height}+0+0")

        image_path = os.path.join(os.path.dirname(__file__), "imt2.png") 
        self.only_image = ctk.CTkImage(Image.open(os.path.join(image_path)), size=(300, 90))

        self.content_frame = ctk.CTkFrame(self.winempleados_ing)
        # Modifica estos valores para ajustar el tamaño del frame 
        self.content_frame.grid(row=0, column=0,  sticky="ns")
        self.content_frame.columnconfigure(0, weight=1)

        # Ajustar la configuración de la cuadrícula principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)



        self.navigation_label = ctk.CTkLabel(master=self.content_frame, text='', image=self.only_image, compound="center",font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_label.grid(row=1, column=1, padx=20, pady=(5, 5), columnspan=4,rowspan=1)


        self.login_label = ctk.CTkLabel(master=self.content_frame, text="Gestor de Nodos", font=ctk.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=4, column=1, padx=40, pady=(5, 5), columnspan=4,rowspan=1)

        self.login_label = ctk.CTkLabel(master=self.content_frame, text="Gestor de Permisos", font=ctk.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=6, column=1, padx=40, pady=(5, 5), columnspan=4,rowspan=1)


        
        
        self.lblempty = ctk.CTkLabel(master=self.content_frame,text="")
        self.lblempty.grid(row=0, column=1, padx=40, pady=100, columnspan=5, sticky="nsew")



        ctk.CTkButton(master=self.content_frame, text="Consulta", hover_color='#006e44', command=self.AccesoXConsultar, font=ctk.CTkFont(size=12, weight="bold")).grid(row=7  , column=1, padx=(200, 200), pady=(15, 5), columnspan=4,rowspan=1)
        ctk.CTkButton(master=self.content_frame, text="Consulta", hover_color='#006e44', command=self.PtransXConsultar, font=ctk.CTkFont(size=12, weight="bold")).grid(row=5  , column=1, padx=(200, 200), pady=(15, 5), columnspan=4,rowspan=1)
    
   



   
    def AccesoXConsultar(self):
        
                self.AccesoXCon = AccesoXExportar()
                self.AccesoXCon.title("Formulario Permisos")  # Set title for FormularioP window
                self.AccesoXCon.mainloop()

   
    def PtransXConsultar(self):
            ruta =  os.path.join(os.path.dirname(__file__), "_SoftEACCPT", "PTCheckSoft.exe")
            try :
                subprocess.Popen([ruta])
            except FileNotFoundError:
                messagebox.showerror(title="Archivo Not Found")
           
           
                

    


    
if __name__ == "__main__":
    app = MainUsers()
    app.mainloop()
    
    
import tkinter as tk
from tkinter import ttk, StringVar,END
import pandas as pd
import mysql.connector
from MysqlConector import Comunication
import customtkinter as ctk
import subprocess
import os 
import pyperclip


class AccesoXExportar(ctk.CTk):
    width = 1400    
    height = 960
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.custom_movistar = ctk.set_appearance_mode("light")
        self.custom_movistar = ctk.set_default_color_theme("blue")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        self.state('zoomed')
        self.resizable(False,False)
        self.title("AccesoX/EXPORTAR CONTENIDO")
        self.datosmo = Comunication()
        self.datosmo.conectar()
        tabla_height_percentage = 0.039  

        
        
        self.tabla_height = int(screen_height * tabla_height_percentage)
        self.todos_los_permisos_consultados = []
        self.CONSULTASIDS = []
        self.owners_var = StringVar ()

        self.create_widgets()
        self.Names_into_DB_owner()
    
    def Names_into_DB_owner(self):
        self.owners_var = StringVar ()
        datosmo = Comunication()    
        sql = "SELECT TORRERO FROM consolidado_permisos"
        datosmo.cursor.execute(sql)
        filas = datosmo.cursor.fetchall()
        unique_owners = set()  # Set to store unique owners
        for row in filas:
            unique_owners.add(row[0])  # Add owner to the set
        
        lista_owners = list(unique_owners)
        self.TORREROGET["values"] = lista_owners 
        

    def create_widgets(self):
        torrero = StringVar ()
   
        
        self.CONSULTASIDS = []

        self.FRAME_PRINCIPAL_PERMISOS = ctk.CTkFrame(master=self)
        self.FRAME_PRINCIPAL_PERMISOS.grid(row=0, column=0, sticky="n") 
        # Se sobrepondrá al frame inferior
        self.FRAME_PRINCIPAL_PERMISOS.columnconfigure(0, weight=1)

        self.FRAME_INFERIOR_PERMISOS = ctk.CTkFrame(master=self)
        self.FRAME_INFERIOR_PERMISOS.grid(row=1, column=0, sticky="nsew")
        self.FRAME_INFERIOR_PERMISOS.columnconfigure(0, weight=1)

        # Ajustar la configuración de la cuadrícula principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.TABLA_INFERIOR_PERMISOS = ttk.Treeview(self.FRAME_INFERIOR_PERMISOS, height=self.tabla_height)
        self.TABLA_INFERIOR_PERMISOS.pack(fill=tk.BOTH, expand=True)
        ctk.CTkLabel(self.FRAME_PRINCIPAL_PERMISOS, text="Consulta Consolidado ",font=ctk.CTkFont(size=14, weight="bold"),text_color="black").grid(row=0, column=1, padx=0, pady=(10,10))
        ctk.CTkLabel(self.FRAME_PRINCIPAL_PERMISOS, text="Opciones",font=ctk.CTkFont(size=12, weight="bold")).grid(row=1, column=1, padx=10, pady=(10,2))
        ctk.CTkLabel(self.FRAME_PRINCIPAL_PERMISOS, text="ID MAXIMO:",font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=3, padx=30, pady=(5,5))
        ctk.CTkLabel(self.FRAME_PRINCIPAL_PERMISOS, text="ID SITIO:",font=ctk.CTkFont(size=12, weight="bold")).grid(row=1, column=3, padx=30, pady=(5,5))
        ctk.CTkLabel(self.FRAME_PRINCIPAL_PERMISOS, text="Torrero",font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=3, padx=30, pady=(5,5))
        ctk.CTkLabel(self.FRAME_PRINCIPAL_PERMISOS, text="Filtrar por Nombre del Nodo\n↓",font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=5, padx=30, pady=(5,5))
        self.botonpersonal=ctk.CTkButton(self.FRAME_PRINCIPAL_PERMISOS, text="Selecionar \nTodos los permisos",command=self.Allallowances, hover_color='#006e44', font=ctk.CTkFont(size=12, weight="bold"))
        self.botonpersonal.grid(row=1, column=2, padx=10, pady=(5,5))
        self.botonvaciarta=ctk.CTkButton(self.FRAME_PRINCIPAL_PERMISOS, text="Borrar Consulta",command=self.eliminar_consulta, hover_color='#006e44', font=ctk.CTkFont(size=12, weight="bold"))
        self.botonvaciarta.grid(row=2, column=2, padx=30, pady=(5,5))
        self.botonexportar =ctk.CTkButton(self.FRAME_PRINCIPAL_PERMISOS, text="Convertir a Excel",command=self.ExportarConsolidado, hover_color='#006e44', font=ctk.CTkFont(size=12, weight="bold"))
        self.botonexportar.grid(row=2, column=6, padx=30, pady=(5,5))
        self.IDSITIO = ctk.CTkEntry(self.FRAME_PRINCIPAL_PERMISOS, width=200)
        self.IDSITIO.grid(row=1, column=4, padx=30, pady=(5,5))
        self.IDSITIO.bind("<Return>", self.bind_enter_entries)
        self.IDMAXIMO = ctk.CTkEntry(self.FRAME_PRINCIPAL_PERMISOS, width=200)
        self.IDMAXIMO.grid(row=0, column=4, padx=30, pady=(5,5))
        self.IDMAXIMO.bind("<Return>", self.bind_enter_entries)
        self.site_name = ctk.CTkEntry(self.FRAME_PRINCIPAL_PERMISOS, width=200)
        self.site_name.grid(row=1, column=5, padx=30, pady=(5,5))
        self.site_name.bind("<Return>", self.bind_enter_entries)
        self.TORREROGET = ttk.Combobox(master=self.FRAME_PRINCIPAL_PERMISOS, textvariable=self.owners_var)
        self.TORREROGET.grid(row=2, column=4, padx=0, pady=(5,5))
        self.TORREROGET.set("<<Selección>>")
        self.TORREROGET.bind("<Return>", self.bind_enter_entries) 
        self.lblmensaje = ctk.CTkLabel(self.FRAME_PRINCIPAL_PERMISOS, text="")
        self.lblmensaje.grid(row=0, column=2, padx=0, pady=(5,5))
        

        self.TABLA_INFERIOR_PERMISOS['columns'] = ('ID MAXIMO', 'ID SITE', 'NOMBRE','RESPONSABLE',' COD_OPERADOR',' COD_TORRERO', 'NOMBRE_TORRERO', 'TORRERO', 'G_CONSECUTIVO1', 'PERIODO_AUTORIZADO', 'OBSERVACIONES', 'TIPO_INGRESO_LLAVES')
        for i in range(12):
            self.TABLA_INFERIOR_PERMISOS.column(f"#{i}", width=100, stretch=tk.YES)
            
        self.TABLA_INFERIOR_PERMISOS.heading("#0", text="MAXIMO ")
        self.TABLA_INFERIOR_PERMISOS.heading("#1", text="ID ")
        self.TABLA_INFERIOR_PERMISOS.heading("#2", text="NOMBRE/MOVISTAR ")
        self.TABLA_INFERIOR_PERMISOS.heading("#3", text="RESPONSABLE ")
        self.TABLA_INFERIOR_PERMISOS.heading("#4", text="COD_OPERADOR ")
        self.TABLA_INFERIOR_PERMISOS.heading("#5", text="COD_TORRERO ")
        self.TABLA_INFERIOR_PERMISOS.heading("#6", text="NOMBRE_TORRERO ")
        self.TABLA_INFERIOR_PERMISOS.heading("#7", text="TORRERO ")
        self.TABLA_INFERIOR_PERMISOS.heading("#8", text="G_CONSECUTIVO1")
        self.TABLA_INFERIOR_PERMISOS.heading("#9", text="PERIODO_AUTORIZADO")
        self.TABLA_INFERIOR_PERMISOS.heading("#10", text="OBSERVACIONES")
        self.TABLA_INFERIOR_PERMISOS.heading("#11", text="TIPO_INGRESO_LLAVES ")
        
        self.TABLA_INFERIOR_PERMISOS.column("#12", width=0)
        self.TABLA_INFERIOR_PERMISOS.bind("<<TreeviewSelect>>", self.copy_to_clipboard)
        self.Allallowances()

    
    
    def copy_to_clipboard(self, event):
        selected_item = self.TABLA_INFERIOR_PERMISOS.selection()
        if selected_item:
            values = self.TABLA_INFERIOR_PERMISOS.item(selected_item, 'values')
            row_str = '\t'.join(map(str, values))
            pyperclip.copy(row_str)
            
    def Allallowances(self):
        self.clear_table()
        datosmo = Comunication()                
        sql = "SELECT COD_MAXIMO, ID_SITIO, NOMBRE_MOVISTAR, RESPONSABLE, COD_OPERADOR, COD_TORRERO, NOMBRE_TORRERO, TORRERO, G_CONSECUTIVO1, PERIODO_AUTORIZADO, OBSERVACIONES, TIPO_INGRESO_LLAVES FROM consolidado_permisos "
        datosmo.cursor.execute(sql)
        filas = datosmo.cursor.fetchall()
        for item in filas:  
                id = item[0]      
                self.TABLA_INFERIOR_PERMISOS.insert("",END,text= id , values=item[1:])
                self.CONSULTASIDS.append(id)
                self.todos_los_permisos_consultados.append(id)
                self.lblmensaje.configure(text="Has verificado\ntodos los Permisos", text_color="green", font=ctk.CTkFont(size=12,weight="bold"))#             
                
                
    def VerificarPermiso(self):
        Torrero = self.TORREROGET.get()
        id_sitio = self.IDSITIO.get()
        Id_maximo = self.IDMAXIMO.get()    
        nombre_sitio = self.site_name.get()
        
        if id_sitio:
            datosmo = Comunication()
            sql = "SELECT COD_MAXIMO, ID_SITIO, NOMBRE_MOVISTAR, RESPONSABLE, COD_OPERADOR, COD_TORRERO, NOMBRE_TORRERO, TORRERO, G_CONSECUTIVO1, PERIODO_AUTORIZADO, OBSERVACIONES, TIPO_INGRESO_LLAVES FROM consolidado_permisos WHERE ID_SITIO =%s "
            datosmo.cursor.execute(sql,(id_sitio,))
            filas = datosmo.cursor.fetchall()
            self.IDSITIO.delete(0,tk.END)
            for item in filas:
                id = item[0]
                self.TABLA_INFERIOR_PERMISOS.insert("",END,id_sitio,text= id , values=item[1:])
                self.CONSULTASIDS.append(id)
                self.lblmensaje.configure(text=f"Has verificado\npor el Id_Sitio {id_sitio}", text_color="green",font=ctk.CTkFont(size=12,weight="bold"))
        elif Id_maximo:
            datosmo = Comunication()
            sql ="SELECT COD_MAXIMO, ID_SITIO, NOMBRE_MOVISTAR, RESPONSABLE, COD_OPERADOR, COD_TORRERO, NOMBRE_TORRERO, TORRERO, G_CONSECUTIVO1, PERIODO_AUTORIZADO, OBSERVACIONES, TIPO_INGRESO_LLAVES FROM consolidado_permisos WHERE COD_MAXIMO =%s"
            datosmo.cursor.execute(sql,(Id_maximo,))
            filas = datosmo.cursor.fetchall()
            self.IDMAXIMO.delete(0,tk.END)    
            for item in filas:
                id = item[0]
                self.TABLA_INFERIOR_PERMISOS.insert("",END,Id_maximo,text= id , values=item[1:])
                self.CONSULTASIDS.append(id)
                self.lblmensaje.configure(text=f"Has verificado\npor el Codigo Maximo {Id_maximo}", text_color="green",font=ctk.CTkFont(size=12,weight="bold"))
        
        elif nombre_sitio:# SELECION POR NOMBRES Y O SIMILITUDES  EN LOS MISMOS 
            datosmo = Comunication()
            sql = "SELECT COD_MAXIMO, ID_SITIO, NOMBRE_MOVISTAR, RESPONSABLE, COD_OPERADOR, COD_TORRERO, NOMBRE_TORRERO, TORRERO, G_CONSECUTIVO1, PERIODO_AUTORIZADO, OBSERVACIONES, TIPO_INGRESO_LLAVES FROM consolidado_permisos WHERE NOMBRE_MOVISTAR LIKE %s"
            nombre_sitio = f"%{nombre_sitio}%"
            datosmo.cursor.execute(sql, (nombre_sitio,))
            filas = datosmo.cursor.fetchall()
            self.site_name.delete(0, tk.END)
            for item in filas:
                id = item[0]
                self.TABLA_INFERIOR_PERMISOS.insert("", tk.END, text=id, values=item[1:])  # Corregir aquí
                self.CONSULTASIDS.append(id)
                self.lblmensaje.configure(text=f"Has verificado\npor el siguiente nombre {nombre_sitio}", text_color="green", font=ctk.CTkFont(size=12, weight="bold"))
                
        elif Torrero:
            datosmo = Comunication()
            sql ="SELECT COD_MAXIMO, ID_SITIO, NOMBRE_MOVISTAR, RESPONSABLE, COD_OPERADOR, COD_TORRERO, NOMBRE_TORRERO, TORRERO, G_CONSECUTIVO1, PERIODO_AUTORIZADO, OBSERVACIONES, TIPO_INGRESO_LLAVES FROM consolidado_permisos WHERE TORRERO =%s"
            datosmo.cursor.execute(sql,(Torrero,))
            filas = datosmo.cursor.fetchall()
            self.TABLA_INFERIOR_PERMISOS.delete(*self.TABLA_INFERIOR_PERMISOS.get_children())
            self.TORREROGET.set("<<SELECCIONE>>")
            for item in filas:
                id = item[0]
                self.TABLA_INFERIOR_PERMISOS.insert("",END,id,text= id , values=item[1:])
                self.CONSULTASIDS.append(id)
                self.lblmensaje.configure(text=f"Has verificado por el siguiente\nTorrero {Torrero}", text_color="green",font=ctk.CTkFont(size=12,weight="bold"))
        else:
            self.lblmensaje.configure(text="Por favor verifica si has completado algún espacio", text_color="red")

    def clear_table(self):
        self.TABLA_INFERIOR_PERMISOS.delete(*self.TABLA_INFERIOR_PERMISOS.get_children())
        
    def execute_query(self, sql):
        self.todos_los_permisos_consultados.clear()
        self.CONSULTASIDS.clear()
        self.datosmo.cursor.execute(sql)
        filas = self.datosmo.cursor.fetchall()
        
        for item in filas:
            id = item[0]
            self.TABLA_INFERIOR_PERMISOS.insert("", tk.END, id, text=id, values=item[1:])
            self.todos_los_permisos_consultados.append(id)
            self.CONSULTASIDS.append(id)
            
    def eliminar_consulta(self):
        self.clear_table()
        self.todos_los_permisos_consultados.clear()
        self.CONSULTASIDS.clear()
        self.lblmensaje.configure(text="")
        self.TORREROGET.set("<<SELECCIONE>>")
        self.todos_los_permisos_consultados.clear()
    def ExportarConsolidado(self):
        try:
            conn = mysql.connector.connect(host="152.202.96.38", user="pruebas", passwd="Autonorte2024", database="datosmo", charset="utf8")
            cursor = conn.cursor()

            if self.CONSULTASIDS:
                placeholders = ', '.join(['%s'] * len(self.CONSULTASIDS))
                sql = f"SELECT COD_MAXIMO, ID_SITIO, NOMBRE_MOVISTAR, RESPONSABLE, COD_OPERADOR, COD_TORRERO, NOMBRE_TORRERO, TORRERO, G_CONSECUTIVO1, PERIODO_AUTORIZADO, OBSERVACIONES, TIPO_INGRESO_LLAVES FROM consolidado_permisos WHERE COD_MAXIMO IN ({placeholders})"
                cursor.execute(sql, self.CONSULTASIDS)
                data = cursor.fetchall()

                if data:
                    df = pd.DataFrame(data, columns=['COD_MAXIMO', 'ID_SITIO', 'NOMBRE_MOVISTAR', 'RESPONSABLE', 'COD_OPERADOR', 'COD_TORRERO', 'NOMBRE_TORRERO', 'TORRERO', 'G_CONSECUTIVO1', 'PERIODO_AUTORIZADO', 'OBSERVACIONES', 'TIPO_INGRESO_LLAVES'])
                    archivo = os.path.join(os.path.dirname(__file__), "_internal", "Consolidado_de_permisos.xlsx")
                    df.to_excel(archivo, index=False)
                    self.lblmensaje.configure(text="Data exportada correctamente\nRecuerde cerrar el archivo\nexcel para realizar modificaciones", text_color="green",font=ctk.CTkFont(size=12, weight="bold"))
                    self.get_folder()
                else:
                    self.lblmensaje.configure(text="No se encontraron datos para exportar", text_color="red")

            else:
                self.lblmensaje.configure(text="No hay consultas seleccionadas para exportar", text_color="red")
        except mysql.connector.Error as e:
            print(e)
            self.lblmensaje.configure(text=f"Error al exportar los datos. Verifique la conexión y vuelva a intentarlo \n {e}.", text_color="red",font=ctk.CTkFont(size=12, weight="bold"))
        except Exception as ex:
            print(ex)
            self.lblmensaje.configure(text=f"Error inesperado. Inténtelo de nuevo más tarde\n {ex}.", text_color="red",font=ctk.CTkFont(size=12, weight="bold"))
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    def get_folder(self):
        archivo = os.path.join(os.path.dirname(__file__), "_internal")
        os.startfile(archivo)
    def bind_enter_entries(self, event):
        self.VerificarPermiso()

if __name__ == "__main__":
    formulario = AccesoXExportar()
    formulario.mainloop()
