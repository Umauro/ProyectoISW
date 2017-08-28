import sqlite3 as lite

class query():
    def __init__(self, *args, **kwargs):
        self.databaseName = 'database.db'
        self.con = None
        self.cur = None

    def isActived(self):
        if(self.con != None):
            return True
        else:
            return False

    def isClosed(self):
        if(self.con == None):
            return True
        else:
            return False

    def conectar(self):
        self.con = lite.connect(self.databaseName)
        self.cur = self.con.cursor()

    def desconectar(self):
        self.cur = None
        self.con.close()

    def insert(self, *args, **kwargs):
        try:
            if(kwargs['tabla'] == 'Confiable'):
                querySql = "INSERT INTO " + kwargs['tabla'] +"(Dominio, URL) VALUES(\'"+ kwargs['dominio'] +"\',\'"+ kwargs['url'] +"\');"
                self.cur.execute(querySql)
                self.con.commit()
            elif(kwargs['tabla'] == 'ListaNegra'):
                querySql = "INSERT INTO " + kwargs['tabla'] +"(StringBusqueda, Dominio, Titulo, tipoHerramienta) VALUES(\'"+kwargs['stringBusqueda']+"\',\'"+ kwargs['dominio'] +"\',\'"+ kwargs['titulo'] +"\',\'" + kwargs['tipoHerramienta'] + "\');"
                self.cur.execute(querySql)
                self.con.commit()
            elif(kwargs['tabla'] == 'ListaNegraImagen'):
                querySql = "INSERT INTO " + kwargs['tabla'] +"(StringBusqueda, Dominio, tipoHerramienta) VALUES(\'"+kwargs['stringBusqueda']+"\',\'"+ kwargs['dominio'] +"\',\'"+ kwargs['tipoHerramienta'] + "\');"
                self.cur.execute(querySql)
                self.con.commit()
            elif(kwargs['tabla'] == 'Cache'):
                querySql = "INSERT INTO " + kwargs['tabla'] + "(StringBusqueda, Dominio, URL) VALUES(\'"+kwargs['stringBusqueda']+"\',\'"+ kwargs['dominio'] +"\',\'"+ kwargs['url'] + "\');"
                self.cur.execute(querySql)
                self.con.commit()

        except AttributeError:
            print("Error en la cantidad de atributos")
        except TypeError:
            print("Error en tipos de atributos")
        except lite.OperationalError:
            print("Error en la consulta sql insert")
        except lite.DatabaseError:
            print("Error con la base de datos"+str(lite.DatabaseError[0]))
        except KeyError:
            print("Parámetro no encontrado")
        except lite.IntegrityError:
            print("Registro ya ingresado en la base de datos")



    def select(self, campos = "*", where = "", *args, **kwargs):
        try:
            querySql = "SELECT "+ campos +" FROM " +kwargs['tabla'] +" "+ where +";"
            print(querySql)
            self.cur.execute(querySql)
            rows = self.cur.fetchall()
            return rows

        except AttributeError:
            print("Error en la cantidad de atributos")
        except TypeError:
            print("Error en tipos de atributos")
        except lite.OperationalError:
            print("Error en la consulta sql select")
        except lite.DatabaseError:
            print("Error con la base de datos: ")



    def update(self, *args, **kwargs):
        try:
            querySql = "UPDATE "+ kwargs['tabla'] + " SET Dominio=\'"+ kwargs['dominioNuevo']+"\', URL=\'"+ kwargs['url']+"\' WHERE Dominio =\'"+kwargs['dominioAntiguo']+"\';"
            self.cur.execute(querySql)
            self.con.commit()

        except AttributeError:
            print("Error en la cantidad de atributos")
        except TypeError:
            print("Error en tipos de atributos")
        except lite.OperationalError:
            print("Error en la consulta sql")
        except lite.DatabaseError:
            print("Error con la base de datos")


    def delete(self, where ="", *args, **kwargs):
        if(where == ""):
            return None
        try:
            querySql = "DELETE FROM " + kwargs['tabla'] + " " + where +";"
            print(querySql)
            self.cur.execute(querySql)
            self.con.commit()
            print("Eliminado")

        except AttributeError:
            print("Error en la cantidad de atributos")
        except TypeError:
            print("Error en tipos de atributos")
        except lite.OperationalError:
            print("Error en la consulta sql")
        except lite.DatabaseError:
            print("Error con la base de datos")
"""
Función: insert(*args, **kwargs)

Función para insertar elementos a la base de datos utilizada

Uso:
    llamar a la función de la siguiente manera
    Confiable:
    .insert(tabla = <nombre_tabla>, dominio = <nombre_dominio>, url = <URL>)

    ListaNegra:
    .insert(tabla = <nombre_tabla>, dominio = <nombre_dominio>, titulo = <nombre_titulo>, tipoHerramienta = <tipo_Herramienta>)
    Donde <nombre_tabla> = {Confiable, ListaNegra}
"""

"""
Función: select(campos = "*",where ="", *args, **kwargs)

Función para seleccionar elementos desde la base de datos

Uso:
    llamar a la función de la siguiente manera
    .select(<campos Requeridos>,<sentencia WHERE>, tabla = '<nombre_tabla>')


    Donde <nombre_tabla> = {Confiable, ListaNegra}
    En atributo campo debe ser un string con los campos requeridos desde la tabla
    EJ:
        .select("Dominio, URL", tabla="Confiable")

Retorno:
    Una lista de tuplas con los campos requeridos
"""

"""
Función update(*args, **kwargs)

Función para realizar Update de campos en la base de datos
Uso:
    llamar a la función de la siguiente manera
    .update(tabla = <nombre_tabla>, dominioNuevo = <nuevo_dominio>, url = <nueva_url>, dominioAntiguo = <dominio_antiguo>)
    Donde <nombre_tabla> = {Confiable, ListaNegra}
"""

"""
Ejemplos de uso
queryClass = query()
queryClass.conectar()
queryClass.insert(tabla="Confiable", dominio="Testo", url="httpASHDAHD")
queryClass.select('Dominio',tabla='Confiable')
queryClass.select(tabla='Confiable')
queryClass.update(tabla='Confiable', dominioNuevo='Me Updatearon', url='meUpdatearon.com', dominioAntiguo='Testo')
"""
