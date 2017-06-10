import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter.scrolledtext import ScrolledText

from urllib.request import urlopen
import base64

import url_Obtainer
import query
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from BuscadordeHerramientasdeAprendizaje.spiders.tabla_spider import tablasSpider
from BuscadordeHerramientasdeAprendizaje.spiders.test_spider import imagenSpider

from scrapy.utils.log import configure_logging
from twisted.internet import reactor


class Aplicacion(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.regular_font = tkfont.Font(family='Helvetica', size=15, slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (menuPrincipal, materia, imagenes):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("menuPrincipal")

    def show_frame(self, tipo=None, campo=None):
        if tipo[0]==0: #Materia
            #Se debe borrar (dejar en blanco) cualquier txt previo
            """
            with open('Resultados/Materia.txt', 'w') as archivo:
                pass

            """
            #===================================================================
            #Inicio Busqueda de materia
            #===================================================================
            '''
            db = query.query()
            db.conectar()
            rows = db.select(tabla='Confiable')
            db.desconectar()
            listaConfiable = []

            for row in rows:
                a, b, c = row
                listaConfiable.append(b)


            url = url_Obtainer.urlObtainer(listaConfiable)
            listaUrl = url.urlGetter(campo)
            configure_logging()
            runner = CrawlerRunner().create_crawler(tablasSpider)
            d = runner.crawl(tablasSpider, start_urls = listaUrl)
            d.addBoth(lambda _: reactor.crash())
            reactor.run()'''


            #===================================================================
            #FIN Busqueda de materia
            #===================================================================

            frame = self.frames["materia"]
            frame.mostrar()

        elif tipo[0]==1:#Caso de imagenes
            """
            with open('Resultados/Imagenes.txt', 'w') as archivo:
                pass

            """
            #===================================================================
            #Inicio Busqueda de imágenes
            #===================================================================
            """
            db = query.query()
            db.conectar()
            rows = db.select(tabla='Confiable')
            db.desconectar()
            listaConfiable = []

            for row in rows:
                a, b, c = row
                listaConfiable.append(b)


            url = url_Obtainer.urlObtainer(listaConfiable)
            listaUrl = url.urlGetter(campo)
            configure_logging()
            runner = CrawlerRunner().create_crawler(imagenSpider)
            d = runner.crawl(imagenSpider, start_urls = listaUrl)
            d.addBoth(lambda _: reactor.crash())
            reactor.run()
            """
            #===================================================================
            #FIN Busqueda de imágenes
            #===================================================================
            frame = self.frames["imagenes"]
            frame.mostrar()
        else:
            #Se deben resetear los campos de los otros frames antes de volver
            self.frames["materia"].texto.delete("1.0", tk.END)
            self.frames["materia"].encontrados=list()


            for panel, titulo, url in self.frames["imagenes"].encontrados:
                panel.pack_forget()
                titulo.pack_forget()
            self.frames["imagenes"].encontrados=list()

            frame = self.frames["menuPrincipal"]
        frame.tkraise()
    def reportarFalsoPositivo(self, Dominio=None, Titulo=None, TipoHerramienta=None):
        print("Datos ingresados",Dominio," = ",Titulo," = ",TipoHerramienta)
        #=======================================================================
        #Aqui se debe hacer coneccion a base de datos y añadir lo seleccionado
        #=======================================================================

        ###PROBABLEMENTE AQUI HAY QUE HACER IFS PARA QUE DADO EL TIPO DE HERRAMIENTA SE HAGA UNA CONSULTA SQL DISTINTA
        if(TipoHerramienta == "materia"):
            db = query.query()
            db.conectar()
            db.insert(tabla='ListaNegra', stringBusqueda=self.frames['menuPrincipal'].entrada.get(), dominio = str(Dominio), titulo = str(Titulo), tipoHerramienta = str(TipoHerramienta))
            db.desconectar()

        elif(TipoHerramienta == "imagenes"):
            db = query.query()
            db.conectar()
            db.insert(tabla='ListaNegraImagen', stringBusqueda=self.frames['menuPrincipal'].entrada.get(), dominio = str(Dominio), tipoHerramienta = str(TipoHerramienta))
            print("INSERTÉ ALGO")
            db.desconectar()

        #=======================================================================
        #Fin añadir lo seleccionado
        #=======================================================================

class menuPrincipal(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Menu principal", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.entrada = tk.Entry(self, width= 50, font = controller.regular_font)
        self.entrada.pack()

        opcionesBusqueda = tk.Listbox(self, selectmode="Single", font = controller.regular_font)
        opcionesBusqueda.insert(tk.END, "Materia", "Imagenes")
        opcionesBusqueda.pack()

        botonBusqueda = tk.Button(self, text="Iniciar Busqueda", font = controller.regular_font,
                                       command = lambda: controller.show_frame( opcionesBusqueda.curselection() , self.entrada.get() ))
        botonBusqueda.pack()


class materia(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Materia", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.encontrados = list()
        self.spinbox= None

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frameCanvas = tk.Frame(self.canvas, background="#ffffff")
        self.canvas.create_window((4,4), anchor="nw" ,window=self.frameCanvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.frameCanvas.bind("<Configure>", self.onFrameConfigure)

        self.texto = tk.Text(self.frameCanvas, font=controller.regular_font,  wrap='word', height= 100, width= 115)

        self.botonRegreso = tk.Button(self, text="Volver al inicio", font= controller.regular_font,
                           command=lambda: controller.show_frame("menuPrincipal"))

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def mostrar(self):
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.botonRegreso.pack(side="left" ,padx=10, pady=5)

        #======================================================================
        #Se inicia el proceso de carga de contenido encontrado
        #======================================================================
        i=1
        string = ""
        deboVerSig=False
        deboIgnorar=False
        with open('Resultados/Materia.txt', 'r') as archivo:
            #==================================================================
            #Query Sql de lista negra
            #==================================================================

            db = query.query()
            db.conectar()
            rows = db.select("Dominio, Titulo", "WHERE StringBusqueda =\""+self.controller.frames['menuPrincipal'].entrada.get()+"\" AND tipoHerramienta = \"materia\"", tabla='ListaNegra')
            print("LO ENCONTRADO EN LA LISTA NEGRA ES", rows)
            rows = set(rows)

            for linea in archivo:
                if '===' in linea:
                    anterior = string
                    fuente = linea.split(" ")[1].strip()
                    string+="===Resultado numero "+str(i)+", fuente: "+fuente+"===\n"
                    deboVerSig = True
                    deboIgnorar = False
                elif deboVerSig:
                    titulo = linea.strip()
                    self.encontrados.append( (fuente, titulo) )
                    string+=linea
                    deboVerSig=False
                    #==========================================================
                    #Aqui se debe verificar si esta en la lista negra
                    #==========================================================
                    if(len(rows) != 0):
                        if((fuente, titulo) in rows):
                            print("==SE DETECTO UN RESULTADO BLOQUEADO==")

                            #Se procede a restaurar el string antes del falso positivo
                            string = anterior

                            print(string)
                            del self.encontrados[-1]
                            deboIgnorar = True
                        else:
                            i+=1
                    else:
                        i+=1

                elif deboIgnorar==False:
                    string+=linea

            #A este punto ya tenemos todos los encontrados

        #DEFINICION DEL SPINBOX DE REPORTES
        if self.spinbox==None:
            #self.spinbox = tk.Spinbox(self, values=tuple(range(1, len(self.encontrados)+1)), font=self.controller.regular_font)
            self.spinbox = tk.Spinbox(self, font=self.controller.regular_font)

            self.textoFalsoPositivo = tk.Label(self, text="Algún problema? reporte falsos positivos seleccionando el número.", font=self.controller.regular_font)

            self.botonEnviarReporte = tk.Button(self, text="Enviar", font= self.controller.regular_font,
            command=lambda: self.controller.reportarFalsoPositivo( self.encontrados[int(self.spinbox.get())-1][0] , self.encontrados[int(self.spinbox.get())-1][1] , "materia") )

        self.spinbox["values"]=tuple(range(1, len(self.encontrados)+1))

        self.texto.insert(tk.END, string)
        self.texto.pack(side="top",fill="both", expand=True)

        self.textoFalsoPositivo.pack()
        self.spinbox.pack()
        self.botonEnviarReporte.pack(padx=10, pady=10)

class imagenes(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Imagenes", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.encontrados = list()
        self.spinbox = None

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frameCanvas = tk.Frame(self.canvas, background="#ffffff")
        self.canvas.create_window((4,4), anchor="nw" ,window=self.frameCanvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.frameCanvas.bind("<Configure>", self.onFrameConfigure)

        self.botonRegreso = tk.Button(self, text="Volver al inicio", font= controller.regular_font,
                           command=lambda: controller.show_frame("menuPrincipal"))
    """
        self.canvas = tk.Canvas(controller, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(controller, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.botonRegreso = tk.Button(self, text="Volver al inicio", font= controller.regular_font,
                           command=lambda: controller.show_frame("menuPrincipal"))

    """
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def mostrar(self):
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.botonRegreso.pack(side="left" ,padx=10, pady=5)

        #=======================================================================
        #Se inicio proceso de carga de imagenes
        #=======================================================================
        self.encontrados = list()
        i=1
        with open('Resultados/Imagenes.txt', 'r') as archivo:
            db = query.query()
            db.conectar()
            rows = db.select("Dominio, tipoHerramienta", "WHERE StringBusqueda =\""+self.controller.frames['menuPrincipal'].entrada.get()+"\" AND tipoHerramienta = \"imagenes\"", tabla='ListaNegraImagen')
            db.desconectar()
            rows = set(rows)

            for linea in archivo:
                puedoAgregarlo=True
                try:
                    #===========================================================
                    #Ver aca si este url ta bloqueado
                    #===========================================================

                    #rows = lo de la query
                    #
                    print(linea.strip())
                    if((linea.strip(),'imagenes') in rows):
                        puedoAgregarlo=False
                    #
                    #===========================================================

                    if puedoAgregarlo:
                        image_byt = urlopen(linea.strip()).read()
                        image_b64 = base64.encodestring(image_byt)
                        photo = tk.PhotoImage(data=image_b64)
                        panel = tk.Label(self.frameCanvas, image = photo)
                        panel.image = photo

                        titulo = tk.Text(self.frameCanvas, font=self.controller.regular_font,  wrap='word', height= 2, width= 100)
                        string = "===Resultado numero "+str(i)+"===\nFuente: "+linea.strip()+"\n"
                        titulo.insert(tk.END, string)

                        titulo.pack(padx=10)
                        panel.pack(padx=10, pady=10)
                        self.encontrados.append( (panel, titulo, linea.strip()) ) # obj, obj, url
                        i+=1
                except tk.TclError:
                    print("No se pudo visualizar la imagen")

        #DEFINICION DEL SPINBOX DE REPORTES
        if self.spinbox==None:
            self.spinbox = tk.Spinbox(self, values=tuple(range(1, len(self.encontrados)+1)), font=self.controller.regular_font)
            self.textoFalsoPositivo = tk.Label(self, text="Algún problema? reporte falsos positivos seleccionando el número.", font=self.controller.regular_font)

            self.botonEnviarReporte = tk.Button(self, text="Enviar", font= self.controller.regular_font,
                                 command=lambda: self.controller.reportarFalsoPositivo( self.encontrados[int(self.spinbox.get())-1][2] , None , "imagenes") )
                                 ###VER LA FUNCION LAMBDA PARA QUE EFECTIVAMENTE META LO NECESARIO PARA REPORTAR LA IMAGEN
        self.textoFalsoPositivo.pack()
        self.spinbox.pack()
        self.botonEnviarReporte.pack(padx=10, pady=10)

app = Aplicacion()
app.geometry("1280x720")
app.mainloop()

"""
class materia(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Materia", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.texto = ScrolledText(self, font=controller.regular_font,  wrap='word', height= 40, width= 115)



        self.button = tk.Button(self, text="Volver al inicio", font= controller.regular_font,
                           command=lambda: controller.show_frame("menuPrincipal"))
        self.spinbox = None

    def mostrar(self):
         #======================================================================
         #Se inicia el proceso de carga de contenido encontrado
         #======================================================================
         i=1
         encontrados=list()
         string = ""
         deboVerSig=False
         deboIgnorar=False
         with open('Resultados/StringsLimpios.txt', 'r') as archivo:
             #==================================================================
             #Query Sql de lista negra
             #==================================================================

             db = query.query()
             db.conectar()
             rows = db.select("Dominio, Titulo", "WHERE StringBusqueda =\""+self.controller.frames['menuPrincipal'].entrada.get()+"\" AND tipoHerramienta = \"materia\"", tabla='ListaNegra')
             print("LO ENCONTRADO EN LA LISTA NEGRA ES", rows)
             rows = set(rows)

             for linea in archivo:
                 if '===' in linea:
                     anterior = string
                     fuente = linea.split(" ")[1].strip()
                     string+="===Resultado numero "+str(i)+", fuente: "+fuente+"===\n"
                     deboVerSig = True
                     deboIgnorar = False
                 elif deboVerSig:
                     titulo = linea.strip()
                     encontrados.append( (fuente, titulo) )
                     string+=linea
                     deboVerSig=False
                     #==========================================================
                     #Aqui se debe verificar si esta en la lista negra
                     #==========================================================
                     if(len(rows) != 0):
                         if((fuente, titulo) in rows):
                             print("==SE DETECTO UN RESULTADO BLOQUEADO==")

                             #Se procede a restaurar el string antes del falso positivo
                             string = anterior

                             print(string)
                             del encontrados[-1]
                             deboIgnorar = True
                         else:
                             i+=1

                 elif deboIgnorar==False:
                     string+=linea

             #A este punto ya tenemos todos los encontrados

         #DEFINICION DEL SPINBOX DE REPORTES
         if self.spinbox==None:
             self.spinbox = tk.Spinbox(self, values=tuple(range(1, len(encontrados)+1)), font=self.controller.regular_font)
             self.textoFalsoPositivo = tk.Label(self, text="Algún problema? reporte falsos positivos seleccionando el número.", font=self.controller.regular_font)

             self.botonEnviarReporte = tk.Button(self, text="Enviar", font= self.controller.regular_font,
                                  command=lambda: self.controller.reportarFalsoPositivo( encontrados[int(self.spinbox.get())-1][0] , encontrados[int(self.spinbox.get())-1][1] , "materia") )


         self.texto.insert(tk.END, string)
         self.texto.pack(side="top",fill="both", expand=True)
         self.button.pack(side="left", padx=10, pady=10)
         self.textoFalsoPositivo.pack()
         self.spinbox.pack()
         self.botonEnviarReporte.pack(padx=10, pady=10)

"""
