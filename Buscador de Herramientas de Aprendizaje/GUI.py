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
        for F in (menuPrincipal, materia, imagenes, desbloqueo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("menuPrincipal")

    def show_frame(self, tipo=None, campo=None):
        if campo=="":#Caso en que no metio nada como campo de busqueda
            self.frames["menuPrincipal"].errores["text"]="Error, porfavor ingrese un tópico para la busqueda"
            self.frames["menuPrincipal"].errores["fg"]="red"
            self.frames["menuPrincipal"].errores.pack(pady=2)
            return None
        else:
            self.frames["menuPrincipal"].errores.pack_forget()
            if tipo[0]==0: #Materia
                #Se debe borrar (dejar en blanco) cualquier txt previo
                """
                with open('Resultados/Materia.txt', 'w') as archivo:
                    pass
                """

                #===================================================================
                #Inicio Busqueda de materia
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
                if(len(listaUrl) == 0):
                    self.frames["menuPrincipal"].errores["text"]="No se encontraron resultados para " + campo
                    self.frames["menuPrincipal"].errores["fg"]="red"
                    self.frames["menuPrincipal"].errores.pack(pady=2)
                    return None
                else:
                    configure_logging()
                    runner = CrawlerRunner().create_crawler(tablasSpider)
                    d = runner.crawl(tablasSpider, start_urls = listaUrl)
                    d.addBoth(lambda _: reactor.crash())
                    reactor.run()
                """



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
                if(len(listaUrl) == 0):
                    self.frames["menuPrincipal"].errores["text"]="No se encontraron resultados para " + campo
                    self.frames["menuPrincipal"].errores["fg"]="red"
                    self.frames["menuPrincipal"].errores.pack(pady=2)
                    return None
                else:
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
            elif tipo=="desbloqueo":
                frame = self.frames["desbloqueo"]
                frame.mostrar()
            else:
                #Se deben resetear los campos de los otros frames antes de volver
                self.frames["materia"].texto.delete("1.0", tk.END)
                self.frames["materia"].encontrados=list()
                self.frames["materia"].textoFeedback.pack_forget()

                for panel, titulo, url in self.frames["imagenes"].encontrados:
                    panel.pack_forget()
                    titulo.pack_forget()
                self.frames["imagenes"].encontrados=list()
                self.frames["imagenes"].textoFeedback.pack_forget()

                for i in self.frames["desbloqueo"].listaFrames:
                    i.pack_forget()
                    del i

                self.frames["desbloqueo"].labelMateria.pack_forget()
                self.frames["desbloqueo"].labelImagen.pack_forget()
                self.frames["desbloqueo"].textoFeedback.pack_forget()
                self.frames["desbloqueo"].frameInferior.pack_forget()

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

        self.frames[TipoHerramienta].textoFeedback["text"] = "Listo, herramienta de aprendizaje bloqueada."
        self.frames[TipoHerramienta].textoFeedback["fg"] = "black"
        self.frames[TipoHerramienta].textoFeedback.pack(side="bottom", pady="5")

        #=======================================================================
        #Fin añadir lo seleccionado
        #=======================================================================
    def desbloquear(self, iterador):
        db = query.query()
        db.conectar()
        iterador = list(iterador)
        if len(iterador)>0:
            for i in iterador:
                print("Se encontro presionado\n", i)
                if(len(i) == 4):
                    db.delete("WHERE StringBusqueda = \'"+i[2]+"\' AND Dominio = \'"+i[0]+ "\' AND Titulo = \'"+i[1]+"\'", tabla = 'ListaNegra')
                elif(len(i) == 3):
                    db.delete("WHERE StringBusqueda = \'"+i[1]+"\' AND Dominio = \'"+i[0]+"\'", tabla = 'ListaNegraImagen')
            self.frames["desbloqueo"].textoFeedback["text"] = "Listo, Herramienta(s) de aprendizaje desbloada(s)."
            self.frames["desbloqueo"].textoFeedback["fg"] = "black"
            self.frames["desbloqueo"].textoFeedback.pack(pady="5")
        else:
            self.frames["desbloqueo"].textoFeedback["text"] = "Error, usted no ha seleccionado ningún objeto."
            self.frames["desbloqueo"].textoFeedback["fg"] = "red"
            self.frames["desbloqueo"].textoFeedback.pack(pady="5")
        #Dale mauro aqui debes ocupar el iterador que te entra para poder desbloquear
        #el objeto de aprendizaje según sea materia (largo 4) o imagen (largo 3)
        #no pesques lo que hay en la última posicion de del iterador (es algo que ocupé antes...)
        #el iterador te saca listas de la forma [url, fuente, string, <obj de tkinter>](si es materia)
        #ve lo que imprime el for y vas a cachar altoque xD



class menuPrincipal(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Menu principal", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        tk.Label(self, text="Ingrese un tópico para sobre el cual buscar:", font=controller.regular_font).pack(side="top", fill="x", pady=2)

        self.entrada = tk.Entry(self, width= 50, font = controller.regular_font)
        self.entrada.pack()

        tk.Label(self, text="Seleccione alguna herramienta de aprendizaje", font=controller.regular_font).pack(side="top", fill="x", pady=5)

        opcionesBusqueda = tk.Listbox(self, selectmode="Single", font = controller.regular_font)
        opcionesBusqueda.insert(tk.END, "Materia", "Imagenes")
        opcionesBusqueda.select_set(0)
        opcionesBusqueda.pack()

        botonBusqueda = tk.Button(self, text="Iniciar Busqueda", font = controller.regular_font,
                                       command = lambda: controller.show_frame( opcionesBusqueda.curselection() , self.entrada.get() ))
        botonBusqueda.pack()

        tk.Button(self, text="Gestionar lista negra", font = controller.regular_font,
                  command = lambda: controller.show_frame( "desbloqueo" , "Nya" )).pack(pady=5)

        self.errores = tk.Label(self, font=controller.regular_font)



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

        self.frameInferior = tk.Frame(self, height=300)

        self.texto = tk.Text(self.frameCanvas, font=controller.regular_font,  wrap='word', height= 100, width= 115)

        self.botonRegreso = tk.Button(self.frameInferior, text="Volver al inicio", font= controller.regular_font,
                           command=lambda: controller.show_frame("menuPrincipal"))

        self.textoFeedback = tk.Label(self, font=self.controller.regular_font)

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
            self.spinbox = tk.Spinbox(self.frameInferior, font=self.controller.regular_font)

            self.textoFalsoPositivo = tk.Label(self.frameInferior, text="¿Algún problema? reporte falsos positivos seleccionando el número.", font=self.controller.regular_font)

            self.botonEnviarReporte = tk.Button(self.frameInferior, text="Enviar", font= self.controller.regular_font,
            command=lambda: self.controller.reportarFalsoPositivo( self.encontrados[int(self.spinbox.get())-1][0] , self.encontrados[int(self.spinbox.get())-1][1] , "materia") )

        self.spinbox["values"]=tuple(range(1, len(self.encontrados)+1))

        self.texto.insert(tk.END, string)
        self.texto.pack(side="top",fill="both", expand=True)

        self.frameInferior.pack(fill="both")

        self.textoFalsoPositivo.pack(side="left", padx="5", fill="x", expand=True)
        self.botonEnviarReporte.pack(side="bottom")
        self.spinbox.pack(side="bottom")

class imagenes(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Imagenes", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.frameInferior = tk.Frame(self, height=300)
        self.encontrados = list()
        self.spinbox = None

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frameCanvas = tk.Frame(self.canvas, background="#ffffff")
        self.canvas.create_window((4,4), anchor="nw" ,window=self.frameCanvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.frameCanvas.bind("<Configure>", self.onFrameConfigure)

        self.botonRegreso = tk.Button(self.frameInferior, text="Volver al inicio", font= controller.regular_font,
                           command=lambda: controller.show_frame("menuPrincipal"))

        self.textoFeedback = tk.Label(self, font=self.controller.regular_font)

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
            self.spinbox = tk.Spinbox(self.frameInferior, values=tuple(range(1, len(self.encontrados)+1)), font=self.controller.regular_font)
            self.textoFalsoPositivo = tk.Label(self.frameInferior, text="¿Algún problema? reporte falsos positivos seleccionando el número.", font=self.controller.regular_font)

            self.botonEnviarReporte = tk.Button(self.frameInferior, text="Enviar", font= self.controller.regular_font,
                                 command=lambda: self.controller.reportarFalsoPositivo( self.encontrados[int(self.spinbox.get())-1][2] , None , "imagenes") )
                                 ###VER LA FUNCION LAMBDA PARA QUE EFECTIVAMENTE META LO NECESARIO PARA REPORTAR LA IMAGEN
        self.textoFalsoPositivo.pack(side="left")
        self.botonEnviarReporte.pack(padx=10, pady=10, side= "bottom")
        self.spinbox.pack(side="bottom")
        self.frameInferior.pack(fill="x")

class desbloqueo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Desbloquear objeto de aprendizaje de la lista negra", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.listaFrames = list()
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frameCanvas = tk.Frame(self.canvas, background="#ffffff")
        self.canvas.create_window((4,4), anchor="nw" ,window=self.frameCanvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.frameCanvas.bind("<Configure>", self.onFrameConfigure)

        self.labelMateria = tk.Label(self.frameCanvas, text="Materia bloqueada", font=self.controller.regular_font)
        self.labelImagen = tk.Label(self.frameCanvas, text="Imagenes bloqueadas", font=self.controller.regular_font)

        self.frameInferior = tk.Frame(self)
        self.textoFeedback = tk.Label(self.frameInferior, font=self.controller.regular_font)
        self.botonRegreso = tk.Button(self.frameInferior, text="Volver al inicio", font= controller.regular_font,
        command=lambda: controller.show_frame("menuPrincipal"))

        self.botonDesbloqueo = tk.Button(self.frameInferior, text="Desbloquear seleccionados", font= self.controller.regular_font)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def mostrar(self):
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.frameInferior.pack(side="bottom", fill="x")
        self.botonDesbloqueo.pack(side="right", padx=10, pady=5)
        self.botonRegreso.pack(side="left" ,padx=10, pady=5)

        #Aqui se deben obtener los objetos que esten baneados
        #Si eran materia deberian tener (fuente, titulo, stringBusqueda)
        #Si es una imagen, (fuente, stringBusqueda)
        #Estos objetos espero que esten en 2 listas de la forma, ojalá que esten ordenados por
        #texto de busqueda
        #materiaBaneada = [ [fuente, titulo, stringBusqueda], [fuente, titulo, stringBusqueda]]
        #imagenBaneada = [ [fuente, stringBusqueda], [fuente, stringBusqueda]]


        db = query.query()
        db.conectar()
        materiaBaneada = db.select("Dominio, Titulo, StringBusqueda", "ORDER BY StringBusqueda", tabla = 'ListaNegra')
        materiaBaneada = list(map(list,materiaBaneada))

        imagenBaneada = db.select("Dominio, StringBusqueda", "ORDER BY StringBusqueda", tabla = 'ListaNegraImagen')
        imagenBaneada = list(map(list,imagenBaneada))


        baneados = list()
        if len(materiaBaneada)==0:
            self.labelMateria["text"]="No se encontró materia bloqueada."
        else:
            self.labelMateria["text"]="Materia bloqueada."
        self.labelMateria.pack()

        for i in range(len(materiaBaneada)):
            materiaBaneada[i].append(tk.IntVar())
            frame = tk.Frame(self.frameCanvas)
            self.listaFrames.append(frame)
            frame.pack(fill="x", pady="2.5")
            texto = tk.Text(frame, font=self.controller.regular_font,  wrap='word', height= 3, width= 100)
            string = "Texto de busqueda: "+str(materiaBaneada[i][2])+"\nTitulo: "+str(materiaBaneada[i][1])+"\nURL Fuente: "+str(materiaBaneada[i][0])+'\n'
            texto.insert(tk.END, string)
            texto.pack(side="left",padx=10)
            baneados.append(materiaBaneada[i])

            tk.Checkbutton(frame, text="¿Desbloquear?", font = self.controller.regular_font, variable = materiaBaneada[i][3], onvalue = 1, offvalue = 0).pack(side="right")

        if len(imagenBaneada)==0:
            self.labelImagen["text"]="No se encontraron imagenes bloqueadas."
        else:
            self.labelImagen["text"]="Imagenes bloqueadas."
        self.labelImagen.pack()

        for i in range(len(imagenBaneada)):
            imagenBaneada[i].append(tk.IntVar())
            frame = tk.Frame(self.frameCanvas)
            self.listaFrames.append(frame)
            frame.pack(fill="x", pady="2.5")
            texto = tk.Text(frame, font=self.controller.regular_font,  wrap='word', height= 2, width= 100)
            string = "Texto de busqueda: "+str(imagenBaneada[i][1])+"\nURL Fuente: "+str(imagenBaneada[i][0])+'\n'
            texto.insert(tk.END, string)
            texto.pack(side="left",padx=10)
            baneados.append(imagenBaneada[i])

            tk.Checkbutton(frame, text="¿Desbloquear?", font = self.controller.regular_font, variable = imagenBaneada[i][2], onvalue = 1, offvalue = 0).pack(side="right")

        self.botonDesbloqueo["command"] = command=lambda: self.controller.desbloquear(filter(lambda x: x[-1].get()==1, baneados))
        self.botonDesbloqueo.pack()






app = Aplicacion()
app.geometry("1280x720")
app.mainloop()
