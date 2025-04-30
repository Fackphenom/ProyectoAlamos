# Conexión a servidor mysql --- Recuerde actualizar cada 6 meses la IP del server.

from mysql.connector.locales.eng import client_error
import mysql.connector

class Comunication():
     def __init__(self) :
          self.conexion=mysql.connector.connect(host="152.202.96.38",                                               
                                      user="select_update_delete",
                                      passwd = "auto_selected@2024",
                                      database = "datosmo",
                                      charset="utf8"
                                      )
                                       
          self.cursor= self.conexion.cursor()
            

     def conectar(self):
         return self.conexion
     
