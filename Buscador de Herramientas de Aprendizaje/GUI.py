import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter.scrolledtext import ScrolledText
import url_Obtainer
import query
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
process = CrawlerProcess(get_project_settings())

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
        for F in (menuPrincipal, materia, PageTwo):
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
            #===================================================================
            #Aqui se debe buscar materia y dejarla en txt
            #===================================================================
            #===================================================================
            #Inicio Busqueda de materia
            #===================================================================
            
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
            process = CrawlerProcess(get_project_settings())
            process.crawl('tablas', start_urls = listaUrl)
            process.start()

            #===================================================================
            #FIN Busqueda de materia
            #===================================================================

            frame = self.frames["materia"]
            frame.mostrar()
        else:
            frame = self.frames["menuPrincipal"]
        frame.tkraise()
    def reportarFalsoPositivo(self, dominio=None, titulo=None, tipoHerramienta=None):
        print("Datos ingresados",dominio," = ",titulo," = ",tipoHerramienta)
        #=======================================================================
        #Aqui se debe hacer coneccion a base de datos y añadir lo seleccionado
        #=======================================================================


class menuPrincipal(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Menu principal", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        entrada = tk.Entry(self, width= 50, font = controller.regular_font)
        entrada.pack()

        opcionesBusqueda = tk.Listbox(self, selectmode="Single", font = controller.regular_font)
        opcionesBusqueda.insert(tk.END, "Materia", "Imagenes")
        opcionesBusqueda.pack()

        botonBusqueda = tk.Button(self, text="Iniciar Busqueda", font = controller.regular_font,
                                       command = lambda: controller.show_frame( opcionesBusqueda.curselection() , entrada.get() ))
        botonBusqueda.pack()

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
         string=""
         deboVerSig=False
         with open('Resultados/StringsLimpios.txt', 'r') as archivo:

             for linea in archivo:
                 if '===' in linea:
                     fuente = linea.split(" ")[1].strip()
                     string+="===Objeto numero "+str(i)+", fuente: "+fuente+"\n"
                     deboVerSig = True
                 elif deboVerSig:
                     titulo = linea.strip()
                     encontrados.append( (fuente, titulo) )
                     string+=linea
                     deboVerSig=False
                     #==========================================================
                     #Aqui se debe verificar si esta en la lista negra
                     #==========================================================
                     #a[:a.rfind('\n')]

                 else:
                     string+=linea


             #string=archivo.read()

             print(encontrados)

         #DEFINICION DEL SPINBOX DE REPORTES
         if self.spinbox==None:
             self.spinbox = tk.Spinbox(self, from_=1, to=len(encontrados), font=self.controller.regular_font)
             self.textoFalsoPositivo = tk.Label(self, text="Algún problema? reporte falsos positivos seleccionando el numero.", font=self.controller.regular_font)

             self.botonEnviarReporte = tk.Button(self, text="Enviar", font= self.controller.regular_font,
                                  command=lambda: self.controller.reportarFalsoPositivo( encontrados[int(self.spinbox.get())-1][0] , encontrados[int(self.spinbox.get())-1][1] , "materia") )


         self.texto.insert(tk.END, string)
         self.texto.pack(side="top",fill="both", expand=True)
         self.button.pack(side="left", padx=10, pady=10)
         self.textoFalsoPositivo.pack()
         self.spinbox.pack()
         self.botonEnviarReporte.pack(padx=10, pady=10)

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

app = Aplicacion()
app.mainloop()
