from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import tkinter as tk
import base64
from urllib.request import urlopen



process = CrawlerProcess(get_project_settings())

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.buscar_imagen = tk.Button(self)
        self.buscar_imagen["text"] = "Buscar imagenes\n"
        self.buscar_imagen["command"] = self.iniciar_Crawl_Imagen
        self.buscar_imagen.pack(side="top")

        self.ver_resultados = tk.Button(self)
        self.ver_resultados["text"] = "Ver resultados \n"
        self.ver_resultados["command"] = self.func_resultados
        self.ver_resultados.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit.pack(side="bottom")

    def iniciar_Crawl_Imagen(self):
        process.crawl('imagenes')
        process.start()

    def func_resultados(self):
        archivo = open('Resultado.txt','r')
        lista = []
        for url in archivo:
            lista.append(url)
        archivo.close()

        for i in lista:
            try:
                image_byt = urlopen(i).read()
                image_b64 = base64.encodestring(image_byt)
                photo = tk.PhotoImage(data=image_b64)
                panel = tk.Label(self, image = photo)
                panel.image = photo
                panel.pack()
            except tk.TclError:
                print("no pude")
            

# 'followall' is the name of one of the spiders of the project.

 # the script will block here until the crawling is finished
root = tk.Tk()
app = Application(master=root)
app.mainloop()
